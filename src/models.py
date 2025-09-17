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
    endereco = Column(Text)
    cidade = Column(String(100))
    estado = Column(String(2))
    cep = Column(String(10))
    tipo = Column(String(100))
    status = Column(String(50), default='Em planejamento')
    valor_total = Column(Float)
    unidades = Column(Integer)
    construtora_id = Column(Integer, ForeignKey('construtoras.id'))
    publicado_em = Column(DateTime)
    expira_em = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    construtora = relationship("Construtora", back_populates="empreendimentos")
    obras = relationship("Obra", back_populates="empreendimento")
    unidades_habitacionais = relationship("Unidade", back_populates="empreendimento")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'tipo': self.tipo,
            'status': self.status,
            'valor_total': self.valor_total,
            'unidades': self.unidades,
            'construtora_id': self.construtora_id,
            'construtora_nome': self.construtora.nome if self.construtora else None,
            'publicado_em': self.publicado_em.isoformat() if self.publicado_em else None,
            'expira_em': self.expira_em.isoformat() if self.expira_em else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Obra(Base):
    __tablename__ = 'obras'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    empreendimento_id = Column(Integer, ForeignKey('empreendimentos.id'))
    status = Column(String(50), default='Não iniciada')
    data_inicio = Column(DateTime)
    data_fim_prevista = Column(DateTime)
    data_fim_real = Column(DateTime)
    valor_orcado = Column(Float)
    valor_executado = Column(Float)
    percentual_concluido = Column(Float, default=0.0)
    publicado_em = Column(DateTime)
    expira_em = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    empreendimento = relationship("Empreendimento", back_populates="obras")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'empreendimento_id': self.empreendimento_id,
            'status': self.status,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim_prevista': self.data_fim_prevista.isoformat() if self.data_fim_prevista else None,
            'data_fim_real': self.data_fim_real.isoformat() if self.data_fim_real else None,
            'valor_orcado': self.valor_orcado,
            'valor_executado': self.valor_executado,
            'percentual_concluido': self.percentual_concluido,
            'publicado_em': self.publicado_em.isoformat() if self.publicado_em else None,
            'expira_em': self.expira_em.isoformat() if self.expira_em else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Unidade(Base):
    __tablename__ = 'unidades'
    
    id = Column(Integer, primary_key=True)
    numero_unidade = Column(String(50), nullable=False)
    empreendimento_id = Column(Integer, ForeignKey('empreendimentos.id'))
    tipo = Column(String(50))  # Apartamento, Casa, etc.
    area_m2 = Column(Float)
    quartos = Column(Integer)
    banheiros = Column(Integer)
    vagas_garagem = Column(Integer)
    preco_venda = Column(Float)
    status = Column(String(50), default='Disponível')  # Disponível, Vendida, Reservada
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    empreendimento = relationship("Empreendimento", back_populates="unidades_habitacionais")
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_unidade': self.numero_unidade,
            'empreendimento_id': self.empreendimento_id,
            'tipo': self.tipo,
            'area_m2': self.area_m2,
            'quartos': self.quartos,
            'banheiros': self.banheiros,
            'vagas_garagem': self.vagas_garagem,
            'preco_venda': self.preco_venda,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
