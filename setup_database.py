"""
Script didático: DDL (create/drop tables) + DML (inserts) com sessão explícita.
Execute na raiz do projeto: python setup_database.py
"""

from sqlalchemy import select

from database import Base, SessionLocal, engine
import models  # noqa: F401 — registra tabelas no metadata


def populate_database():
    print("Limpando e criando tabelas...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        print("Inserindo produto...")
        produto = [
            models.Produto(nome="Notebook", codigo="NB-001", categoria="Eletrônicos", preco=3500.00, quantidade=10, descricao="Notebook Dell Inspiron"),  # imagem removida
            models.Produto(nome="Mouse", codigo="MO-001", categoria="Eletrônicos", preco=150.00, quantidade=50, descricao="Mouse Óptico Logitech"),  # imagem removida
        ]
        session.add_all(produto)
        session.flush()

        print("Inserindo tipos_categoria...")
        tipos_categoria = [
            models.Tipos_categoria(nome="Eletrônicos"),
            models.Tipos_categoria(nome="Móveis"),
        ]
        session.add_all(tipos_categoria)
        session.flush()

        print("Inserindo funcionarios...")
        funcionarios = [
            models.Funcionarios(nome="João", email="joao@example.com", senha="senha123", cargo="Vendedor"),
            models.Funcionarios(nome="Maria", email="maria@example.com", senha="senha456", cargo="Gerente"),
        ]
        session.add_all(funcionarios)
        session.flush()
        

        session.commit()
        print("\nSucesso! Commit concluído.")

        np = len(session.scalars(select(models.Produto)).all())
        print(f"- Produtos: {np}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    populate_database()
