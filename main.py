from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas
from database import SessionLocal, engine
from crud import get_livro_crud, get_categoria_crud

# Cria tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Livros API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Dependência para obter sessão de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== LIVROS ====================

@app.get("/livros/", response_model=List[schemas.LivroRead])
def list_livros(categoria_id: Optional[int] = None, db: Session = Depends(get_db)):
    crud = get_livro_crud(db)
    if categoria_id is not None:
        return crud.read_by_categoria(categoria_id)
    return crud.read_all()

@app.get("/livros/{livro_id}", response_model=schemas.LivroRead)
def get_livro(livro_id: int, db: Session = Depends(get_db)):
    crud = get_livro_crud(db)
    livro = crud.read(livro_id)
    if not livro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Livro não encontrado")
    return livro

@app.post(
    "/livros/",
    response_model=schemas.LivroRead,
    status_code=status.HTTP_201_CREATED
)
def create_livro(livro_in: schemas.LivroCreate, db: Session = Depends(get_db)):
    crud = get_livro_crud(db)
    try:
        return crud.create(livro_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))

@app.put("/livros/{livro_id}", response_model=schemas.LivroRead)
def update_livro(livro_id: int, livro_in: schemas.LivroUpdate, db: Session = Depends(get_db)):
    crud = get_livro_crud(db)
    updated = crud.update(livro_id, livro_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Livro não encontrado")
    return updated

@app.patch("/livros/{livro_id}", response_model=schemas.LivroRead)
def patch_livro(
    livro_id: int,
    livro_in: schemas.LivroUpdate,
    db: Session = Depends(get_db)
):
    crud = get_livro_crud(db)
    updated = crud.update(livro_id, livro_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Livro não encontrado")
    return updated

@app.delete(
    "/livros/{livro_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_livro(livro_id: int, db: Session = Depends(get_db)):
    crud = get_livro_crud(db)
    if not crud.delete(livro_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Livro não encontrado")
    return None


# ==================== CATEGORIAS ====================

@app.get("/categorias/", response_model=List[schemas.CategoriaRead])
def list_categorias(db: Session = Depends(get_db)):
    crud = get_categoria_crud(db)
    return crud.read_all()

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaRead)
def get_categoria(categoria_id: int, db: Session = Depends(get_db)):
    crud = get_categoria_crud(db)
    categoria = crud.read(categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria não encontrada")
    return categoria

@app.post(
    "/categorias/",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_201_CREATED
)
def create_categoria(categoria_in: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    crud = get_categoria_crud(db)
    return crud.create(categoria_in)

@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaRead)
def update_categoria(categoria_id: int, categoria_in: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    crud = get_categoria_crud(db)
    updated = crud.update(categoria_id, categoria_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria não encontrada")
    return updated

@app.patch("/categorias/{categoria_id}", response_model=schemas.CategoriaRead)
def patch_categoria(
    categoria_id: int,
    categoria_in: schemas.CategoriaUpdate,
    db: Session = Depends(get_db)
):
    crud = get_categoria_crud(db)
    updated = crud.update(categoria_id, categoria_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria não encontrada")
    return updated

@app.delete(
    "/categorias/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    crud = get_categoria_crud(db)
    try:
        if not crud.delete(categoria_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Categoria não encontrada")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    return None
