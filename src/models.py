from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Construtora(Base):
    __tablename__ = 'construtoras'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(18))
    telefone = Column(String(20))
    email = Column(String(255))
    endereco = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    empreendimentos = relationship("Empreendimento", back_populates="construtora")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Empreendimento(Base):
    __tablename__ = 'empreendimentos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    nome_empresa = Column(String(255), nullable=False)  # Nome da Empresa (separado da construtora)
    endereco = Column(Text)
    cep = Column(String(10), nullable=False)
    observacao = Column(Text)
    construtora_id = Column(Integer, ForeignKey('construtoras.id'), nullable=True)  # Agora opcional
    publicado_em = Column(DateTime)
    expira_em = Column(DateTime)
    status_publicacao = Column(String(20), default='aguardando')  # 'aguardando', 'publicado', 'expirado'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    construtora = relationship("Construtora", back_populates="empreendimentos")
    unidades = relationship("Unidade", back_populates="empreendimento", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'nome_empresa': self.nome_empresa,
            'endereco': self.endereco,
            'cep': self.cep,
            'observacao': self.observacao,
            'construtora_id': self.construtora_id,
            'construtora_nome': self.construtora.nome if self.construtora else None,
            'publicado_em': self.publicado_em.isoformat() if self.publicado_em else None,
            'expira_em': self.expira_em.isoformat() if self.expira_em else None,
            'status_publicacao': self.status_publicacao,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Unidade(Base):
    __tablename__ = 'unidades'

    id = Column(Integer, primary_key=True)
    numero_unidade = Column(String(50), nullable=False)
    empreendimento_id = Column(Integer, ForeignKey('empreendimentos.id'), nullable=False)
    tamanho_m2 = Column(Float)
    preco_venda = Column(Float)
    mecanismo_pagamento = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    empreendimento = relationship("Empreendimento", back_populates="unidades")

    def to_dict(self):
        return {
            'id': self.id,
            'numero_unidade': self.numero_unidade,
            'empreendimento_id': self.empreendimento_id,
            'tamanho_m2': self.tamanho_m2,
            'preco_venda': self.preco_venda,
            'mecanismo_pagamento': self.mecanismo_pagamento,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
