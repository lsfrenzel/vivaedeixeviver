from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from models import Voluntario, Hospital, Livro, Diario
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from functools import wraps


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
                         medalha=medalha,
                         ano_atual=hoje.year)


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


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    inicio_ano = hoje.replace(month=1, day=1)
    
    total_voluntarios = Voluntario.query.count()
    total_atuacoes = Diario.query.count()
    
    horas_mes_total = db.session.query(func.sum(Diario.duracao)).filter(
        Diario.data >= inicio_mes
    ).scalar() or 0
    
    horas_ano_total = db.session.query(func.sum(Diario.duracao)).filter(
        Diario.data >= inicio_ano
    ).scalar() or 0
    
    total_pacientes = 0
    diarios = Diario.query.all()
    for diario in diarios:
        if diario.pacientes_atendidos:
            for faixa, dados in diario.pacientes_atendidos.items():
                total_pacientes += dados.get('feminino', 0) + dados.get('masculino', 0)
    
    total_livros = Livro.query.count()
    
    voluntarios_ativos = db.session.query(
        Voluntario.nome,
        func.sum(Diario.duracao).label('total_horas')
    ).join(Diario).filter(
        Diario.data >= inicio_mes
    ).group_by(Voluntario.id, Voluntario.nome).order_by(
        func.sum(Diario.duracao).desc()
    ).limit(10).all()
    
    horas_por_mes = []
    for mes in range(1, 13):
        total = db.session.query(func.sum(Diario.duracao)).filter(
            extract('year', Diario.data) == hoje.year,
            extract('month', Diario.data) == mes
        ).scalar() or 0
        horas_por_mes.append(float(total))
    
    return render_template('admin_dashboard.html',
                         total_voluntarios=total_voluntarios,
                         total_atuacoes=total_atuacoes,
                         horas_mes_total=horas_mes_total,
                         horas_ano_total=horas_ano_total,
                         total_pacientes=total_pacientes,
                         total_livros=total_livros,
                         voluntarios_ativos=voluntarios_ativos,
                         horas_por_mes=horas_por_mes,
                         ano_atual=hoje.year)


@app.route('/admin/usuarios')
@login_required
@admin_required
def admin_usuarios():
    voluntarios = Voluntario.query.order_by(Voluntario.nome).all()
    
    usuarios_stats = []
    for vol in voluntarios:
        total_horas = db.session.query(func.sum(Diario.duracao)).filter(
            Diario.voluntario_id == vol.id
        ).scalar() or 0
        
        total_atuacoes = Diario.query.filter_by(voluntario_id=vol.id).count()
        
        ultima_atuacao = Diario.query.filter_by(voluntario_id=vol.id).order_by(
            Diario.data.desc()
        ).first()
        
        usuarios_stats.append({
            'voluntario': vol,
            'total_horas': total_horas,
            'total_atuacoes': total_atuacoes,
            'ultima_atuacao': ultima_atuacao.data if ultima_atuacao else None
        })
    
    return render_template('admin_usuarios.html', usuarios_stats=usuarios_stats)


@app.route('/admin/usuarios/criar', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_criar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        estado_padrao = request.form.get('estado_padrao')
        hospital_padrao_id = request.form.get('hospital_padrao_id')
        is_admin = request.form.get('is_admin') == 'on'
        
        if not nome or not email or not senha:
            flash('Nome, email e senha são obrigatórios.', 'error')
            return redirect(url_for('admin_criar_usuario'))
        
        existente = Voluntario.query.filter_by(email=email).first()
        if existente:
            flash('Já existe um usuário com este e-mail.', 'error')
            return redirect(url_for('admin_criar_usuario'))
        
        novo_voluntario = Voluntario(
            nome=nome,
            email=email,
            estado_padrao=estado_padrao if estado_padrao else None,
            hospital_padrao_id=int(hospital_padrao_id) if hospital_padrao_id else None,
            is_admin=is_admin
        )
        novo_voluntario.set_senha(senha)
        
        db.session.add(novo_voluntario)
        db.session.commit()
        
        flash(f'Usuário {nome} criado com sucesso!', 'success')
        return redirect(url_for('admin_usuarios'))
    
    hospitais = Hospital.query.order_by(Hospital.estado, Hospital.nome).all()
    estados = db.session.query(Hospital.estado).distinct().order_by(Hospital.estado).all()
    estados = [e[0] for e in estados]
    
    return render_template('admin_criar_usuario.html', hospitais=hospitais, estados=estados)


@app.route('/admin/usuarios/excluir/<int:usuario_id>', methods=['POST'])
@login_required
@admin_required
def admin_excluir_usuario(usuario_id):
    voluntario = Voluntario.query.get_or_404(usuario_id)
    
    if voluntario.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'error')
        return redirect(url_for('admin_usuarios'))
    
    if voluntario.is_admin:
        admin_count = Voluntario.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            flash('Não é possível excluir o último administrador do sistema.', 'error')
            return redirect(url_for('admin_usuarios'))
    
    db.session.delete(voluntario)
    db.session.commit()
    
    flash(f'Usuário {voluntario.nome} excluído com sucesso.', 'success')
    return redirect(url_for('admin_usuarios'))


@app.route('/admin/relatorios')
@login_required
@admin_required
def admin_relatorios():
    periodo = request.args.get('periodo', 'mes')
    voluntario_id = request.args.get('voluntario_id', '')
    
    hoje = datetime.now()
    
    if periodo == 'mes':
        inicio = hoje.replace(day=1)
        titulo_periodo = f'{inicio.strftime("%B de %Y")}'
    elif periodo == 'ano':
        inicio = hoje.replace(month=1, day=1)
        titulo_periodo = f'Ano {hoje.year}'
    else:
        inicio = datetime(2000, 1, 1)
        titulo_periodo = 'Todo o período'
    
    query = Diario.query.filter(Diario.data >= inicio)
    
    if voluntario_id:
        query = query.filter(Diario.voluntario_id == int(voluntario_id))
    
    diarios = query.order_by(Diario.data.desc()).all()
    
    total_horas = sum(d.duracao for d in diarios)
    total_atuacoes = len(diarios)
    
    total_pacientes = 0
    pacientes_por_faixa = {}
    for diario in diarios:
        if diario.pacientes_atendidos:
            for faixa, dados in diario.pacientes_atendidos.items():
                fem = dados.get('feminino', 0)
                masc = dados.get('masculino', 0)
                total_pacientes += fem + masc
                
                if faixa not in pacientes_por_faixa:
                    pacientes_por_faixa[faixa] = {'feminino': 0, 'masculino': 0}
                pacientes_por_faixa[faixa]['feminino'] += fem
                pacientes_por_faixa[faixa]['masculino'] += masc
    
    livros_contados = {}
    for diario in diarios:
        if diario.livros_contados:
            for livro in diario.livros_contados:
                titulo = livro.get('titulo', 'Desconhecido')
                if titulo not in livros_contados:
                    livros_contados[titulo] = {
                        'titulo': titulo,
                        'autor': livro.get('autor', ''),
                        'editora': livro.get('editora', ''),
                        'vezes': 0
                    }
                livros_contados[titulo]['vezes'] += 1
    
    livros_ranking = sorted(livros_contados.values(), key=lambda x: x['vezes'], reverse=True)[:10]
    
    locais_contagem = {}
    for diario in diarios:
        if diario.locais_atendimento:
            for local in diario.locais_atendimento:
                locais_contagem[local] = locais_contagem.get(local, 0) + 1
    
    voluntarios = Voluntario.query.order_by(Voluntario.nome).all()
    
    return render_template('admin_relatorios.html',
                         diarios=diarios,
                         total_horas=total_horas,
                         total_atuacoes=total_atuacoes,
                         total_pacientes=total_pacientes,
                         pacientes_por_faixa=pacientes_por_faixa,
                         livros_ranking=livros_ranking,
                         locais_contagem=locais_contagem,
                         periodo=periodo,
                         titulo_periodo=titulo_periodo,
                         voluntarios=voluntarios,
                         voluntario_selecionado=voluntario_id)
