from sqlalchemy.orm import Session
from ..models import Empreendimento, Construtora, Unidade
from ..db_sql import get_db
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EmpreendimentosRepositorySQL:
    def __init__(self, db: Session = None):
        self.db = db
    
    def listar_empreendimentos(self, filtros=None) -> List[Dict]:
        """Lista empreendimentos com filtros opcionais"""
        try:
            with get_db() as db:
                query = db.query(Empreendimento).join(Construtora, isouter=True)

                if filtros:
                    if filtros.get('somente_publicadas'):
                        query = query.filter(
                            Empreendimento.publicado_em.isnot(None),
                            Empreendimento.expira_em > datetime.utcnow()
                        )
                    if filtros.get('construtora_id'):
                        query = query.filter(Empreendimento.construtora_id == filtros['construtora_id'])
                    if filtros.get('nome'):
                        query = query.filter(Empreendimento.nome.like(f"%{filtros['nome']}%"))
                    if filtros.get('cep'):
                        query = query.filter(Empreendimento.cep.like(f"%{filtros['cep']}%"))
                    if filtros.get('data_inicio'):
                        query = query.filter(Empreendimento.created_at >= filtros['data_inicio'])
                    if filtros.get('data_fim'):
                        query = query.filter(Empreendimento.created_at <= filtros['data_fim'])

                empreendimentos = query.order_by(Empreendimento.id.desc()).all()
                return [emp.to_dict() for emp in empreendimentos]

        except Exception as e:
            logger.error(f"Erro ao listar empreendimentos: {str(e)}")
            raise
    
    def listar_todos(self) -> List[Dict]:
        """Lista todos os empreendimentos"""
        return self.listar_empreendimentos()
    
    def obter_por_id(self, id: int) -> Optional[Dict]:
        """Obtém um empreendimento por ID"""
        try:
            with get_db() as db:
                empreendimento = db.query(Empreendimento).filter(Empreendimento.id == id).first()
                return empreendimento.to_dict() if empreendimento else None
                
        except Exception as e:
            logger.error(f"Erro ao obter empreendimento {id}: {str(e)}")
            raise
    
    def buscar_empreendimento(self, id: int) -> Optional[Empreendimento]:
        """Busca um empreendimento por ID (retorna objeto SQLAlchemy)"""
        try:
            with get_db() as db:
                return db.query(Empreendimento).filter(Empreendimento.id == id).first()
                
        except Exception as e:
            logger.error(f"Erro ao buscar empreendimento {id}: {str(e)}")
            raise
    
    def buscar_ou_criar_construtora(self, nome_construtora: str, db: Session) -> Construtora:
        """Busca ou cria uma construtora"""
        construtora = db.query(Construtora).filter(Construtora.nome == nome_construtora).first()
        
        if not construtora:
            construtora = Construtora(nome=nome_construtora)
            db.add(construtora)
            db.flush()  # Para obter o ID sem fazer commit
        
        return construtora
    
    def criar(self, dados: Dict) -> Dict:
        """Cria um novo empreendimento"""
        try:
            with get_db() as db:
                # Buscar ou criar construtora se fornecida
                construtora_id = dados.get('construtora_id')
                if not construtora_id and dados.get('empresa'):
                    construtora = self.buscar_ou_criar_construtora(dados['empresa'], db)
                    construtora_id = construtora.id
                
                empreendimento = Empreendimento(
                    nome=dados['nome'],
                    nome_empresa=dados.get('nome_empresa', dados['nome']),  # Usar nome se nome_empresa não fornecido
                    endereco=dados.get('endereco'),
                    cep=dados['cep'],
                    observacao=dados.get('observacao'),
                    construtora_id=construtora_id,
                    status_publicacao=dados.get('status_publicacao', 'aguardando')
                )
                
                db.add(empreendimento)
                db.flush()
                db.refresh(empreendimento)
                
                return empreendimento.to_dict()
                
        except Exception as e:
            logger.error(f"Erro ao criar empreendimento: {str(e)}")
            raise
    
    def atualizar(self, id: int, dados: Dict) -> Optional[Dict]:
        """Atualiza um empreendimento existente"""
        try:
            with get_db() as db:
                empreendimento = db.query(Empreendimento).filter(Empreendimento.id == id).first()
                
                if not empreendimento:
                    return None
                
                # Atualizar campos
                campos_permitidos = ['nome', 'nome_empresa', 'endereco', 'cep', 'observacao', 'status_publicacao', 'publicado_em', 'expira_em']
                
                for campo in campos_permitidos:
                    if campo in dados:
                        setattr(empreendimento, campo, dados[campo])
                
                # Atualizar construtora se fornecida
                if dados.get('empresa'):
                    construtora = self.buscar_ou_criar_construtora(dados['empresa'], db)
                    empreendimento.construtora_id = construtora.id
                elif dados.get('construtora_id'):
                    empreendimento.construtora_id = dados['construtora_id']
                
                empreendimento.updated_at = datetime.utcnow()
                db.flush()
                db.refresh(empreendimento)
                
                return empreendimento.to_dict()
                
        except Exception as e:
            logger.error(f"Erro ao atualizar empreendimento {id}: {str(e)}")
            raise
    
    def deletar(self, id: int) -> bool:
        """Deleta um empreendimento"""
        try:
            with get_db() as db:
                empreendimento = db.query(Empreendimento).filter(Empreendimento.id == id).first()
                
                if empreendimento:
                    db.delete(empreendimento)
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Erro ao deletar empreendimento {id}: {str(e)}")
            raise
    
    def publicar_empreendimento(self, id: int) -> Optional[Dict]:
        """Publica um empreendimento"""
        try:
            with get_db() as db:
                empreendimento = db.query(Empreendimento).filter(Empreendimento.id == id).first()
                
                if not empreendimento:
                    return None
                
                now = datetime.utcnow()
                empreendimento.publicado_em = now
                empreendimento.expira_em = now + timedelta(days=30)
                
                db.flush()
                db.refresh(empreendimento)
                
                return empreendimento.to_dict()
                
        except Exception as e:
            logger.error(f"Erro ao publicar empreendimento {id}: {str(e)}")
            raise
    
    def buscar_por_nome(self, nome: str) -> List[Dict]:
        """Busca empreendimentos por nome"""
        filtros = {'nome': nome}
        return self.listar_empreendimentos(filtros)
    
    def buscar_por_cep(self, cep: str) -> List[Dict]:
        """Busca empreendimentos por CEP"""
        filtros = {'cep': cep}
        return self.listar_empreendimentos(filtros)

    def criar_unidade(self, dados: Dict) -> Dict:
        """Cria uma nova unidade"""
        try:
            with get_db() as db:
                unidade = Unidade(
                    empreendimento_id=dados['empreendimento_id'],
                    numero_unidade=dados['numero_unidade'],
                    tamanho_m2=dados.get('tamanho_m2'),
                    preco_venda=dados.get('preco_venda'),
                    mecanismo_pagamento=dados.get('mecanismo_pagamento', 'outros')
                )

                db.add(unidade)
                db.flush()
                db.refresh(unidade)

                return unidade.to_dict()

        except Exception as e:
            logger.error(f"Erro ao criar unidade: {str(e)}")
            raise
