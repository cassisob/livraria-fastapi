from ast import For
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base

class Editora(Base):
    __tablename__ = 'editoras'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)
    site = Column(String)

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key = True, index = True)
    descricao = Column(String)


class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key = True, index = True)
    titulo = Column(String)
    ISBN = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    autores = relationship("Autor", secondary='livros_autores')
    
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria")
    
    editora_id = Column(Integer, ForeignKey("editoras.id"))
    editora = relationship("Editora")

livros_autores = Table(
    'livros_autores', Base.metadata,
    Column('livro_id', ForeignKey('livros.id'), primary_key=True),
    Column('autor_id', ForeignKey('autores.id'), primary_key=True)
)

class Leitor(Base):
    __tablename__ = 'leitores'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)

    favoritos = relationship("Livro", secondary='livros_leitores')

livros_leitores = Table(
    'livros_leitores', Base.metadata,
    Column('leitor_id', ForeignKey('leitores.id'), primary_key=True),
    Column('livro_id', ForeignKey('livros.id'), primary_key=True),
)

