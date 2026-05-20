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
        nome="Notebook Dell Inspiron",
        codigo="NB-001",
        id_categoria=tipos_categoria[0].id,
        preco=3500.00,
        quantidade=10,
        descricao="Notebook Dell Inspiron 15 polegadas",
    ),
    models.Produto(
        nome="Mouse Logitech",
        codigo="MO-001",
        id_categoria=tipos_categoria[0].id,
        preco=150.00,
        quantidade=50,
        descricao="Mouse óptico Logitech USB",
    ),
    models.Produto(
        nome="Teclado Mecânico",
        codigo="TC-001",
        id_categoria=tipos_categoria[0].id,
        preco=280.00,
        quantidade=30,
        descricao="Teclado mecânico RGB",
    ),
    models.Produto(
        nome="Monitor LG 24",
        codigo="MN-001",
        id_categoria=tipos_categoria[0].id,
        preco=1200.00,
        quantidade=15,
        descricao='Monitor LG 24 polegadas Full HD',
    ),
    models.Produto(
        nome="Headset Gamer",
        codigo="HS-001",
        id_categoria=tipos_categoria[0].id,
        preco=320.00,
        quantidade=25,
        descricao="Headset gamer com microfone",
    ),
    models.Produto(
        nome="Impressora HP",
        codigo="IM-001",
        id_categoria=tipos_categoria[1].id,
        preco=950.00,
        quantidade=8,
        descricao="Impressora multifuncional HP",
    ),
    models.Produto(
        nome="Cadeira Escritório",
        codigo="CD-001",
        id_categoria=tipos_categoria[1].id,
        preco=780.00,
        quantidade=12,
        descricao="Cadeira ergonômica para escritório",
    ),
    models.Produto(
        nome="Mesa Escritório",
        codigo="MS-001",
        id_categoria=tipos_categoria[1].id,
        preco=650.00,
        quantidade=7,
        descricao="Mesa de escritório em MDF",
    ),
    models.Produto(
        nome="HD Externo 1TB",
        codigo="HD-001",
        id_categoria=tipos_categoria[0].id,
        preco=420.00,
        quantidade=20,
        descricao="HD externo portátil 1TB",
    ),
    models.Produto(
        nome="Pendrive 64GB",
        codigo="PD-001",
        id_categoria=tipos_categoria[0].id,
        preco=80.00,
        quantidade=100,
        descricao="Pendrive USB 64GB",
    ),
    models.Produto(
        nome="Roteador TP-Link",
        codigo="RT-001",
        id_categoria=tipos_categoria[0].id,
        preco=260.00,
        quantidade=18,
        descricao="Roteador Wi-Fi TP-Link",
    ),
    models.Produto(
        nome="Switch 8 Portas",
        codigo="SW-001",
        id_categoria=tipos_categoria[0].id,
        preco=340.00,
        quantidade=10,
        descricao="Switch de rede 8 portas",
    ),
    models.Produto(
        nome="Cabo HDMI",
        codigo="CB-001",
        id_categoria=tipos_categoria[0].id,
        preco=45.00,
        quantidade=80,
        descricao="Cabo HDMI 2 metros",
    ),
    models.Produto(
        nome="Estabilizador",
        codigo="ES-001",
        id_categoria=tipos_categoria[0].id,
        preco=390.00,
        quantidade=9,
        descricao="Estabilizador bivolt",
    ),
    models.Produto(
        nome="Nobreak Intelbras",
        codigo="NO-001",
        id_categoria=tipos_categoria[0].id,
        preco=890.00,
        quantidade=6,
        descricao="Nobreak Intelbras 1200VA",
    ),
    models.Produto(
        nome="Scanner Epson",
        codigo="SC-001",
        id_categoria=tipos_categoria[1].id,
        preco=1100.00,
        quantidade=5,
        descricao="Scanner Epson profissional",
    ),
    models.Produto(
        nome="Webcam Full HD",
        codigo="WB-001",
        id_categoria=tipos_categoria[0].id,
        preco=210.00,
        quantidade=22,
        descricao="Webcam Full HD USB",
    ),
    models.Produto(
        nome="Projetor Epson",
        codigo="PJ-001",
        id_categoria=tipos_categoria[1].id,
        preco=2800.00,
        quantidade=4,
        descricao="Projetor Epson multimídia",
    ),
    models.Produto(
        nome="Tablet Samsung",
        codigo="TB-001",
        id_categoria=tipos_categoria[0].id,
        preco=1900.00,
        quantidade=11,
        descricao="Tablet Samsung Galaxy",
    ),
    models.Produto(
        nome="Smartphone Motorola",
        codigo="SP-001",
        id_categoria=tipos_categoria[0].id,
        preco=1700.00,
        quantidade=14,
        descricao="Smartphone Motorola Android",
    ),

        ]

        session.add_all(produtos)
        session.flush()

        print("Inserindo funcionários...")

        funcionarios = [
    models.Funcionarios(
        nome="João Silva",
        email="joao.silva@example.com",
        cargo="Vendedor",
    ),
    models.Funcionarios(
        nome="Maria Oliveira",
        email="maria.oliveira@example.com",
        cargo="Gerente",
    ),
    models.Funcionarios(
        nome="Carlos Souza",
        email="carlos.souza@example.com",
        cargo="Administrador",
    ),
    models.Funcionarios(
        nome="Ana Lima",
        email="ana.lima@example.com",
        cargo="Caixa",
    ),
    models.Funcionarios(
        nome="Pedro Santos",
        email="pedro.santos@example.com",
        cargo="Estoquista",
    ),
    models.Funcionarios(
        nome="Juliana Costa",
        email="juliana.costa@example.com",
        cargo="RH",
    ),
    models.Funcionarios(
        nome="Lucas Pereira",
        email="lucas.pereira@example.com",
        cargo="Supervisor",
    ),
    models.Funcionarios(
        nome="Fernanda Alves",
        email="fernanda.alves@example.com",
        cargo="Vendedor",
    ),
    models.Funcionarios(
        nome="Ricardo Gomes",
        email="ricardo.gomes@example.com",
        cargo="Motorista",
    ),
    models.Funcionarios(
        nome="Patrícia Rocha",
        email="patricia.rocha@example.com",
        cargo="Financeiro",
    ),
    models.Funcionarios(
        nome="Gabriel Martins",
        email="gabriel.martins@example.com",
        cargo="Técnico",
    ),
    models.Funcionarios(
        nome="Larissa Ferreira",
        email="larissa.ferreira@example.com",
        cargo="Secretária",
    ),
    models.Funcionarios(
        nome="Bruno Carvalho",
        email="bruno.carvalho@example.com",
        cargo="Comprador",
    ),
    models.Funcionarios(
        nome="Camila Ribeiro",
        email="camila.ribeiro@example.com",
        cargo="Atendente",
    ),
    models.Funcionarios(
        nome="Felipe Barbosa",
        email="felipe.barbosa@example.com",
        cargo="Analista",
    ),
    models.Funcionarios(
        nome="Aline Mendes",
        email="aline.mendes@example.com",
        cargo="Coordenadora",
    ),
    models.Funcionarios(
        nome="Thiago Nunes",
        email="thiago.nunes@example.com",
        cargo="Auxiliar Administrativo",
    ),
    models.Funcionarios(
        nome="Vanessa Teixeira",
        email="vanessa.teixeira@example.com",
        cargo="Recepcionista",
    ),
    models.Funcionarios(
        nome="Eduardo Moraes",
        email="eduardo.moraes@example.com",
        cargo="Operador de Sistema",
    ),
    models.Funcionarios(
        nome="Beatriz Cardoso",
        email="beatriz.cardoso@example.com",
        cargo="Gerente de Estoque",
    ),
    models.Funcionarios(
        nome="Rafael Dias",
        email="rafael.dias@example.com",
        cargo="Analista de Marketing",
    ),

    ]
        for funcionario in funcionarios:
            funcionario.set_password("senha123")

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