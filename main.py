from app import app, db
import models
import routes
import os


def init_users():
    """Create admin and volunteer users if they don't exist."""
    from models import Voluntario, Hospital, Livro, Diario
    from datetime import datetime, timedelta
    
    hospital = Hospital.query.first()
    if not hospital:
        hospital = Hospital(nome="Hospital Padrão", estado="SP")
        db.session.add(hospital)
        db.session.commit()
        print(f"Hospital criado: {hospital.nome}")
    
    admin_exists = Voluntario.query.filter_by(is_admin=True).first()
    if not admin_exists:
        print("Criando admin padrão...")
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@diariodocontador.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        
        admin = Voluntario(
            nome="Administrador",
            email=admin_email,
            estado_padrao="SP",
            hospital_padrao_id=hospital.id,
            is_admin=True
        )
        admin.set_senha(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin criado: {admin_email}")
    else:
        print(f"Admin já existe: {admin_exists.email}")
    
    voluntario = Voluntario.query.filter_by(email="voluntario@diariodocontador.com").first()
    if not voluntario:
        print("Criando voluntário padrão...")
        voluntario = Voluntario(
            nome="Voluntário Teste",
            email="voluntario@diariodocontador.com",
            estado_padrao="SP",
            hospital_padrao_id=hospital.id,
            is_admin=False
        )
        voluntario.set_senha("senha123")
        db.session.add(voluntario)
        db.session.commit()
        print("Voluntário criado: voluntario@diariodocontador.com")
    else:
        print(f"Voluntário já existe: {voluntario.email}")
    
    if Livro.query.count() == 0:
        print("Criando livros de exemplo...")
        livros = [
            Livro(titulo="O Pequeno Príncipe", autor="Antoine de Saint-Exupéry", editora="Agir"),
            Livro(titulo="O Menino Maluquinho", autor="Ziraldo", editora="Melhoramentos"),
            Livro(titulo="Chapeuzinho Vermelho", autor="Irmãos Grimm", editora="Ática"),
            Livro(titulo="Os Três Porquinhos", autor="Tradicional", editora="Todolivro"),
            Livro(titulo="Alice no País das Maravilhas", autor="Lewis Carroll", editora="Zahar"),
        ]
        db.session.add_all(livros)
        db.session.commit()
        print(f"{len(livros)} livros criados")
    
    if Diario.query.count() == 0 and voluntario:
        print("Criando atuação de exemplo...")
        livros = Livro.query.limit(2).all()
        livros_data = [{"id": l.id, "titulo": l.titulo, "autor": l.autor, "editora": l.editora} for l in livros]
        
        atuacao = Diario(
            voluntario_id=voluntario.id,
            data=datetime.now().date(),
            periodo="Manhã",
            duracao=2.0,
            pacientes_atendidos={
                "0-3": {"feminino": 2, "masculino": 1},
                "4-6": {"feminino": 3, "masculino": 2},
                "7-9": {"feminino": 1, "masculino": 2}
            },
            locais_atendimento=["Pediatria", "Enfermaria"],
            livros_contados=livros_data,
            relato_qualitativo="Atuação muito gratificante. As crianças adoraram as histórias!"
        )
        db.session.add(atuacao)
        db.session.commit()
        print("Atuação de exemplo criada")


with app.app_context():
    db.create_all()
    init_users()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
