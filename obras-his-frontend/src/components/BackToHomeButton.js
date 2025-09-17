import React from 'react';
import { Button } from '@mui/material';
import { Home as HomeIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const BackToHomeButton = () => {
  const navigate = useNavigate();

  const handleBackToHome = () => {
    navigate('/');
  };

  return (
    <Button
      variant="outlined"
      startIcon={<HomeIcon />}
      onClick={handleBackToHome}
      sx={{ mb: 2 }}
    >
      Voltar ao Início
    </Button>
  );
};

export default BackToHomeButton;
