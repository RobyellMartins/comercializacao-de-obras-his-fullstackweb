from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os
from .models import Base
import logging

logger = logging.getLogger(__name__)

# Configuração do banco de dados com fallback automático
DATABASE_URL = os.getenv('DATABASE_URL')
engine = None

def create_database_engine():
    """Cria engine do banco com fallback automático"""
    global engine
    
    if not DATABASE_URL:
        # Usar SQLite como padrão para desenvolvimento
        database_url = 'sqlite:///obras_his.db'
        logger.info("Usando SQLite como banco padrão")
    else:
        database_url = DATABASE_URL
    
    # Tentar PostgreSQL primeiro se configurado
    if database_url.startswith('postgresql'):
        try:
            logger.info("Tentando conectar ao PostgreSQL...")
            test_engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=10,
                max_overflow=20,
                echo=False
            )
            # Testar conexão
            with test_engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info("Conexão PostgreSQL estabelecida com sucesso")
            engine = test_engine
            return engine
            
        except Exception as e:
            logger.warning(f"Falha ao conectar PostgreSQL: {str(e)}")
            logger.info("Fazendo fallback para SQLite...")
            
            # Fallback para SQLite
            database_url = 'sqlite:///obras_his.db'
    
    # Configurar SQLite (padrão ou fallback)
    if database_url.startswith('sqlite'):
        logger.info("Configurando SQLite...")
        engine = create_engine(
            database_url,
            poolclass=StaticPool,
            connect_args={
                "check_same_thread": False,
                "timeout": 20
            },
            echo=False  # Mudar para True para debug SQL
        )
    else:
        # Outros bancos (MySQL, etc.)
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20,
            echo=False
        )
    
    return engine

# Inicializar engine
engine = create_database_engine()

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
