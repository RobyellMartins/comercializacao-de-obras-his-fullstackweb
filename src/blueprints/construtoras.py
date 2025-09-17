from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..db_sql import get_db
from ..models import Construtora
from ..schemas import ConstrutorSchema
import logging

logger = logging.getLogger(__name__)

construtoras_bp = Blueprint("construtoras", __name__, url_prefix="/api/construtoras")

construtora_schema = ConstrutorSchema()
construtoras_schema = ConstrutorSchema(many=True)

@construtoras_bp.route("", methods=["GET"])
def listar_construtoras():
    """Lista todas as construtoras"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            construtoras = db.query(Construtora).order_by(Construtora.nome).all()
            return jsonify([c.to_dict() for c in construtoras]), 200
            
    except Exception as e:
        logger.error(f"Erro ao listar construtoras: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@construtoras_bp.route("/<int:construtora_id>", methods=["GET"])
def buscar_construtora(construtora_id):
    """Busca uma construtora pelo ID"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            construtora = db.query(Construtora).filter(Construtora.id == construtora_id).first()
            
            if not construtora:
                return jsonify({"message": "Construtora não encontrada"}), 404
                
            return jsonify(construtora.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao buscar construtora {construtora_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@construtoras_bp.route("", methods=["POST"])
def criar_construtora():
    """Cria uma nova construtora"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        json_data = request.get_json()
        if not json_data:
            return jsonify(error="Nenhum dado JSON enviado"), 400

        try:
            data = construtora_schema.load(json_data)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        with get_db() as db:
            construtora = Construtora(**data)
            db.add(construtora)
            db.flush()
            db.refresh(construtora)
            
            return jsonify(construtora.to_dict()), 201
            
    except Exception as e:
        logger.error(f"Erro ao criar construtora: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@construtoras_bp.route("/<int:construtora_id>", methods=["PUT"])
def atualizar_construtora(construtora_id):
    """Atualiza uma construtora existente"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        try:
            data = construtora_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        with get_db() as db:
            construtora = db.query(Construtora).filter(Construtora.id == construtora_id).first()
            
            if not construtora:
                return jsonify({"message": "Construtora não encontrada"}), 404
            
            # Atualizar campos
            for campo, valor in data.items():
                setattr(construtora, campo, valor)
            
            db.flush()
            db.refresh(construtora)
            
            return jsonify(construtora.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao atualizar construtora {construtora_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@construtoras_bp.route("/<int:construtora_id>", methods=["DELETE"])
def deletar_construtora(construtora_id):
    """Deleta uma construtora"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            construtora = db.query(Construtora).filter(Construtora.id == construtora_id).first()
            
            if not construtora:
                return jsonify({"message": "Construtora não encontrada"}), 404
            
            db.delete(construtora)
            
            return jsonify({"message": "Construtora deletada com sucesso"}), 204
            
    except Exception as e:
        logger.error(f"Erro ao deletar construtora {construtora_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
