from asyncio.windows_events import NULL
from typing import List
from typing import Optional

from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import SessionLocal, get_db
from .. import models, schemas
from . import utils

router = APIRouter(
    tags = ['Livros'],
    prefix = '/livros'
)

@router.get('/', response_model=List[schemas.LivroShow])
def list_all(search : Optional[str] = "", categoria : Optional[int] = "", editora : Optional[int] = "", maxpreco : Optional[int] = "", db: SessionLocal = Depends(get_db)):

    livros = db.query(models.Livro).all()
    
    if search != "":
        for livro in livros:
            if not search in livro.titulo:
                livros.remove(livro)
                
    if categoria != "":
        for livro in livros:
            if not str(categoria) in str(livro.categoria_id):
                livros.remove(livro)
        
    if editora != "":
        for livro in livros:
            if not str(editora) in str(livro.editora_id):
                livros.remove(livro)

    if maxpreco != "":
        for livro in livros:
            if livro.preco > maxpreco:
                livros.remove(livro)

    return livros





@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LivroShow)
def create(request: schemas.Livro, db: SessionLocal = Depends(get_db)):
    
    utils.checkEditoraById(request.editora_id, db)
    utils.checkCategoriaById(request.categoria_id, db)
    
    new_livro = models.Livro(
        titulo = request.titulo,
        ISBN = request.ISBN,
        preco = request.preco,
        quantidade = request.quantidade,
        editora_id = request.editora_id,
        categoria_id = request.categoria_id
    )

    for autor_id in request.autores:
        autor = utils.checkAutorById(autor_id, db).first()
        new_livro.autores.append(autor)

    db.add(new_livro)
    db.commit()
    db.refresh(new_livro)

    return new_livro

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LivroShow)
def retrieve(id: int, db: SessionLocal = Depends(get_db)):
    livro = utils.checkLivroById(id, db).first()
    return livro

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.LivroShow)
def update(id: int, request: schemas.Livro, db: SessionLocal = Depends(get_db)):

    utils.checkCategoriaById(request.categoria_id, db)
    utils.checkEditoraById(request.editora_id, db)

    query = utils.checkLivroById(id, db)
    
    query.update( {
        'titulo' : request.titulo, 
        'ISBN' : request.ISBN,
        'quantidade' : request.quantidade,
        'preco': request.preco,
        'editora_id' : request.editora_id,
        'categoria_id' : request.categoria_id
    }, synchronize_session=False )
    
    livro = query.first()
    livro.autores = []

    for autor_id in request.autores:
        autor = utils.checkAutorById(autor_id, db).first()
        livro.autores.append(autor)

    db.commit()
    return query.first()

@router.delete('/{id}')
def destroy(id: int, db: SessionLocal = Depends(get_db)):
    query = utils.checkLivroById(id, db)
    
    query.first().autores = []

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)