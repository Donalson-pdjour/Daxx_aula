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

    preco = Column(Float, nullable=True)

    id_categoria = Column(
        Integer,
        ForeignKey("tipos_categoria.id"),
        nullable=True,
    )

    quantidade = Column(Integer, nullable=True)

    descricao = Column(String(500), nullable=True)

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
            "disponivel": self.disponivel,
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
            "entrada": self.entrada,
            "saida": self.saida,
            "hora_entrada": self.hora_entrada,
            "hora_saida": self.hora_saida,
            "data_entrada": self.data_entrada.isoformat() if self.data_entrada else None,
            "data_saida": self.data_saida.isoformat() if self.data_saida else None,
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