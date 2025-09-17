import openpyxl
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class EmpreendimentosService:
    def __init__(self, repository):
        self.repository = repository
    
    def listar_todos(self) -> List[Dict]:
        """Lista todos os empreendimentos"""
        return self.repository.listar_todos()
    
    def obter_por_id(self, id: int) -> Optional[Dict]:
        """Obtém um empreendimento por ID"""
        return self.repository.obter_por_id(id)
    
    def criar(self, dados: Dict) -> Dict:
        """Cria um novo empreendimento"""
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'endereco', 'cidade']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"Campo '{campo}' é obrigatório")
        
        return self.repository.criar(dados)
    
    def atualizar(self, id: int, dados: Dict) -> Optional[Dict]:
        """Atualiza um empreendimento existente"""
        # Verificar se existe
        empreendimento_existente = self.repository.obter_por_id(id)
        if not empreendimento_existente:
            return None
        
        return self.repository.atualizar(id, dados)
    
    def deletar(self, id: int) -> bool:
        """Deleta um empreendimento"""
        # Verificar se existe
        empreendimento_existente = self.repository.obter_por_id(id)
        if not empreendimento_existente:
            return False
        
        return self.repository.deletar(id)
    
    def processar_planilha(self, file) -> Dict:
        """Processa uma planilha Excel com dados de empreendimentos"""
        try:
            # Carregar a planilha
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active
            
            empreendimentos_processados = []
            erros = []
            
            # Assumir que a primeira linha contém os cabeçalhos
            headers = []
            for cell in sheet[1]:
                headers.append(cell.value)
            
            # Mapear colunas esperadas
            mapeamento_colunas = {
                'nome': ['nome', 'empreendimento', 'projeto'],
                'endereco': ['endereco', 'endereço', 'rua', 'logradouro'],
                'cidade': ['cidade', 'municipio', 'município'],
                'estado': ['estado', 'uf'],
                'cep': ['cep'],
                'tipo': ['tipo', 'categoria'],
                'status': ['status', 'situacao', 'situação'],
                'valor_total': ['valor_total', 'valor total', 'investimento'],
                'unidades': ['unidades', 'qtd_unidades', 'quantidade']
            }
            
            # Encontrar índices das colunas
            indices_colunas = {}
            for campo, possiveis_nomes in mapeamento_colunas.items():
                for i, header in enumerate(headers):
                    if header and header.lower().strip() in [nome.lower() for nome in possiveis_nomes]:
                        indices_colunas[campo] = i
                        break
            
            # Processar cada linha (começando da linha 2)
            for row_num in range(2, sheet.max_row + 1):
                try:
                    row = sheet[row_num]
                    dados_empreendimento = {}
                    
                    # Extrair dados baseado no mapeamento
                    for campo, indice in indices_colunas.items():
                        if indice < len(row):
                            valor = row[indice].value
                            if valor is not None:
                                dados_empreendimento[campo] = str(valor).strip()
                    
                    # Validar se tem dados mínimos
                    if dados_empreendimento.get('nome'):
                        # Criar o empreendimento
                        empreendimento_criado = self.criar(dados_empreendimento)
                        empreendimentos_processados.append(empreendimento_criado)
                    else:
                        erros.append(f"Linha {row_num}: Nome do empreendimento não encontrado")
                        
                except Exception as e:
                    erros.append(f"Linha {row_num}: {str(e)}")
            
            return {
                'processados': len(empreendimentos_processados),
                'erros': len(erros),
                'detalhes_erros': erros,
                'empreendimentos': empreendimentos_processados
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar planilha: {str(e)}")
            raise Exception(f"Erro ao processar planilha: {str(e)}")
