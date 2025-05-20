# Smart Inventory Management System

A full-stack application for intelligent inventory management and demand forecasting.

## Features

- Demand forecasting using XGBoost
- Real-time inventory recommendations
- Interactive dashboard with visualizations
- Weather and festival impact analysis
- Responsive web interface

## Tech Stack

### Backend
- Python 3.9
- FastAPI
- XGBoost
- Pandas
- Scikit-learn

### Frontend
- React
- Material-UI
- Chart.js
- Axios

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Node.js 16+ (for local development)
- API keys for:
  - WeatherAPI
  - Calendarific

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd smart-inventory-management
```

2. Create a `.env` file in the root directory:
```bash
WEATHERAPI_KEY=your_weatherapi_key
CALENDARIFIC_API_KEY=your_calendarific_api_key
```

3. Place the dataset file:
```bash
cp path/to/your/dataset.csv backend/app/data/smart_inventory_stock_dataset.csv
```

4. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Backend Development

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

### Frontend Development

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Endpoints

- `POST /api/predict`: Get demand prediction
- `GET /api/recommend`: Get inventory recommendations
- `POST /api/train`: Train the forecasting model

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

The application is containerized and can be deployed to any cloud platform that supports Docker:

1. Build the images:
```bash
docker-compose build
```

2. Push to your container registry:
```bash
docker tag smart-inventory-management_backend your-registry/backend:latest
docker tag smart-inventory-management_frontend your-registry/frontend:latest
docker push your-registry/backend:latest
docker push your-registry/frontend:latest
```

3. Deploy to your cloud platform using the provided docker-compose.yml

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 