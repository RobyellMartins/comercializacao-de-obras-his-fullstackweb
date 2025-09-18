import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import BackToHomeButton from '../components/BackToHomeButton';
import api from '../services/api';

const CadastrarUnidade = () => {
  const [formData, setFormData] = useState({
    empreendimento_id: '',
    numero_unidade: '',
    tamanho_m2: '',
    preco_venda: '',
    mecanismo_pagamento: '',
    outro_pagamento: '', // Campo para quando "outros" for selecionado
  });
  const [empreendimentos, setEmpreendimentos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingEmpreendimentos, setLoadingEmpreendimentos] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Carregar empreendimentos ao montar o componente
  useEffect(() => {
    const carregarEmpreendimentos = async () => {
      try {
        const response = await api.get('/empreendimentos');
        setEmpreendimentos(response.data);
      } catch (err) {
        setError('Erro ao carregar empreendimentos');
      } finally {
        setLoadingEmpreendimentos(false);
      }
    };

    carregarEmpreendimentos();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData((prev) => ({
      ...prev,
      [name]: value,
      // Limpar campo "outro_pagamento" se não for "outros"
      ...(name === 'mecanismo_pagamento' && value !== 'outros' ? { outro_pagamento: '' } : {})
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      // Preparar dados para envio
      const dadosEnvio = {
        ...formData,
        // Se mecanismo for "outros", usar o valor do campo outro_pagamento
        mecanismo_pagamento: formData.mecanismo_pagamento === 'outros' 
          ? formData.outro_pagamento 
          : formData.mecanismo_pagamento
      };
      
      // Remover campo auxiliar
      delete dadosEnvio.outro_pagamento;
      
      await api.post('/api/unidades', dadosEnvio);
      setSuccess('Unidade cadastrada com sucesso!');
      setTimeout(() => {
        navigate('/');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao cadastrar unidade');
    } finally {
      setLoading(false);
    }
  };

  const mecanismosPagamento = [
    { value: 'financiamento', label: 'Financiamento Bancário' },
    { value: 'avista', label: 'À Vista' },
    { value: 'consorcio', label: 'Consórcio' },
    { value: 'outros', label: 'Outros (especificar)' },
  ];

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <BackToHomeButton />
      
      <Paper sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>
          Cadastrar Unidade
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}
        
        <Box component="form" onSubmit={handleSubmit} noValidate>
          {/* Dropdown de Empreendimentos */}
          <FormControl fullWidth margin="normal" required>
            <InputLabel id="empreendimento-label">Selecione o Empreendimento</InputLabel>
            <Select
              labelId="empreendimento-label"
              name="empreendimento_id"
              value={formData.empreendimento_id}
              onChange={handleChange}
              label="Selecione o Empreendimento"
              disabled={loadingEmpreendimentos}
            >
              {loadingEmpreendimentos ? (
                <MenuItem disabled>
                  <CircularProgress size={20} sx={{ mr: 1 }} />
                  Carregando empreendimentos...
                </MenuItem>
              ) : empreendimentos.length === 0 ? (
                <MenuItem disabled>Nenhum empreendimento encontrado</MenuItem>
              ) : (
                empreendimentos.map((emp) => (
                  <MenuItem key={emp.id} value={emp.id}>
                    {emp.nome} - {emp.construtora_nome || emp.nome_empresa}
                  </MenuItem>
                ))
              )}
            </Select>
          </FormControl>

          <TextField
            label="Número da Unidade"
            name="numero_unidade"
            value={formData.numero_unidade}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
            placeholder="Ex: 101, A-201, Casa 15"
            helperText="Informe o número ou identificação da unidade"
          />
          
          <TextField
            label="Tamanho (m²)"
            name="tamanho_m2"
            value={formData.tamanho_m2}
            onChange={handleChange}
            fullWidth
            margin="normal"
            type="number"
            step="0.01"
            placeholder="Ex: 65.50"
            helperText="Área total da unidade em metros quadrados"
          />
          
          <TextField
            label="Preço de Venda (R$)"
            name="preco_venda"
            value={formData.preco_venda}
            onChange={handleChange}
            fullWidth
            margin="normal"
            type="number"
            step="0.01"
            placeholder="Ex: 180000.00"
            helperText="Valor de venda da unidade em reais"
          />
          
          {/* Dropdown de Mecanismo de Pagamento */}
          <FormControl fullWidth margin="normal" required>
            <InputLabel id="pagamento-label">Forma de Pagamento</InputLabel>
            <Select
              labelId="pagamento-label"
              name="mecanismo_pagamento"
              value={formData.mecanismo_pagamento}
              onChange={handleChange}
              label="Forma de Pagamento"
            >
              {mecanismosPagamento.map((mecanismo) => (
                <MenuItem key={mecanismo.value} value={mecanismo.value}>
                  {mecanismo.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Campo de texto para "Outros" */}
          {formData.mecanismo_pagamento === 'outros' && (
            <TextField
              label="Especifique a forma de pagamento"
              name="outro_pagamento"
              value={formData.outro_pagamento}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              placeholder="Ex: Parcelamento direto, Permuta, etc."
              helperText="Descreva a forma de pagamento específica"
            />
          )}
          
          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button 
              variant="outlined" 
              onClick={() => navigate('/')}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained" 
              disabled={loading || loadingEmpreendimentos}
              sx={{ minWidth: 120 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Cadastrar Unidade'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default CadastrarUnidade;
