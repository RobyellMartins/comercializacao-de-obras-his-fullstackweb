import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const CadastrarUnidade = () => {
  const [formData, setFormData] = useState({
    empreendimento_id: '',
    numero_unidade: '',
    tamanho_m2: '',
    preco_venda: '',
    mecanismo_pagamento: 'outros',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await api.post('/api/unidades', formData);
      setSuccess('Unidade cadastrada com sucesso!');
      setTimeout(() => {
        navigate('/unidades');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao cadastrar unidade');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
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
          <TextField
            label="ID do Empreendimento"
            name="empreendimento_id"
            value={formData.empreendimento_id}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
            type="number"
          />
          <TextField
            label="Número da Unidade"
            name="numero_unidade"
            value={formData.numero_unidade}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
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
          />
          <TextField
            label="Preço de Venda"
            name="preco_venda"
            value={formData.preco_venda}
            onChange={handleChange}
            fullWidth
            margin="normal"
            type="number"
            step="0.01"
          />
          <TextField
            select
            label="Mecanismo de Pagamento"
            name="mecanismo_pagamento"
            value={formData.mecanismo_pagamento}
            onChange={handleChange}
            fullWidth
            margin="normal"
            SelectProps={{
              native: true,
            }}
          >
            <option value="financiamento">Financiamento</option>
            <option value="avista">À vista</option>
            <option value="consorcio">Consórcio</option>
            <option value="outros">Outros</option>
          </TextField>
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? <CircularProgress size={24} /> : 'Cadastrar'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default CadastrarUnidade;
