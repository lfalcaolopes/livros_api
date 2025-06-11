# Livros API - Sistema de Gerenciamento de Livros e Categorias

## 📚 Descrição

API RESTful desenvolvida com FastAPI para gerenciamento de livros e categorias.

---

## 🎯 Objetivos da Avaliação

Este projeto foi desenvolvido para a disciplina **UC Sistemas Distribuídos e Mobile – Avaliação A3**, atendendo aos seguintes requisitos:

- ✅ Operações CRUD para duas entidades relacionadas
- ✅ Acesso a banco de dados relacional
- ✅ Organização do código e boas práticas
- ✅ Injeção de dependência via FastAPI
- ✅ Testes funcionais abrangentes

---

## 🏗️ Arquitetura REST - Constraints Implementados

1. **Client-Server**
2. **Stateless**
3. **Uniform Interface**
   - URIs padronizadas e consistentes
   - Métodos HTTP apropriados (GET, POST, PUT, PATCH, DELETE)
4. **Layered System**
5. **Code on Demand (Opcional)**
   - Documentação interativa com Swagger UI

---

## 🗄️ Modelo de Dados

### Entidades

1. **Livro**
   - `id` (Primary Key)
   - `titulo`
   - `autor`
   - `ano_publicacao`
   - `categoria_id` (Foreign Key)

2. **Categoria**
   - `id` (Primary Key)
   - `nome`
   - `descricao`

### Relacionamentos

- Uma categoria pode ter muitos livros (1:N)
- Um livro pertence a uma categoria

---

## 🚀 Endpoints da API

### Livros

- `GET /livros/` - Listar todos os livros
- `GET /livros/{id}` - Obter livro específico
- `POST /livros/` - Criar novo livro
- `PUT /livros/{id}` - Atualizar livro completo
- `PATCH /livros/{id}` - Atualizar livro parcial
- `DELETE /livros/{id}` - Excluir livro

### Categorias

- `GET /categorias/` - Listar todas as categorias
- `GET /categorias/{id}` - Obter categoria específica
- `POST /categorias/` - Criar nova categoria
- `PUT /categorias/{id}` - Atualizar categoria completo
- `PATCH /categorias/{id}` - Atualizar categoria parcial
- `DELETE /categorias/{id}` - Excluir categoria

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Pytest**
- **Uvicorn**

---

## 📦 Instalação e Execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/lfalcaolopes/livros_api.git
   cd livros_api
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o servidor:
   ```bash
   python -m uvicorn main:app --reload
   ```

Acesse em:

- API: [http://localhost:8000](http://localhost:8000)
- Documentação: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testes

- Executar testes:
  ```bash
  python -m pytest
  ```

---
