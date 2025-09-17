from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..db_sql import get_db
from ..models import Unidade, Empreendimento
from ..schemas import UnidadeSchema
import logging

logger = logging.getLogger(__name__)

unidades_bp = Blueprint("unidades", __name__, url_prefix="/api/unidades")

unidade_schema = UnidadeSchema()
unidades_schema = UnidadeSchema(many=True)

@unidades_bp.route("", methods=["GET"])
def listar_unidades():
    """Lista todas as unidades com filtros opcionais"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        empreendimento_id = request.args.get('empreendimento_id')
        status = request.args.get('status')
        tipo = request.args.get('tipo')
        
        with get_db() as db:
            query = db.query(Unidade).join(Empreendimento, isouter=True)
            
            if empreendimento_id:
                query = query.filter(Unidade.empreendimento_id == empreendimento_id)
            if status:
                query = query.filter(Unidade.status == status)
            if tipo:
                query = query.filter(Unidade.tipo == tipo)
            
            unidades = query.order_by(Unidade.numero_unidade).all()
            return jsonify([unidade.to_dict() for unidade in unidades]), 200
            
    except Exception as e:
        logger.error(f"Erro ao listar unidades: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@unidades_bp.route("/<int:unidade_id>", methods=["GET"])
def buscar_unidade(unidade_id):
    """Busca uma unidade pelo ID"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
            
            if not unidade:
                return jsonify({"message": "Unidade não encontrada"}), 404
                
            return jsonify(unidade.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao buscar unidade {unidade_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@unidades_bp.route("", methods=["POST"])
def criar_unidade():
    """Cria uma nova unidade"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        json_data = request.get_json()
        if not json_data:
            return jsonify(error="Nenhum dado JSON enviado"), 400

        try:
            data = unidade_schema.load(json_data)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        with get_db() as db:
            # Verificar se o empreendimento existe
            empreendimento = db.query(Empreendimento).filter(
                Empreendimento.id == data['empreendimento_id']
            ).first()
            
            if not empreendimento:
                return jsonify(error="Empreendimento não encontrado"), 404
            
            # Verificar se já existe uma unidade com o mesmo número no empreendimento
            unidade_existente = db.query(Unidade).filter(
                Unidade.empreendimento_id == data['empreendimento_id'],
                Unidade.numero_unidade == data['numero_unidade']
            ).first()
            
            if unidade_existente:
                return jsonify(error="Já existe uma unidade com este número neste empreendimento"), 400
            
            unidade = Unidade(**data)
            db.add(unidade)
            db.flush()
            db.refresh(unidade)
            
            return jsonify(unidade.to_dict()), 201
            
    except Exception as e:
        logger.error(f"Erro ao criar unidade: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@unidades_bp.route("/<int:unidade_id>", methods=["PUT"])
def atualizar_unidade(unidade_id):
    """Atualiza uma unidade existente"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        try:
            data = unidade_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        with get_db() as db:
            unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
            
            if not unidade:
                return jsonify({"message": "Unidade não encontrada"}), 404
            
            # Se está alterando o número da unidade, verificar se não existe outra com o mesmo número
            if 'numero_unidade' in data and data['numero_unidade'] != unidade.numero_unidade:
                unidade_existente = db.query(Unidade).filter(
                    Unidade.empreendimento_id == unidade.empreendimento_id,
                    Unidade.numero_unidade == data['numero_unidade'],
                    Unidade.id != unidade_id
                ).first()
                
                if unidade_existente:
                    return jsonify(error="Já existe uma unidade com este número neste empreendimento"), 400
            
            # Atualizar campos
            for campo, valor in data.items():
                setattr(unidade, campo, valor)
            
            db.flush()
            db.refresh(unidade)
            
            return jsonify(unidade.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao atualizar unidade {unidade_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@unidades_bp.route("/<int:unidade_id>", methods=["DELETE"])
def deletar_unidade(unidade_id):
    """Deleta uma unidade"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
            
            if not unidade:
                return jsonify({"message": "Unidade não encontrada"}), 404
            
            db.delete(unidade)
            
            return jsonify({"message": "Unidade deletada com sucesso"}), 204
            
    except Exception as e:
        logger.error(f"Erro ao deletar unidade {unidade_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@unidades_bp.route("/<int:unidade_id>/status", methods=["PUT"])
def atualizar_status_unidade(unidade_id):
    """Atualiza o status de uma unidade"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        json_data = request.get_json()
        if not json_data or 'status' not in json_data:
            return jsonify(error="Status é obrigatório"), 400
        
        status = json_data['status']
        status_validos = ['Disponível', 'Reservada', 'Vendida', 'Indisponível']
        
        if status not in status_validos:
            return jsonify(error=f"Status deve ser um dos seguintes: {', '.join(status_validos)}"), 400
        
        with get_db() as db:
            unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
            
            if not unidade:
                return jsonify({"message": "Unidade não encontrada"}), 404
            
            unidade.status = status
            db.flush()
            db.refresh(unidade)
            
            return jsonify(unidade.to_dict()), 200
            
    except Exception as e:
        logger.error(f"Erro ao atualizar status da unidade {unidade_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@unidades_bp.route("/empreendimento/<int:empreendimento_id>", methods=["GET"])
def listar_unidades_por_empreendimento(empreendimento_id):
    """Lista todas as unidades de um empreendimento específico"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        with get_db() as db:
            # Verificar se o empreendimento existe
            empreendimento = db.query(Empreendimento).filter(
                Empreendimento.id == empreendimento_id
            ).first()
            
            if not empreendimento:
                return jsonify({"message": "Empreendimento não encontrado"}), 404
            
            unidades = db.query(Unidade).filter(
                Unidade.empreendimento_id == empreendimento_id
            ).order_by(Unidade.numero_unidade).all()
            
            return jsonify([unidade.to_dict() for unidade in unidades]), 200
            
    except Exception as e:
        logger.error(f"Erro ao listar unidades do empreendimento {empreendimento_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
