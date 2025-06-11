from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from models import Livro, Categoria
import schemas


class LivroCRUD:
    """Operações CRUD básicas para Livro"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: schemas.LivroCreate) -> Livro:
        try:
            livro = Livro(**data.dict())
            self.db.add(livro)
            self.db.commit()
            self.db.refresh(livro)
            return livro
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro de integridade")

    def read(self, livro_id: int) -> Optional[Livro]:
        return self.db.query(Livro).get(livro_id)

    def read_all(self) -> List[Livro]:
        """Retorna todos os livros"""
        return self.db.query(Livro).all()

    def read_by_categoria(self, categoria_id: int) -> List[Livro]:
        """Retorna todos os livros de uma categoria"""
        return (
            self.db.query(Livro)
                   .filter(Livro.categoria_id == categoria_id)
                   .all()
        )

    def update(self, livro_id: int, data: schemas.LivroUpdate) -> Optional[Livro]:
        livro = self.read(livro_id)
        if not livro:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(livro, key, value)
        try:
            self.db.commit()
            self.db.refresh(livro)
            return livro
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro de integridade")

    def delete(self, livro_id: int) -> bool:
        livro = self.read(livro_id)
        if not livro:
            return False
        self.db.delete(livro)
        self.db.commit()
        return True


class CategoriaCRUD:
    """Operações CRUD básicas para Categoria"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: schemas.CategoriaCreate) -> Categoria:
        categoria = Categoria(**data.dict())
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def read(self, categoria_id: int) -> Optional[Categoria]:
        return self.db.query(Categoria).get(categoria_id)

    def read_all(self) -> List[Categoria]:
        """Retorna todas as categorias"""
        return self.db.query(Categoria).all()

    def update(self, categoria_id: int, data: schemas.CategoriaUpdate) -> Optional[Categoria]:
        categoria = self.read(categoria_id)
        if not categoria:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(categoria, key, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, categoria_id: int) -> bool:
        categoria = self.read(categoria_id)
        if not categoria:
            return False
        # não permite exclusão se houver livros associados
        has_livros = (
            self.db.query(Livro)
                   .filter(Livro.categoria_id == categoria_id)
                   .count() > 0
        )
        if has_livros:
            raise ValueError("Não é possível excluir categoria com livros associados")
        self.db.delete(categoria)
        self.db.commit()
        return True


# Funções de injeção de dependência
def get_livro_crud(db: Session) -> LivroCRUD:
    return LivroCRUD(db)

def get_categoria_crud(db: Session) -> CategoriaCRUD:
    return CategoriaCRUD(db)