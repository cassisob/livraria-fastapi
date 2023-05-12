from fastapi import APIRouter, Depends, Response, status, HTTPException

from livraria.routers import utils
from ..database import SessionLocal, get_db
from .. import models, schemas

from typing import Optional

router = APIRouter(
    tags = ['Editoras'],
    prefix = '/editoras'
)

@router.get('/')
def list_all(search : Optional[str] = "", db: SessionLocal = Depends(get_db)):
    if search != "":
        editoras = db.query(models.Editora).filter(models.Editora.nome.contains(search)).all()
    else:
        editoras = db.query(models.Editora).all()
    return editoras

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Editora, db: SessionLocal = Depends(get_db)):
    new_editora = models.Editora(nome=request.nome, site=request.site)
    db.add(new_editora)
    db.commit()
    db.refresh(new_editora)
    return new_editora

@router.get('/{id}', status_code=status.HTTP_200_OK)
def retrieve(id: int, db: SessionLocal = Depends(get_db)):
    editora = utils.checkEditoraById(id, db).first()
    return editora

@router.delete('/{id}')
def destroy(id: int, db: SessionLocal = Depends(get_db)):
    query = utils.checkEditoraById(id, db)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Editora, db: SessionLocal = Depends(get_db)):
    query = utils.checkEditoraById(id, db)
    query.update( request.dict(), synchronize_session=False )
    db.commit()
    return query.first()