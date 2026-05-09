"""
Regras de negócio e acesso ao banco (sessão + consultas).
Nas rotas só chamamos estas funções e devolvemos JSON — fica mais fácil de explicar.
"""

from sqlalchemy import select

from database import SessionLocal
from models import Produto


def listar_produtos():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Produto).order_by(Produto.nome)).all()
        return [p.to_dict() for p in linhas]
    finally:
        session.close()


def _numero_positivo(valor, campo, tipo=float):
    """Valida se o valor é um número positivo"""
    if valor is None:
        return None
    try:
        num = tipo(valor)
        if num < 0:
            raise ValueError(f"O campo '{campo}' deve ser um número positivo.")
        return num
    except (ValueError, TypeError):
        raise ValueError(f"O campo '{campo}' deve ser um número válido.")


def _texto_obrigatorio(valor, campo):
    if valor is None or str(valor).strip() == "":
        raise ValueError(f"O campo '{campo}' é obrigatório.")
    return str(valor).strip()


def _texto_opcional(valor):
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None


def cadastrar_produto(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    codigo = _texto_opcional(dados.get("codigo"))
    categoria = _texto_opcional(dados.get("categoria"))
    preco = _numero_positivo(dados.get("preco"), "preco", float)
    quantidade = _numero_positivo(dados.get("quantidade"), "quantidade", int)
    descricao = _texto_opcional(dados.get("descricao"))



    session = SessionLocal()
    try:
        produto = Produto(
            nome=nome,
            codigo=codigo,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
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
    """Obtém um produto pelo ID"""
    session = SessionLocal()
    try:
        produto = session.get(Produto, produto_id)
        if not produto:
            raise ValueError(f"Produto com ID {produto_id} não encontrado.")
        return produto.to_dict()
    finally:
        session.close()


def atualizar_produto(produto_id, dados):
    """Atualiza um produto existente"""
    session = SessionLocal()
    try:
        produto = session.get(Produto, produto_id)
        if not produto:
            raise ValueError(f"Produto com ID {produto_id} não encontrado.")
        
        # Atualiza apenas os campos fornecidos
        if "nome" in dados:
            produto.nome = _texto_obrigatorio(dados["nome"], "nome")
        if "codigo" in dados:
            produto.codigo = _texto_opcional(dados["codigo"])
        if "categoria" in dados:
            produto.categoria = _texto_opcional(dados["categoria"])
        if "preco" in dados:
            produto.preco = _numero_positivo(dados["preco"], "preco", float)
        if "quantidade" in dados:
            produto.quantidade = _numero_positivo(dados["quantidade"], "quantidade", int)
        if "descricao" in dados:
            produto.descricao = _texto_opcional(dados["descricao"])
        if "disponivel" in dados:
            produto.disponivel = bool(dados["disponivel"])
        
        session.commit()
        session.refresh(produto)
        return produto.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def deletar_produto(produto_id):
    """Deleta um produto pelo ID"""
    session = SessionLocal()
    try:
        produto = session.get(Produto, produto_id)
        if not produto:
            raise ValueError(f"Produto com ID {produto_id} não encontrado.")
        
        session.delete(produto)
        session.commit()
        return {"mensagem": f"Produto {produto_id} deletado com sucesso."}
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
