from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException

from livraria.routers import utils
from ..database import SessionLocal, get_db
from .. import models, schemas

from typing import Optional

router = APIRouter(
    tags = ['Leitores'],
    prefix = '/leitores'
)

@router.get('/', response_model=List[schemas.LeitorShow])
def list_all(search : Optional[str] = "", db: SessionLocal = Depends(get_db)):
    if search != "":
        leitores = db.query(models.Leitor).filter(models.Leitor.nome.contains(search)).all()
    else:
        leitores = db.query(models.Leitor).all()
    return leitores

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LeitorShow)
def create(request: schemas.Leitor, db: SessionLocal = Depends(get_db)):
    new_leitor = models.Leitor(nome=request.nome)

    for livro_id in request.favoritos:
        livro = utils.checkLivroById(livro_id, db).first()
        new_leitor.favoritos.append(livro)

    db.add(new_leitor)
    db.commit()
    db.refresh(new_leitor)
    return new_leitor

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LeitorShow)
def retrieve(id: int, db: SessionLocal = Depends(get_db)):
    leitor = utils.checkLivroById(id, db).first()
    return leitor

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.LeitorShow)
def update(id: int, request: schemas.Leitor, db: SessionLocal = Depends(get_db)):
    query = utils.checkLivroById(id, db)
    query.update( request.dict(), synchronize_session=False )

    leitor = query.first()
    leitor.livros = []

    for livro_id in request.livros:
        livro = utils.checkLivroById(livro_id, db).first()
        leitor.livros.append(livro)

    db.commit()
    return query.first()


@router.delete('/{id}')
def destroy(id: int, db: SessionLocal = Depends(get_db)):
    query = utils.checkLeitorById(id, db)

    query.first().favoritos = []

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
