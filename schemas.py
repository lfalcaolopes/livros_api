from pydantic import BaseModel, Field
from typing import Optional

# ==================== CATEGORIA SCHEMAS ====================
class CategoriaCreate(BaseModel):
    nome: str = Field(..., description="Nome da categoria", min_length=1, max_length=100)
    descricao: Optional[str] = Field(None, description="Descrição da categoria", max_length=500)

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(None, description="Nome da categoria", min_length=1, max_length=100)
    descricao: Optional[str] = Field(None, description="Descrição da categoria", max_length=500)

class CategoriaRead(CategoriaCreate):
    id: int

    class Config:
        orm_mode = True


# ==================== LIVRO SCHEMAS ====================
class LivroCreate(BaseModel):
    titulo: str = Field(..., description="Título do livro", min_length=1, max_length=200)
    autor: str = Field(..., description="Autor do livro", min_length=1, max_length=100)
    ano_publicacao: int = Field(..., description="Ano de publicação", ge=1000, le=2030)
    categoria_id: Optional[int] = Field(None, description="ID da categoria")

class LivroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, description="Título do livro", min_length=1, max_length=200)
    autor: Optional[str] = Field(None, description="Autor do livro", min_length=1, max_length=100)
    ano_publicacao: Optional[int] = Field(None, description="Ano de publicação", ge=1000, le=2030)
    categoria_id: Optional[int] = Field(None, description="ID da categoria")

class LivroRead(LivroCreate):
    id: int

    class Config:
        orm_mode = True