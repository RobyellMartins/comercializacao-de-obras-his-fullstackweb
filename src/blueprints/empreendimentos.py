from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..db_sql import get_db
from ..repositories.empreendimentos_repo_sql import EmpreendimentosRepositorySQL
from ..schemas import EmpreendimentoSchema
from ..services.empreendimentos_service import EmpreendimentosService
import logging

logger = logging.getLogger(__name__)

empreendimentos_bp = Blueprint("empreendimentos", __name__, url_prefix="/empreendimentos")

empreendimento_schema = EmpreendimentoSchema()
empreendimentos_schema = EmpreendimentoSchema(many=True)

@empreendimentos_bp.route("", methods=["GET"])
def listar_empreendimentos():
    """Lista todos os empreendimentos com filtros opcionais."""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        filtros = {
            'construtora_id': request.args.get('construtora_id'),
            'nome': request.args.get('nome'),
            'cep': request.args.get('cep'),
            'data_inicio': request.args.get('dataInicio'),
            'data_fim': request.args.get('dataFim'),
            'somente_publicadas': request.args.get('somente_publicadas') == '1'
        }
        
        # Remover filtros vazios
        filtros = {k: v for k, v in filtros.items() if v is not None and v != ''}
        
        repo = EmpreendimentosRepositorySQL()
        empreendimentos = repo.listar_empreendimentos(filtros=filtros)
        return jsonify(empreendimentos), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar empreendimentos: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("/<int:empreendimento_id>", methods=["GET"])
def buscar_empreendimento(empreendimento_id):
    """Busca um empreendimento pelo ID."""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        repo = EmpreendimentosRepositorySQL()
        empreendimento = repo.obter_por_id(empreendimento_id)
        
        if not empreendimento:
            return jsonify({"message": "Empreendimento não encontrado"}), 404
            
        return jsonify(empreendimento), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar empreendimento {empreendimento_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("", methods=["POST"])
def criar_empreendimento():
    """
    Cria um novo empreendimento.
    Recebe um JSON com os dados do empreendimento.
    """
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        json_data = request.get_json()
        if not json_data:
            return jsonify(error="Nenhum dado JSON enviado"), 400

        try:
            data = empreendimento_schema.load(json_data)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        repo = EmpreendimentosRepositorySQL()
        novo_empreendimento = repo.criar(data)

        return jsonify(novo_empreendimento), 201
        
    except Exception as e:
        logger.error(f"Erro ao criar empreendimento: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("/<int:empreendimento_id>", methods=["PUT"])
def atualizar_empreendimento(empreendimento_id):
    """
    Atualiza um empreendimento existente pelo ID.
    Recebe um JSON com os dados atualizados do empreendimento.
    """
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        try:
            data = empreendimento_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(error="Campos inválidos", detalhes=err.messages), 422

        repo = EmpreendimentosRepositorySQL()
        empreendimento_atualizado = repo.atualizar(empreendimento_id, data)

        if not empreendimento_atualizado:
            return jsonify({"message": "Empreendimento não encontrado"}), 404
            
        return jsonify(empreendimento_atualizado), 200
        
    except Exception as e:
        logger.error(f"Erro ao atualizar empreendimento {empreendimento_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("/<int:empreendimento_id>", methods=["DELETE"])
def deletar_empreendimento(empreendimento_id):
    """Deleta um empreendimento pelo ID."""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        repo = EmpreendimentosRepositorySQL()
        sucesso = repo.deletar(empreendimento_id)
        
        if sucesso:
            return jsonify({"message": "Empreendimento deletado com sucesso"}), 204
        return jsonify({"message": "Empreendimento não encontrado"}), 404
        
    except Exception as e:
        logger.error(f"Erro ao deletar empreendimento {empreendimento_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("/<int:empreendimento_id>/publicar", methods=["POST"])
def publicar_empreendimento(empreendimento_id):
    """Publica um empreendimento."""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        repo = EmpreendimentosRepositorySQL()
        service = EmpreendimentosService(repo)
        empreendimento = service.publicar_empreendimento(empreendimento_id)
        
        if not empreendimento:
            return jsonify({"message": "Empreendimento não encontrado"}), 404
            
        return jsonify({
            "message": "Empreendimento publicado com sucesso",
            "id": empreendimento['id'],
            "publicado_em": empreendimento['publicado_em'],
            "expira_em": empreendimento['expira_em'],
            "status_publicacao": empreendimento['status_publicacao']
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao publicar empreendimento {empreendimento_id}: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("/<int:empreendimento_id>/aguardar", methods=["POST"])
def aguardar_publicacao(empreendimento_id):
    """Marca empreendimento para aguardar publicação."""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        repo = EmpreendimentosRepositorySQL()
        service = EmpreendimentosService(repo)
        empreendimento = service.aguardar_publicacao(empreendimento_id)
        
        if not empreendimento:
            return jsonify({"message": "Empreendimento não encontrado"}), 404
            
        return jsonify({
            "message": "Empreendimento marcado para aguardar publicação",
            "id": empreendimento['id'],
            "status_publicacao": empreendimento['status_publicacao']
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao marcar empreendimento {empreendimento_id} para aguardar: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@empreendimentos_bp.route("/upload/preview", methods=["POST"])
def preview_planilha():
    """Preview dos dados da planilha antes da publicação"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        repo = EmpreendimentosRepositorySQL()
        service = EmpreendimentosService(repo)
        resultado = service.preview_planilha(file)
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"Erro ao fazer preview da planilha: {str(e)}")
        return jsonify({'error': 'Erro ao processar planilha para preview'}), 500

@empreendimentos_bp.route("/upload", methods=["POST"])
def upload_planilha():
    """Upload de planilha de empreendimentos"""
    try:
        logger.info(f"Request recebido: {request.method} {request.path}")
        
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        repo = EmpreendimentosRepositorySQL()
        service = EmpreendimentosService(repo)
        resultado = service.processar_planilha(file)
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar planilha: {str(e)}")
        return jsonify({'error': 'Erro ao processar planilha'}), 500

@empreendimentos_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de verificação de saúde"""
    logger.info(f"Request recebido: {request.method} {request.path}")
    return jsonify({'status': 'OK', 'message': 'Serviço de empreendimentos funcionando'}), 200
