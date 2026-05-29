from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    codigo = Column(
        String(20),
        unique=True,
        nullable=False,
    )

    preco = Column(Float, nullable=False)
    id_categoria = Column(
        Integer,
        ForeignKey("tipos_categoria.id"),
        nullable=False,
    )

    quantidade = Column(Integer, nullable=False)
    descricao = Column(String(500), nullable=True)
    imagem = Column(String(500), nullable=True)
    disponivel = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.now,
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    valor_total = Column(Float, nullable=True)
    entrada = Column(Integer, default=0)
    saida = Column(Integer, default=0)
    hora_entrada = Column(String(8), nullable=True)
    hora_saida = Column(String(8), nullable=True)
    data_entrada = Column(DateTime, nullable=True)
    data_saida = Column(DateTime, nullable=True)

    # Relacionamento com Tipos_categoria
    tipo_categoria = relationship(
        "Tipos_categoria",
        back_populates="produtos",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "preco": self.preco,
            "id_categoria": self.id_categoria,
            "quantidade": self.quantidade,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "status": "ativo" if self.disponivel else "inativo",
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "valor_total": (
                self.preco * self.quantidade
                if self.preco is not None and self.quantidade is not None
                else None
            ),
            "categoria": (
                self.tipo_categoria.nome
                if self.tipo_categoria
                else None
            ),
            
            "movimentacao": (
                "entrada" if self.entrada > 0 else "saida" if self.saida > 0 else "nenhuma"
            )
        }
        

    def __repr__(self):
        return f"<Produto {self.id} {self.nome!r}>"


class Tipos_categoria(Base):
    __tablename__ = "tipos_categoria"

    id = Column(Integer, primary_key=True)

    nome = Column(
        String(120),
        nullable=False,
    )

    # Relacionamento com Produto
    produtos = relationship(
        "Produto",
        back_populates="tipo_categoria",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
        }

    def __repr__(self):
        return f"<Tipos_categoria {self.id} {self.nome!r}>"


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    acao = Column(String(50), nullable=False)
    data_hora = Column(DateTime, default=datetime.now, nullable=False)
    quantidade = Column(Integer, nullable=True)
    data_exclusao_agendada = Column(DateTime, nullable=True)

    produto = relationship("Produto")

    def __repr__(self):
        return f"<Movimentacao {self.id} Produto:{self.produto_id} {self.acao} em {self.data_hora}>"

class Funcionarios(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True)

    nome = Column(
        String(120),
        nullable=False,
    )

    email = Column(
        String(120),
        unique=True,
        nullable=False,
    )

    senha = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    cargo = Column(
        String(120),
        nullable=False,
    )

    def set_password(self, senha_plana):
        """Criptografa a senha antes de salvar."""

        self.senha = generate_password_hash(
            senha_plana
        )

    def check_password(self, senha_plana):
        """Verifica se a senha está correta."""

        return check_password_hash(
            self.senha,
            senha_plana,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "cargo": self.cargo,
        }

    def __repr__(self):
        return f"<Funcionarios {self.id} {self.nome!r}>"