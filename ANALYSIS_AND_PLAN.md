# Análise do Sistema Atual e Plano de Implementação

## Análise do Sistema Atual

### O que já está implementado:
1. **Modelos de Dados**: 
   - Construtora, Empreendimento, Unidade com relacionamentos corretos
   - Campos de publicação (publicado_em, expira_em) já existem

2. **Backend (Flask)**:
   - CRUD básico para empreendimentos
   - Upload de planilha com processamento básico
   - Estrutura de repositórios e serviços

3. **Frontend (React)**:
   - Páginas para cadastro manual de empreendimentos e unidades
   - Interface de upload de planilha
   - Listagem de empreendimentos

### O que precisa ser implementado/melhorado:

## PLANO DE IMPLEMENTAÇÃO

### 1. **Configuração do Banco de Dados**
- [ ] Atualizar configuração para usar PostgreSQL (IP: 192.168.50.12, porta: 5432, banco: familias)
- [ ] Criar arquivo .env com as credenciais corretas

### 2. **Melhorias no Modelo de Dados**
- [ ] Adicionar campo "nome_empresa" no modelo Empreendimento (separado de construtora_id)
- [ ] Garantir que mecanismos de pagamento aceitem: financiamento, à vista, consórcio, outros
- [ ] Adicionar campos de auditoria e histórico

### 3. **Processamento de Planilha com Unicode**
- [ ] Implementar tratamento unicode adequado no service
- [ ] Melhorar validação de campos obrigatórios
- [ ] Adicionar suporte para múltiplos empreendimentos na mesma planilha

### 4. **Funcionalidade de Resumo e Validação**
- [ ] Criar endpoint para preview dos dados antes da publicação
- [ ] Implementar tela de resumo com botão de validação
- [ ] Permitir edição dos dados importados antes da publicação

### 5. **Sistema de Publicação**
- [ ] Implementar botões "Publicar" e "Aguardar Publicação"
- [ ] Sistema automático de expiração em 30 dias
- [ ] Filtros por período, construtora, empreendimento

### 6. **Autocompletar CEP**
- [ ] Integrar API de CEP (ViaCEP) no frontend
- [ ] Preencher endereço automaticamente

### 7. **Melhorias na Interface**
- [ ] Tela de resumo dos dados coletados
- [ ] Validação visual antes da publicação
- [ ] Filtros avançados na listagem
- [ ] Histórico de uploads

### 8. **Tratamento de Erros e Validações**
- [ ] Mensagens específicas para formatos inválidos
- [ ] Reenvio sem perda de dados vinculados
- [ ] Tratamento de indisponibilidade do sistema

### 9. **Funcionalidades de Download**
- [ ] Link para download da planilha
- [ ] Visualização em tela dos dados publicados

### 10. **Testes e Validação**
- [ ] Testes das duas modalidades de cadastro
- [ ] Validação contra modelo oficial
- [ ] Testes de auditoria e histórico
