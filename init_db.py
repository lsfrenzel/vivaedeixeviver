from app import app, db
from models import Voluntario, Hospital
import os


def init_database():
    """Initialize database with admin user if none exists."""
    with app.app_context():
        db.create_all()
        
        admin_exists = Voluntario.query.filter_by(is_admin=True).first()
        
        if not admin_exists:
            print("Nenhum administrador encontrado. Criando admin padrão...")
            
            hospital = Hospital.query.first()
            if not hospital:
                hospital = Hospital(nome="Hospital Padrão", estado="SP")
                db.session.add(hospital)
                db.session.commit()
                print(f"Hospital criado: {hospital.nome}")
            
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
            
            print(f"Admin criado com sucesso!")
            print(f"E-mail: {admin_email}")
            print(f"Senha: {admin_password}")
            print("\n*** IMPORTANTE: Troque a senha após o primeiro login! ***")
        else:
            print(f"Admin já existe: {admin_exists.email}")


if __name__ == "__main__":
    init_database()
