import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { Home as HomeIcon } from '@mui/icons-material';

const Header = () => {
  return (
    <AppBar position="static" elevation={0}>
      <Toolbar sx={{ minHeight: '64px' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <HomeIcon sx={{ fontSize: 28, color: 'white' }} />
          <Typography 
            variant="h6" 
            component="h1" 
            sx={{ 
              fontWeight: 700,
              fontSize: '1.25rem',
              letterSpacing: '-0.025em'
            }}
          >
            Sistema de Obras HIS
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
