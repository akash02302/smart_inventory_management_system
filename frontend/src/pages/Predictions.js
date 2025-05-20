import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  MenuItem,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { predictDemand } from '../services/api';

const products = [
  { id: 101, name: 'Basmati Rice' },
  { id: 102, name: 'Ice Cream' },
  { id: 103, name: 'Raincoat' },
  { id: 104, name: 'Sweets' },
  { id: 105, name: 'Water Bottle' },
];

const regions = ['Delhi', 'Mumbai', 'Kochi'];
const weatherConditions = ['Hot', 'Cold', 'Rainy', 'Moderate'];

function Predictions() {
  const [formData, setFormData] = useState({
    date: new Date(),
    product_id: '',
    region: '',
    weather: '',
    is_festival: false,
    current_stock: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleDateChange = (date) => {
    setFormData((prev) => ({
      ...prev,
      date,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const payload = {
        ...formData,
        date: formData.date.toISOString().split('T')[0],
        product_id: parseInt(formData.product_id, 10),
        is_festival: formData.is_festival === 'true' || formData.is_festival === true,
      };
      if (formData.current_stock !== '' && formData.current_stock !== null && formData.current_stock !== undefined) {
        payload.current_stock = parseInt(formData.current_stock, 10);
      } else {
        payload.current_stock = null;
      }
      const response = await predictDemand(payload);
      setPrediction(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Demand Prediction
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                      label="Prediction Date"
                      value={formData.date}
                      onChange={handleDateChange}
                      renderInput={(params) => <TextField {...params} fullWidth />}
                    />
                  </LocalizationProvider>
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    select
                    fullWidth
                    label="Product"
                    name="product_id"
                    value={formData.product_id}
                    onChange={handleInputChange}
                    required
                  >
                    {products.map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    select
                    fullWidth
                    label="Region"
                    name="region"
                    value={formData.region}
                    onChange={handleInputChange}
                    required
                  >
                    {regions.map((region) => (
                      <MenuItem key={region} value={region}>
                        {region}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    select
                    fullWidth
                    label="Weather"
                    name="weather"
                    value={formData.weather}
                    onChange={handleInputChange}
                    required
                  >
                    {weatherConditions.map((weather) => (
                      <MenuItem key={weather} value={weather}>
                        {weather}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    type="number"
                    fullWidth
                    label="Current Stock (Optional)"
                    name="current_stock"
                    value={formData.current_stock}
                    onChange={handleInputChange}
                  />
                </Grid>

                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Predict Demand'}
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {prediction && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Prediction Results
                </Typography>
                <Box mt={2}>
                  <Typography variant="body1" gutterBottom>
                    Predicted Demand: {prediction.predicted_demand?.toFixed(2)} units
                  </Typography>
                  <Typography variant="body1" gutterBottom>
                    Recommendation: {prediction.recommendation}
                  </Typography>
                  <Typography variant="body1" gutterBottom>
                    Confidence Score: {(prediction.confidence_score * 100).toFixed(2)}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}

export default Predictions; 