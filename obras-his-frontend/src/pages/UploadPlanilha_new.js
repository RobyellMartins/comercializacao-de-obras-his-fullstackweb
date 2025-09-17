import React, { useState, useCallback } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Button, 
  Alert, 
  CircularProgress,
  Paper,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent,
  Chip,
  useTheme
} from '@mui/material';
import { 
  CloudUpload as UploadIcon,
  Description as FileIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import BackToHomeButton from '../components/BackToHomeButton';
import api from '../services/api';

const UploadPlanilha = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [uploadResults, setUploadResults] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const theme = useTheme();

  const handleFileChange = (selectedFile) => {
    if (selectedFile) {
      if (selectedFile.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
          selectedFile.type === 'application/vnd.ms-excel') {
        setFile(selectedFile);
        setMessage('');
      } else {
        setMessage('Por favor, selecione um arquivo Excel (.xlsx ou .xls)');
        setMessageType('error');
        setFile(null);
      }
    }
  };

  const handleInputChange = (event) => {
    const selectedFile = event.target.files[0];
    handleFileChange(selectedFile);
  };

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    setDragOver(false);
    const droppedFile = event.dataTransfer.files[0];
    handleFileChange(droppedFile);
  }, []);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((event) => {
    event.preventDefault();
    setDragOver(false);
  }, []);

  const handleUpload = async () => {
    if (!file) {
      setMessage('Por favor, selecione um arquivo');
      setMessageType('error');
      return;
    }

    setUploading(true);
    setMessage('');
    setUploadResults(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage('Upload realizado com sucesso!');
      setMessageType('success');
      setUploadResults(response.data);
      setFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('file-input');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (error) {
      console.error('Erro no upload:', error);
      setMessage(error.response?.data?.error || 'Erro ao fazer upload do arquivo');
      setMessageType('error');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: 'calc(100vh - 64px)',
        background: `linear-gradient(135deg, ${theme.palette.primary.light}15 0%, ${theme.palette.secondary.light}15 100%)`,
        py: 4,
      }}
    >
      <Container maxWidth="md">
        <BackToHomeButton />
        
        {/* Header */}
        <Box textAlign="center" mb={4} sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 2 }}>
            <UploadIcon sx={{ fontSize: 48, color: theme.palette.secondary.main, mr: 2 }} />
            <Typography 
              variant="h3" 
              component="h1" 
              sx={{ 
                fontWeight: 700,
                background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Upload de Planilhas
            </Typography>
          </Box>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            Importe dados de empreendimentos através de planilhas Excel para cadastro em lote
          </Typography>
        </Box>

        {/* Upload Area */}
        <Card sx={{ mb: 4, overflow: 'visible' }}>
          <CardContent sx={{ p: 4 }}>
            <Box
              className={`drag-zone ${dragOver ? 'drag-over' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              sx={{
                border: `2px dashed ${dragOver ? theme.palette.primary.main : '#cbd5e1'}`,
                borderRadius: 3,
                p: 6,
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                backgroundColor: dragOver ? `${theme.palette.primary.light}10` : '#f8fafc',
                '&:hover': {
                  borderColor: theme.palette.primary.main,
                  backgroundColor: `${theme.palette.primary.light}08`,
                }
              }}
              onClick={() => document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleInputChange}
                style={{ display: 'none' }}
              />
              
              <UploadIcon sx={{ fontSize: 64, color: theme.palette.primary.main, mb: 2 }} />
              
              <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
                {dragOver ? 'Solte o arquivo aqui' : 'Arraste e solte seu arquivo aqui'}
              </Typography>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                ou clique para selecionar um arquivo Excel (.xlsx, .xls)
              </Typography>
              
              <Button
                variant="outlined"
                startIcon={<FileIcon />}
                sx={{ 
                  borderRadius: 2,
                  px: 3,
                  py: 1.5,
                  fontWeight: 600
                }}
              >
                Selecionar Arquivo
              </Button>
            </Box>
            
            {file && (
              <Box sx={{ mt: 3, p: 3, backgroundColor: theme.palette.success.light + '20', borderRadius: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <FileIcon sx={{ color: theme.palette.success.main }} />
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>
                      {file.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </Typography>
                  </Box>
                  <Chip 
                    label="Pronto" 
                    color="success" 
                    size="small"
                    icon={<SuccessIcon />}
                  />
                </Box>
              </Box>
            )}

            <Box sx={{ mt: 4 }}>
              <Button
                variant="contained"
                onClick={handleUpload}
                disabled={!file || uploading}
                startIcon={uploading ? <CircularProgress size={20} color="inherit" /> : <UploadIcon />}
                fullWidth
                size="large"
                sx={{
                  py: 2,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  borderRadius: 2,
                }}
              >
                {uploading ? 'Processando Upload...' : 'Fazer Upload'}
              </Button>
            </Box>
          </CardContent>
        </Card>

        {/* Messages */}
        {message && (
          <Alert 
            severity={messageType} 
            sx={{ 
              mb: 3,
              borderRadius: 2,
              '& .MuiAlert-icon': {
                fontSize: '1.5rem'
              }
            }}
          >
            {message}
          </Alert>
        )}

        {/* Upload Results */}
        {uploadResults && (
          <Card sx={{ mb: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                <InfoIcon sx={{ color: theme.palette.info.main }} />
                Resultados do Upload
              </Typography>
              
              {uploadResults.summary && (
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Chip 
                      label={`Total: ${uploadResults.summary.total || 0}`}
                      variant="outlined"
                      sx={{ fontWeight: 600 }}
                    />
                    <Chip 
                      label={`Sucessos: ${uploadResults.summary.success || 0}`}
                      color="success"
                      sx={{ fontWeight: 600 }}
                    />
                    <Chip 
                      label={`Erros: ${uploadResults.summary.errors || 0}`}
                      color="error"
                      sx={{ fontWeight: 600 }}
                    />
                  </Box>
                </Box>
              )}

              {uploadResults.errors && uploadResults.errors.length > 0 && (
                <Box>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <ErrorIcon sx={{ color: theme.palette.error.main }} />
                    Erros Encontrados
                  </Typography>
                  <Paper sx={{ p: 2, backgroundColor: theme.palette.error.light + '10' }}>
                    <List dense>
                      {uploadResults.errors.slice(0, 10).map((error, index) => (
                        <ListItem key={index} sx={{ px: 0 }}>
                          <ListItemText
                            primary={`Linha ${error.row || 'N/A'}: ${error.message || error}`}
                            secondary={error.data ? JSON.stringify(error.data) : ''}
                            primaryTypographyProps={{ fontWeight: 500 }}
                          />
                        </ListItem>
                      ))}
                      {uploadResults.errors.length > 10 && (
                        <ListItem sx={{ px: 0 }}>
                          <ListItemText
                            primary={`... e mais ${uploadResults.errors.length - 10} erros`}
                            primaryTypographyProps={{ fontStyle: 'italic', color: 'text.secondary' }}
                          />
                        </ListItem>
                      )}
                    </List>
                  </Paper>
                </Box>
              )}
            </CardContent>
          </Card>
        )}

        {/* Format Guide */}
        <Card>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
              <InfoIcon sx={{ color: theme.palette.info.main }} />
              Formato da Planilha
            </Typography>
            <Typography variant="body1" paragraph color="text.secondary">
              Para garantir o sucesso da importação, sua planilha Excel deve conter as seguintes colunas:
            </Typography>
            
            <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' } }}>
              {[
                { field: 'nome_empreendimento', desc: 'Nome do empreendimento', required: true },
                { field: 'construtora', desc: 'Nome da construtora', required: true },
                { field: 'endereco', desc: 'Endereço completo', required: true },
                { field: 'cep', desc: 'CEP (formato: 00000-000)', required: true },
                { field: 'publicado', desc: 'Status de publicação (true/false)', required: false },
              ].map((item, index) => (
                <Box key={index} sx={{ p: 2, backgroundColor: theme.palette.grey[50], borderRadius: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Typography variant="body1" sx={{ fontWeight: 600, fontFamily: 'monospace' }}>
                      {item.field}
                    </Typography>
                    {item.required && (
                      <Chip label="Obrigatório" size="small" color="error" />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {item.desc}
                  </Typography>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
};

export default UploadPlanilha;
