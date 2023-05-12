from .. import models
from fastapi import status, HTTPException

def checkLivroById(id, db):
    query = db.query(models.Livro).filter(models.Livro.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'livro with id equals to {id} was not found')
    return query

def checkCategoriaById(id, db):
    query = db.query(models.Categoria).filter(models.Categoria.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'categoria with id equals to {id} was not found')
    return query

def checkEditoraById(id, db):
    query = db.query(models.Editora).filter(models.Editora.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'editora with id equals to {id} was not found')
    return query

def checkAutorById(id, db):
    query = db.query(models.Autor).filter(models.Autor.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'autor with id equals to {id} was not found')
    return query

def checkLeitorById(id, db):
    query = db.query(models.Leitor).filter(models.Leitor.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'leitor with id equals to {id} was not found')
    return query