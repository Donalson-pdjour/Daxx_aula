"""
Script didático: DDL (create/drop tables) + DML (inserts)
com sessão explícita.

Execute na raiz do projeto:
python setup_database.py
"""

from sqlalchemy import select

from database import Base, SessionLocal, engine
import models  # noqa: F401 -> registra tabelas no metadata


def populate_database():
    print("Limpando e criando tabelas...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        print("Inserindo tipos de categoria...")

        tipos_categoria = [
            models.Tipos_categoria(nome="Eletrônicos"),
            models.Tipos_categoria(nome="Móveis"),
        ]

        session.add_all(tipos_categoria)
        session.flush()

        print("Inserindo produtos...")

        produtos = [
            models.Produto(
                nome="Notebook",
                codigo="NB-001",
                id_categoria=tipos_categoria[0].id,
                preco=3500.00,
                quantidade=10,
                descricao="Notebook Dell Inspiron",
            ),
            models.Produto(
                nome="Mouse",
                codigo="MO-001",
                id_categoria=tipos_categoria[0].id,
                preco=150.00,
                quantidade=50,
                descricao="Mouse Óptico Logitech",
            ),
        ]

        session.add_all(produtos)
        session.flush()

        print("Inserindo funcionários...")

        funcionarios = [
            models.Funcionarios(
                nome="João",
                email="joao@example.com",
                cargo="Vendedor",
            ),
            models.Funcionarios(
                nome="Maria",
                email="maria@example.com",
                cargo="Gerente",
            ),
        ]

        funcionarios[0].set_password("senha123")
        funcionarios[1].set_password("senha456")

        session.add_all(funcionarios)
        session.flush()

        session.commit()

        print("\nSucesso! Commit concluído.")

        total_produtos = len(
            session.scalars(select(models.Produto)).all()
        )

        print(f"- Produtos cadastrados: {total_produtos}")

    except Exception as erro:
        print(f"Ocorreu um erro: {erro}")

        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    populate_database()