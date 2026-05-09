import flask as fk
from sqlalchemy.exc import IntegrityError

from .servicos import (
    cadastrar_produto,
    listar_produtos,
    listar_tipos_categoria,
    obter_produto,
    atualizar_produto,
    deletar_produto,
)

bp = fk.Blueprint("api", __name__, url_prefix="/api")


def _erro(mensagem, status=400):
    return fk.jsonify({"erro": mensagem}), status


@bp.get("/produtos")
def produtos():
    return fk.jsonify(listar_produtos())


@bp.get("/tipos_categoria")
def tipos_categoria():
    return fk.jsonify(listar_tipos_categoria())


@bp.get("/produtos/<int:produto_id>")
def obter_produto_rota(produto_id):
    try:
        return fk.jsonify(obter_produto(produto_id))
    except ValueError as exc:
        return _erro(str(exc), 404)


@bp.post("/produtos")
def criar_produto():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_produto(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Já existe um produto com este código.", 409)


@bp.put("/produtos/<int:produto_id>")
def atualizar_produto_rota(produto_id):
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(atualizar_produto(produto_id, dados))

    except ValueError as exc:
        return _erro(str(exc), 404)


@bp.delete("/produtos/<int:produto_id>")
def deletar_produto_rota(produto_id):
    try:
        return fk.jsonify(deletar_produto(produto_id))

    except ValueError as exc:
        return _erro(str(exc), 404)


paginas = fk.Blueprint("paginas", __name__)


@paginas.get("/")
def home():
    return fk.render_template("index.html")