"""
Regras de negócio e acesso ao banco (sessão + consultas).

Nas rotas, apenas chamamos estas funções e devolvemos JSON.
Isso deixa o código mais organizado e fácil de explicar.
"""

from sqlalchemy import select

from database import SessionLocal
from models import Produto, Tipos_categoria, Funcionarios


def listar_produtos():
    session = SessionLocal()

    try:
        linhas = session.scalars(
            select(Produto).order_by(Produto.nome)
        ).all()

        return [p.to_dict() for p in linhas]

    finally:
        session.close()


def listar_tipos_categoria():
    session = SessionLocal()

    try:
        linhas = session.scalars(
            select(Tipos_categoria).order_by(Tipos_categoria.nome)
        ).all()

        return [c.to_dict() for c in linhas]

    finally:
        session.close()


def listar_categorias():
    session = SessionLocal()

    try:
        linhas = session.scalars(
            select(Tipos_categoria).order_by(Tipos_categoria.nome)
        ).all()

        return [c.to_dict() for c in linhas]

    finally:
        session.close()


def listar_funcionarios():
    session = SessionLocal()

    try:
        linhas = session.scalars(
            select(Funcionarios).order_by(Funcionarios.nome)
        ).all()

        return [f.to_dict() for f in linhas]

    finally:
        session.close()


def cadastrar_categoria(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")

    session = SessionLocal()

    try:
        categoria = Tipos_categoria(nome=nome)
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria.to_dict()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def cadastrar_funcionario(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    email = _texto_obrigatorio(dados.get("email"), "email")
    cargo = _texto_obrigatorio(dados.get("cargo"), "cargo")
    senha = _texto_obrigatorio(dados.get("senha"), "senha")

    session = SessionLocal()

    try:
        funcionario = Funcionarios(
            nome=nome,
            email=email,
            cargo=cargo,
        )
        funcionario.set_password(senha)

        session.add(funcionario)
        session.commit()
        session.refresh(funcionario)

        return funcionario.to_dict()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def _numero_positivo(valor, campo, tipo=float):
    """Valida se o valor é um número positivo."""

    if valor is None:
        return None

    try:
        num = tipo(valor)

        if num < 0:
            raise ValueError(
                f"O campo '{campo}' deve ser um número positivo."
            )

        return num

    except (ValueError, TypeError):
        raise ValueError(
            f"O campo '{campo}' deve ser um número válido."
        )


def _texto_obrigatorio(valor, campo):
    """Valida campos de texto obrigatórios."""

    if valor is None or str(valor).strip() == "":
        raise ValueError(f"O campo '{campo}' é obrigatório.")

    return str(valor).strip()


def _texto_opcional(valor):
    """Trata campos de texto opcionais."""

    if valor is None:
        return None

    texto = str(valor).strip()

    return texto or None


def cadastrar_produto(dados):
    """Cadastra um novo produto."""

    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    codigo = _texto_obrigatorio(dados.get("codigo"), "codigo")
    id_categoria = dados.get("id_categoria")
    if id_categoria is not None and id_categoria != "":
        try:
            id_categoria = int(id_categoria)
        except (ValueError, TypeError):
            raise ValueError("O campo 'id_categoria' deve ser um número válido.")
    preco = _numero_positivo(dados.get("preco"), "preco", float)
    quantidade = _numero_positivo(
        dados.get("quantidade"),
        "quantidade",
        int,
    )
    status = dados.get("status")
    if status in ("ativo", "inativo"):
        disponivel = status == "ativo"
    elif status in (None, ""):
        disponivel = True
    else:
        raise ValueError("O campo 'status' deve ser 'ativo' ou 'inativo'.")
    descricao = _texto_opcional(dados.get("descricao"))
    imagem = _texto_opcional(dados.get("imagem"))

    session = SessionLocal()

    try:
        produto = Produto(
            nome=nome,
            codigo=codigo,
            id_categoria=id_categoria,
            preco=preco,
            quantidade=quantidade,
            imagem=imagem,
            disponivel=disponivel,
            descricao=descricao,
        )

        session.add(produto)
        session.commit()
        session.refresh(produto)

        return produto.to_dict()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def obter_produto(produto_id):
    """Obtém um produto pelo ID."""

    session = SessionLocal()

    try:
        produto = session.get(Produto, produto_id)

        if not produto:
            raise ValueError(
                f"Produto com ID {produto_id} não encontrado."
            )

        return produto.to_dict()

    finally:
        session.close()


def atualizar_produto(produto_id, dados):
    """Atualiza um produto existente."""

    session = SessionLocal()

    try:
        produto = session.get(Produto, produto_id)

        if not produto:
            raise ValueError(
                f"Produto com ID {produto_id} não encontrado."
            )

        # Atualiza apenas os campos enviados
        if "nome" in dados:
            produto.nome = _texto_obrigatorio(
                dados["nome"],
                "nome",
            )

        if "codigo" in dados:
            produto.codigo = _texto_opcional(
                dados["codigo"]
            )

        if "preco" in dados:
            produto.preco = _numero_positivo(
                dados["preco"],
                "preco",
                float,
            )

        if "quantidade" in dados:
            produto.quantidade = _numero_positivo(
                dados["quantidade"],
                "quantidade",
                int,
            )

        if "descricao" in dados:
            produto.descricao = _texto_opcional(
                dados["descricao"]
            )

        if "imagem" in dados:
            produto.imagem = _texto_opcional(
                dados["imagem"]
            )

        if "id_categoria" in dados:
            produto.id_categoria = (
                int(dados["id_categoria"])
                if dados["id_categoria"] not in (None, "")
                else None
            )
        if "disponivel" in dados:
            produto.disponivel = bool(
                dados["disponivel"]
            )

        if "status" in dados:
            if dados["status"] in ("ativo", "inativo"):
                produto.disponivel = dados["status"] == "ativo"
            elif dados["status"] not in (None, ""):
                raise ValueError("O campo 'status' deve ser 'ativo' ou 'inativo'.")

        if "entrada" in dados:
            produto.entrada = _numero_positivo(
                dados["entrada"],
                "entrada",
                int,
            ) or 0

        if "saida" in dados:
            produto.saida = _numero_positivo(
                dados["saida"],
                "saida",
                int,
            ) or 0

        if "hora_entrada" in dados:
            produto.hora_entrada = _texto_opcional(
                dados["hora_entrada"]
            )

        if "hora_saida" in dados:
            produto.hora_saida = _texto_opcional(
                dados["hora_saida"]
            )

        if "data_entrada" in dados:
            if dados["data_entrada"]:
                from datetime import datetime
                try:
                    produto.data_entrada = datetime.fromisoformat(
                        str(dados["data_entrada"]).replace("Z", "+00:00")
                    )
                except ValueError:
                    produto.data_entrada = None

        if "data_saida" in dados:
            if dados["data_saida"]:
                from datetime import datetime
                try:
                    produto.data_saida = datetime.fromisoformat(
                        str(dados["data_saida"]).replace("Z", "+00:00")
                    )
                except ValueError:
                    produto.data_saida = None

        session.commit()
        session.refresh(produto)

        return produto.to_dict()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def deletar_produto(produto_id):
    """Deleta um produto pelo ID."""

    session = SessionLocal()

    try:
        produto = session.get(Produto, produto_id)

        if not produto:
            raise ValueError(
                f"Produto com ID {produto_id} não encontrado."
            )

        session.delete(produto)
        session.commit()

        return {
            "mensagem": (
                f"Produto {produto_id} deletado com sucesso."
            )
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()