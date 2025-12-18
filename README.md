# Salary Prediction API

A FastAPI-based machine learning API that predicts salary based on years of experience.

## Features

- RESTful API built with FastAPI
- Linear regression model for salary prediction
- Interactive API documentation (Swagger UI)

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn modelwithdepapi:app --reload
```

3. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

## API Endpoints

### GET /
Health check endpoint

### POST /predict
Predict salary based on years of experience

**Request Body:**
```json
{
  "years": 5.5
}
```

**Response:**
```json
{
  "years_experience": 5.5,
  "predicted_salary": 75000.0
}
```

## Deployment on Render

This project is configured for deployment on Render. The `render.yaml` file contains the deployment configuration.

### Steps to Deploy:

1. Push your code to a GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and configure the service
6. Make sure `salary_model.joblib` is included in your repository
7. Deploy!

The API will be available at your Render service URL.

