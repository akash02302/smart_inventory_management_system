import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  MenuItem,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { getInventoryRecommendations } from '../services/api';

const regions = ['All', 'Delhi', 'Mumbai', 'Kochi'];
const recommendations = ['All', 'Restock', 'Overstock', 'Stock OK'];

function Inventory() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [filters, setFilters] = useState({
    region: 'All',
    recommendation: 'All',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getInventoryRecommendations();
        setData(response);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const columns = [
    { field: 'product_id', headerName: 'Product ID', width: 100 },
    { field: 'product_name', headerName: 'Product Name', width: 150 },
    { field: 'region', headerName: 'Region', width: 120 },
    { field: 'current_stock', headerName: 'Current Stock', width: 120 },
    { field: 'predicted_demand', headerName: 'Predicted Demand', width: 150 },
    { field: 'restock_threshold', headerName: 'Restock Threshold', width: 150 },
    {
      field: 'recommendation',
      headerName: 'Recommendation',
      width: 150,
      renderCell: (params) => (
        <Box
          sx={{
            color:
              params.value === 'Restock'
                ? 'error.main'
                : params.value === 'Overstock'
                ? 'warning.main'
                : 'success.main',
          }}
        >
          {params.value}
        </Box>
      ),
    },
  ];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  const filteredRows = data.items.filter((item) => {
    const regionMatch = filters.region === 'All' || item.region === filters.region;
    const recommendationMatch =
      filters.recommendation === 'All' || item.recommendation === filters.recommendation;
    return regionMatch && recommendationMatch;
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Inventory Management
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <TextField
            select
            fullWidth
            label="Filter by Region"
            name="region"
            value={filters.region}
            onChange={handleFilterChange}
          >
            {regions.map((region) => (
              <MenuItem key={region} value={region}>
                {region}
              </MenuItem>
            ))}
          </TextField>
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            select
            fullWidth
            label="Filter by Recommendation"
            name="recommendation"
            value={filters.recommendation}
            onChange={handleFilterChange}
          >
            {recommendations.map((rec) => (
              <MenuItem key={rec} value={rec}>
                {rec}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
      </Grid>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={filteredRows}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10]}
          disableSelectionOnClick
          getRowId={(row) => `${row.product_id}-${row.region}`}
        />
      </Paper>
    </Box>
  );
}

export default Inventory; 