import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da aplicação
APP_NAME = os.getenv('APP_NAME', 'Sistema de Obras HIS')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///obras_his.db')

# Configurações CORS
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')

# Configurações de upload
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configurações de paginação
DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))

# Configurações de cache
CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))

# Configurações de publicação
PUBLICACAO_DURACAO_DIAS = int(os.getenv('PUBLICACAO_DURACAO_DIAS', 30))

# Configurações de email (para notificações futuras)
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

# Configurações de segurança
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hora

# Configurações de API
API_VERSION = os.getenv('API_VERSION', 'v1')
API_PREFIX = f'/api/{API_VERSION}'

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_path():
    """Retorna o caminho completo para a pasta de uploads"""
    upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
    os.makedirs(upload_path, exist_ok=True)
    return upload_path
