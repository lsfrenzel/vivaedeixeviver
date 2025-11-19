from app import app, db
from models import Voluntario, Hospital, Livro, Diario
from datetime import datetime, timedelta
import random


def seed_database():
    with app.app_context():
        print("Limpando banco de dados...")
        db.drop_all()
        db.create_all()
        
        print("Criando hospitais...")
        hospitais = [
            Hospital(nome="Hospital das Clínicas", estado="SP"),
            Hospital(nome="Hospital São Paulo", estado="SP"),
            Hospital(nome="Hospital Universitário", estado="RJ"),
            Hospital(nome="Hospital da Criança", estado="MG"),
            Hospital(nome="Hospital Regional", estado="RS"),
        ]
        db.session.add_all(hospitais)
        db.session.commit()
        
        print("Criando administrador...")
        admin = Voluntario(
            nome="Administrador",
            email="admin@teste.com",
            estado_padrao="SP",
            hospital_padrao_id=hospitais[0].id,
            is_admin=True
        )
        admin.set_senha("admin123")
        db.session.add(admin)
        
        print("Criando voluntário de teste...")
        voluntario = Voluntario(
            nome="Maria Silva",
            email="voluntario@teste.com",
            estado_padrao="SP",
            hospital_padrao_id=hospitais[0].id,
            is_admin=False
        )
        voluntario.set_senha("senha123")
        db.session.add(voluntario)
        db.session.commit()
        
        print("Criando livros de exemplo...")
        livros_exemplo = [
            Livro(titulo="O Pequeno Príncipe", autor="Antoine de Saint-Exupéry", editora="Agir"),
            Livro(titulo="A Menina que Roubava Livros", autor="Markus Zusak", editora="Intrínseca"),
            Livro(titulo="O Menino Maluquinho", autor="Ziraldo", editora="Melhoramentos"),
            Livro(titulo="Chapeuzinho Vermelho", autor="Irmãos Grimm", editora="Ática"),
            Livro(titulo="Os Três Porquinhos", autor="Desconhecido", editora="Todolivro"),
            Livro(titulo="A Bela e a Fera", autor="Jeanne-Marie Leprince de Beaumont", editora="Companhia das Letrinhas"),
            Livro(titulo="Alice no País das Maravilhas", autor="Lewis Carroll", editora="Zahar"),
            Livro(titulo="Peter Pan", autor="J.M. Barrie", editora="Principis"),
            Livro(titulo="Pinóquio", autor="Carlo Collodi", editora="Cosac Naify"),
            Livro(titulo="A Bela Adormecida", autor="Charles Perrault", editora="FTD"),
            Livro(titulo="Branca de Neve", autor="Irmãos Grimm", editora="Moderna"),
            Livro(titulo="Cinderela", autor="Charles Perrault", editora="Salamandra"),
            Livro(titulo="O Patinho Feio", autor="Hans Christian Andersen", editora="Paulus"),
            Livro(titulo="João e Maria", autor="Irmãos Grimm", editora="Scipione"),
            Livro(titulo="A Cigarra e a Formiga", autor="Esopo", editora="Companhia Editora Nacional"),
        ]
        db.session.add_all(livros_exemplo)
        db.session.commit()
        
        print("Criando atuações de exemplo...")
        locais = ["Leito", "UTI", "Pediatria", "Oncologia", "Enfermaria"]
        periodos = ["Manhã", "Tarde", "Noite"]
        
        for i in range(15):
            data = datetime.now().date() - timedelta(days=random.randint(0, 180))
            
            pacientes = {}
            faixas = ['0-3', '4-6', '7-9', '10-12', '13-15', '16-18']
            for faixa in faixas:
                pacientes[faixa] = {
                    'feminino': random.randint(0, 5),
                    'masculino': random.randint(0, 5)
                }
            
            livros_atuacao = random.sample(livros_exemplo, random.randint(1, 3))
            livros_data = [{
                'id': livro.id,
                'titulo': livro.titulo,
                'autor': livro.autor,
                'editora': livro.editora
            } for livro in livros_atuacao]
            
            diario = Diario(
                voluntario_id=voluntario.id,
                data=data,
                periodo=random.choice(periodos),
                duracao=random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 4.0]),
                pacientes_atendidos=pacientes,
                locais_atendimento=random.sample(locais, random.randint(1, 3)),
                livros_contados=livros_data,
                relato_qualitativo=f"Atuação muito gratificante. As crianças adoraram as histórias e demonstraram grande interesse. Foi possível ver sorrisos e momentos de alegria em meio ao tratamento."
            )
            db.session.add(diario)
        
        db.session.commit()
        
        print("✅ Banco de dados populado com sucesso!")
        print("\n📝 Credenciais de acesso:")
        print("\n👤 Voluntário:")
        print("   E-mail: voluntario@teste.com")
        print("   Senha: senha123")
        print("\n🛡️  Administrador:")
        print("   E-mail: admin@teste.com")
        print("   Senha: admin123")


if __name__ == "__main__":
    seed_database()
