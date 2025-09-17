from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os
from .models import Base
import logging

logger = logging.getLogger(__name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Usar SQLite como padrão para desenvolvimento
    DATABASE_URL = 'sqlite:///obras_his.db'

# Configurações específicas para SQLite
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
            "timeout": 20
        },
        echo=False  # Mudar para True para debug SQL
    )
else:
    # Configurações para PostgreSQL ou outros bancos
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        raise

@contextmanager
def get_db() -> Session:
    """Context manager para obter uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Erro na transação do banco de dados: {str(e)}")
        raise
    finally:
        db.close()

def get_db_session():
    """Função para obter uma sessão do banco (para uso em dependency injection)"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise

# Função para criar dados iniciais (se necessário)
def create_initial_data():
    """Cria dados iniciais no banco de dados"""
    try:
        with get_db() as db:
            from .models import Construtora
            
            # Verificar se já existem construtoras
            existing_construtoras = db.query(Construtora).count()
            
            if existing_construtoras == 0:
                # Criar algumas construtoras de exemplo
                construtoras_exemplo = [
                    {
                        'nome': 'Construtora ABC Ltda',
                        'cnpj': '12.345.678/0001-90',
                        'telefone': '(61) 3333-4444',
                        'email': 'contato@construtorabc.com.br',
                        'endereco': 'SCS Quadra 1, Bloco A, Sala 101 - Brasília/DF'
                    },
                    {
                        'nome': 'Empreendimentos XYZ S.A.',
                        'cnpj': '98.765.432/0001-10',
                        'telefone': '(61) 2222-3333',
                        'email': 'info@empxyz.com.br',
                        'endereco': 'SGAN 601, Módulo F - Brasília/DF'
                    }
                ]
                
                for dados_construtora in construtoras_exemplo:
                    construtora = Construtora(**dados_construtora)
                    db.add(construtora)
                
                db.commit()
                logger.info("Dados iniciais criados com sucesso")
                
    except Exception as e:
        logger.error(f"Erro ao criar dados iniciais: {str(e)}")
        raise
