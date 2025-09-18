import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import BackToHomeButton from '../components/BackToHomeButton';
import api from '../services/api';

const UploadPlanilha = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
          selectedFile.type === 'application/vnd.ms-excel') {
        setFile(selectedFile);
        setError('');
        setUploadResult(null);
      } else {
        setError('Por favor, selecione um arquivo Excel (.xlsx ou .xls)');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Por favor, selecione um arquivo');
      return;
    }

    setUploading(true);
    setError('');
    setUploadResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/empreendimentos/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadResult(response.data);
    } catch (err) {
      console.error('Erro no upload:', err);
      setError(
        err.response?.data?.error || 
        'Erro ao fazer upload do arquivo. Tente novamente.'
      );
    } finally {
      setUploading(false);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setUploadResult(null);
    setError('');
    // Reset file input
    const fileInput = document.getElementById('file-input');
    if (fileInput) {
      fileInput.value = '';
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <BackToHomeButton />
      
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Upload de Planilha - Comercialização de Obras HIS
        </Typography>
        
        <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
          Faça upload de planilhas Excel com dados dos empreendimentos e unidades
        </Typography>

        {!uploadResult && (
          <Box>
            <Box
              sx={{
                border: '2px dashed',
                borderColor: file ? 'success.main' : 'grey.300',
                borderRadius: 2,
                p: 4,
                textAlign: 'center',
                mb: 3,
                backgroundColor: file ? 'success.light' : 'grey.50',
                transition: 'all 0.3s ease',
              }}
            >
              <input
                id="file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="file-input">
                <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  {file ? file.name : 'Clique para selecionar um arquivo'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Formatos aceitos: .xlsx, .xls
                </Typography>
                <Button
                  variant="outlined"
                  component="span"
                  sx={{ mt: 2 }}
                  disabled={uploading}
                >
                  Selecionar Arquivo
                </Button>
              </label>
            </Box>

            {file && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="text.secondary">
                  Arquivo selecionado: <strong>{file.name}</strong>
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Tamanho: {(file.size / 1024 / 1024).toFixed(2)} MB
                </Typography>
              </Box>
            )}

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button
                variant="contained"
                onClick={handleUpload}
                disabled={!file || uploading}
                size="large"
                startIcon={<CloudUploadIcon />}
              >
                {uploading ? 'Enviando...' : 'Fazer Upload'}
              </Button>
              
              {file && (
                <Button
                  variant="outlined"
                  onClick={resetUpload}
                  disabled={uploading}
                  size="large"
                >
                  Cancelar
                </Button>
              )}
            </Box>
          </Box>
        )}

        {uploading && (
          <Box sx={{ mt: 3 }}>
            <LinearProgress />
            <Typography variant="body2" align="center" sx={{ mt: 1 }}>
              Processando arquivo...
            </Typography>
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 3 }} icon={<ErrorIcon />}>
            {error}
          </Alert>
        )}

        {uploadResult && (
          <Box sx={{ mt: 3 }}>
            <Alert severity="success" sx={{ mb: 3 }} icon={<CheckCircleIcon />}>
              Upload realizado com sucesso!
            </Alert>

            <Typography variant="h6" gutterBottom>
              Resultado do Processamento:
            </Typography>

            <List>
              <ListItem>
                <ListItemText
                  primary="Empreendimentos processados"
                  secondary={uploadResult.empreendimentos_processados || 0}
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Unidades processadas"
                  secondary={uploadResult.unidades_processadas || 0}
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Erros encontrados"
                  secondary={uploadResult.erros || 0}
                />
              </ListItem>
            </List>

            {uploadResult.detalhes_erros && uploadResult.detalhes_erros.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" color="error" gutterBottom>
                  Detalhes dos erros encontrados:
                </Typography>
                <List dense>
                  {uploadResult.detalhes_erros.map((erro, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={erro}
                        sx={{ color: 'error.main' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {uploadResult.empreendimentos && uploadResult.empreendimentos.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" color="success.main" gutterBottom>
                  Empreendimentos criados:
                </Typography>
                <List dense>
                  {uploadResult.empreendimentos.map((emp, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={emp.nome}
                        secondary={`Empresa: ${emp.nome_empresa} | CEP: ${emp.cep}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {uploadResult.unidades && uploadResult.unidades.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" color="info.main" gutterBottom>
                  Unidades criadas:
                </Typography>
                <List dense>
                  {uploadResult.unidades.slice(0, 10).map((unidade, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={`Unidade ${unidade.numero_unidade}`}
                        secondary={`${unidade.tamanho_m2}m² | R$ ${unidade.preco_venda?.toLocaleString('pt-BR')} | ${unidade.mecanismo_pagamento}`}
                      />
                    </ListItem>
                  ))}
                  {uploadResult.unidades.length > 10 && (
                    <ListItem>
                      <ListItemText
                        primary={`... e mais ${uploadResult.unidades.length - 10} unidades`}
                        sx={{ fontStyle: 'italic', color: 'text.secondary' }}
                      />
                    </ListItem>
                  )}
                </List>
              </Box>
            )}

            <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button
                variant="contained"
                onClick={resetUpload}
                size="large"
              >
                Fazer Novo Upload
              </Button>
            </Box>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default UploadPlanilha;
