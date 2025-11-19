from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from models import Voluntario, Hospital, Livro, Diario
from datetime import datetime, timedelta
from sqlalchemy import func, extract


@login_manager.user_loader
def load_user(user_id):
    return Voluntario.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        voluntario = Voluntario.query.filter_by(email=email).first()
        
        if voluntario and voluntario.check_senha(senha):
            login_user(voluntario)
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha inválidos.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    inicio_ano = hoje.replace(month=1, day=1)
    
    horas_mes = db.session.query(func.sum(Diario.duracao)).filter(
        Diario.voluntario_id == current_user.id,
        Diario.data >= inicio_mes
    ).scalar() or 0
    
    horas_ano = db.session.query(func.sum(Diario.duracao)).filter(
        Diario.voluntario_id == current_user.id,
        Diario.data >= inicio_ano
    ).scalar() or 0
    
    total_atuacoes = Diario.query.filter_by(voluntario_id=current_user.id).count()
    
    recentes = Diario.query.filter_by(voluntario_id=current_user.id).order_by(
        Diario.data.desc()
    ).limit(5).all()
    
    horas_por_mes = []
    for mes in range(1, 13):
        total = db.session.query(func.sum(Diario.duracao)).filter(
            Diario.voluntario_id == current_user.id,
            extract('year', Diario.data) == hoje.year,
            extract('month', Diario.data) == mes
        ).scalar() or 0
        horas_por_mes.append(float(total))
    
    medalha = None
    if horas_mes >= 20:
        medalha = {'tipo': 'ouro', 'titulo': 'Voluntário Ouro', 'descricao': f'{horas_mes:.1f} horas este mês!'}
    elif horas_mes >= 10:
        medalha = {'tipo': 'prata', 'titulo': 'Voluntário Prata', 'descricao': f'{horas_mes:.1f} horas este mês!'}
    elif horas_mes >= 5:
        medalha = {'tipo': 'bronze', 'titulo': 'Voluntário Bronze', 'descricao': f'{horas_mes:.1f} horas este mês!'}
    
    return render_template('dashboard.html',
                         horas_mes=horas_mes,
                         horas_ano=horas_ano,
                         total_atuacoes=total_atuacoes,
                         recentes=recentes,
                         horas_por_mes=horas_por_mes,
                         medalha=medalha)


@app.route('/nova-atuacao', methods=['GET', 'POST'])
@login_required
def nova_atuacao():
    if request.method == 'POST':
        data = request.form.get('data')
        periodo = request.form.get('periodo')
        duracao = request.form.get('duracao')
        relato = request.form.get('relato_qualitativo')
        
        faixas_etarias = ['0-3', '4-6', '7-9', '10-12', '13-15', '16-18']
        pacientes = {}
        for faixa in faixas_etarias:
            fem = request.form.get(f'pacientes_{faixa}_f') or '0'
            masc = request.form.get(f'pacientes_{faixa}_m') or '0'
            pacientes[faixa] = {'feminino': int(fem), 'masculino': int(masc)}
        
        locais = request.form.getlist('locais_atendimento')
        
        livros_ids = request.form.getlist('livros_selecionados')
        livros_data = []
        for livro_id in livros_ids:
            if livro_id:
                livro = Livro.query.get(int(livro_id))
                if livro:
                    livros_data.append({
                        'id': livro.id,
                        'titulo': livro.titulo,
                        'autor': livro.autor,
                        'editora': livro.editora
                    })
        
        novo_livro_titulo = request.form.get('novo_livro_titulo')
        if novo_livro_titulo:
            novo_livro_autor = request.form.get('novo_livro_autor')
            novo_livro_editora = request.form.get('novo_livro_editora')
            
            livro_existente = Livro.query.filter_by(titulo=novo_livro_titulo).first()
            if not livro_existente:
                novo_livro = Livro(
                    titulo=novo_livro_titulo,
                    autor=novo_livro_autor,
                    editora=novo_livro_editora
                )
                db.session.add(novo_livro)
                db.session.flush()
                livros_data.append({
                    'id': novo_livro.id,
                    'titulo': novo_livro.titulo,
                    'autor': novo_livro.autor,
                    'editora': novo_livro.editora
                })
        
        diario = Diario(
            voluntario_id=current_user.id,
            data=datetime.strptime(data, '%Y-%m-%d').date(),
            periodo=periodo,
            duracao=float(duracao),
            pacientes_atendidos=pacientes,
            locais_atendimento=locais,
            livros_contados=livros_data,
            relato_qualitativo=relato
        )
        
        db.session.add(diario)
        db.session.commit()
        
        flash('Atuação registrada com sucesso!', 'success')
        return redirect(url_for('confirmacao', diario_id=diario.id))
    
    locais_disponiveis = [
        'Leito',
        'UTI',
        'Pronto Socorro',
        'Hemodiálise',
        'Oncologia',
        'Pediatria',
        'Enfermaria',
        'Sala de Espera'
    ]
    
    data_atual = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('nova_atuacao.html',
                         locais_disponiveis=locais_disponiveis,
                         data_atual=data_atual)


@app.route('/confirmacao/<int:diario_id>')
@login_required
def confirmacao(diario_id):
    diario = Diario.query.get_or_404(diario_id)
    
    if diario.voluntario_id != current_user.id:
        flash('Acesso negado.', 'error')
        return redirect(url_for('dashboard'))
    
    total_pacientes = 0
    for faixa, dados in diario.pacientes_atendidos.items():
        total_pacientes += dados.get('feminino', 0) + dados.get('masculino', 0)
    
    return render_template('confirmacao.html', diario=diario, total_pacientes=total_pacientes)


@app.route('/api/buscar-livros')
@login_required
def buscar_livros():
    termo = request.args.get('q', '')
    
    if len(termo) < 2:
        return jsonify([])
    
    livros = Livro.query.filter(
        Livro.titulo.ilike(f'%{termo}%')
    ).limit(10).all()
    
    resultados = [{
        'id': livro.id,
        'titulo': livro.titulo,
        'autor': livro.autor,
        'editora': livro.editora
    } for livro in livros]
    
    return jsonify(resultados)
