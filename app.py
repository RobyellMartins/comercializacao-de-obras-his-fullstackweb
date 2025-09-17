from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
import logging
import os

from src.config import *
from src.db_sql import init_db, create_initial_data

def create_app():
    app = Flask(__name__)
    
    # Configuração de logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT
    )
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    
    # Configuração CORS
    origins = (
        [o.strip() for o in ALLOWED_ORIGINS.split(",")]
        if ALLOWED_ORIGINS != "*"
        else "*"
    )
    CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)
    
    # Inicializar banco de dados
    init_db()
    create_initial_data()
    
    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
    }
    Swagger(app, config=swagger_config)
    
    # Registrar blueprints
    from src.blueprints.empreendimentos import empreendimentos_bp
    from src.blueprints.construtoras import construtoras_bp
    from src.blueprints.obras import obras_bp
    from src.blueprints.unidades import unidades_bp
    
    app.register_blueprint(empreendimentos_bp)
    app.register_blueprint(construtoras_bp)
    app.register_blueprint(obras_bp)
    app.register_blueprint(unidades_bp)
    
    # Rotas principais
    @app.route("/")
    def home():
        return jsonify({
            "message": "Sistema de Obras HIS - API",
            "version": "1.0.0",
            "docs": "/docs/",
            "endpoints": {
                "empreendimentos": "/empreendimentos",
                "construtoras": "/api/construtoras",
                "obras": "/api/obras",
                "unidades": "/api/unidades"
            }
        })
    
    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok", 
            "app": APP_NAME,
            "version": "1.0.0"
        })
    
    # Handlers de erro
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Recurso não encontrado"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error="Erro interno do servidor"), 500
    
    @app.errorhandler(413)
    def too_large(e):
        return jsonify(error="Arquivo muito grande"), 413
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
