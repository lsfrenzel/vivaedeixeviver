from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Voluntario(UserMixin, db.Model):
    __tablename__ = 'voluntarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    estado_padrao = db.Column(db.String(2))
    hospital_padrao_id = db.Column(db.Integer, db.ForeignKey('hospitais.id'))
    
    hospital_padrao = db.relationship('Hospital', backref='voluntarios')
    diarios = db.relationship('Diario', backref='voluntario', lazy=True, cascade='all, delete-orphan')
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Hospital(db.Model):
    __tablename__ = 'hospitais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(2), nullable=False)


class Livro(db.Model):
    __tablename__ = 'livros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(300), nullable=False)
    autor = db.Column(db.String(200))
    editora = db.Column(db.String(200))


class Diario(db.Model):
    __tablename__ = 'diarios'
    
    id = db.Column(db.Integer, primary_key=True)
    voluntario_id = db.Column(db.Integer, db.ForeignKey('voluntarios.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    periodo = db.Column(db.String(20), nullable=False)
    duracao = db.Column(db.Float, nullable=False)
    pacientes_atendidos = db.Column(db.JSON)
    locais_atendimento = db.Column(db.JSON)
    livros_contados = db.Column(db.JSON)
    relato_qualitativo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
