from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..db_sql import get_db
from ..models import Obra, Empreendimento
from ..schemas import ObraSchema
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

obras_bp = Blueprint("obras", __name__, url_prefix="/api/obras")

obra_schema = ObraSchema()
obras_schema = ObraSchema(many=True)

@obras_bp.route("", methods=["GET"])
def listar_obras():
    """Lista todas as obras com filtros opcionais"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        filtros = {
            'empreendimento_id': request.args.get('empreendimento_id'),
            'nome': request.args.get('nome'),
            'status': request.args.get('status'),
            'somente_publicadas': request.args.get('somente_publicadas') == '1'
        }
        
        # Remover filtros vazios
        filtros = {k: v for k, v in filtros.items() if v is not None and v != ''}
        
        with get_db() as db:
            query = db.query(Obra).join(Empreendimento, isouter=True)
            
            if filtros.get('somente_publicadas'):
                query = query.filter(
                    Obra.publicado_em.isnot(None),
                    Obra.expira_em > datetime.utcnow()
                )
            if filtros.get('empreendimento_id'):
                query = query.filter(Obra.empreendimento_id == filtros['empreendimento_id'])
            if filtros.get('nome'):
                query = query.filter(Obra.nome.like(f"%{filtros['nome']}%"))
            if filtros.get('status'):
                query = query.filter(Obra.status == filtros['status'])
            
            obras = query.order_by(Obra.id.desc()).all()
            return jsonify([obra.to_dict() for obra in obras]), 200
            
    except Exception as e:
        logger.error(f"Erro ao listar obras: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@obras_bp.route("/<int:obra_id>", methods=["GET"])
def buscar_obra(obra_id):
    """Busca uma obra pelo ID"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            obra = db.query(Obra).filter(Obra.id == obra_id).first()
            
            if not obra:
                return jsonify({"message": "Obra não encontrada"}), 404
                
            return jsonify(obra.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao buscar obra {obra_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@obras_bp.route("", methods=["POST"])
def criar_obra():
    """Cria uma nova obra"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        json_data = request.get_json()
        if not json_data:
            return jsonify(error="Nenhum dado JSON enviado"), 400

        try:
            data = obra_schema.load(json_data)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        with get_db() as db:
            # Verificar se o empreendimento existe
            empreendimento = db.query(Empreendimento).filter(
                Empreendimento.id == data['empreendimento_id']
            ).first()
            
            if not empreendimento:
                return jsonify(error="Empreendimento não encontrado"), 404
            
            obra = Obra(**data)
            db.add(obra)
            db.flush()
            db.refresh(obra)
            
            return jsonify(obra.to_dict()), 201
            
    except Exception as e:
        logger.error(f"Erro ao criar obra: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@obras_bp.route("/<int:obra_id>", methods=["PUT"])
def atualizar_obra(obra_id):
    """Atualiza uma obra existente"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        try:
            data = obra_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        with get_db() as db:
            obra = db.query(Obra).filter(Obra.id == obra_id).first()
            
            if not obra:
                return jsonify({"message": "Obra não encontrada"}), 404
            
            # Atualizar campos
            for campo, valor in data.items():
                setattr(obra, campo, valor)
            
            obra.updated_at = datetime.utcnow()
            db.flush()
            db.refresh(obra)
            
            return jsonify(obra.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao atualizar obra {obra_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@obras_bp.route("/<int:obra_id>", methods=["DELETE"])
def deletar_obra(obra_id):
    """Deleta uma obra"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            obra = db.query(Obra).filter(Obra.id == obra_id).first()
            
            if not obra:
                return jsonify({"message": "Obra não encontrada"}), 404
            
            db.delete(obra)
            
            return jsonify({"message": "Obra deletada com sucesso"}), 204
            
    except Exception as e:
        logger.error(f"Erro ao deletar obra {obra_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@obras_bp.route("/<int:obra_id>/publicar", methods=["POST"])
def publicar_obra(obra_id):
    """Publica uma obra"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            obra = db.query(Obra).filter(Obra.id == obra_id).first()
            
            if not obra:
                return jsonify({"message": "Obra não encontrada"}), 404
            
            now = datetime.utcnow()
            obra.publicado_em = now
            obra.expira_em = now + timedelta(days=30)
            
            db.flush()
            db.refresh(obra)
            
            return jsonify({
                "id": obra.id,
                "publicado_em": obra.publicado_em.isoformat(),
                "expira_em": obra.expira_em.isoformat(),
            }), 200
            
    except Exception as e:
        logger.error(f"Erro ao publicar obra {obra_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@obras_bp.route("/<int:obra_id>/progresso", methods=["PUT"])
def atualizar_progresso(obra_id):
    """Atualiza o progresso de uma obra"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        json_data = request.get_json()
        if not json_data or 'percentual_concluido' not in json_data:
            return jsonify(error="Percentual de conclusão é obrigatório"), 400
        
        percentual = json_data['percentual_concluido']
        if not isinstance(percentual, (int, float)) or percentual < 0 or percentual > 100:
            return jsonify(error="Percentual deve ser um número entre 0 e 100"), 400
        
        with get_db() as db:
            obra = db.query(Obra).filter(Obra.id == obra_id).first()
            
            if not obra:
                return jsonify({"message": "Obra não encontrada"}), 404
            
            obra.percentual_concluido = percentual
            obra.updated_at = datetime.utcnow()
            
            # Atualizar status baseado no percentual
            if percentual == 0:
                obra.status = "Não iniciada"
            elif percentual < 100:
                obra.status = "Em andamento"
            else:
                obra.status = "Concluída"
                if not obra.data_fim_real:
                    obra.data_fim_real = datetime.utcnow()
            
            db.flush()
            db.refresh(obra)
            
            return jsonify(obra.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao atualizar progresso da obra {obra_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
