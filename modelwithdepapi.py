from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import joblib
import numpy as np
import logging
import os
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Salary Prediction API")

# Global variable to store model
model = None

# Load model with error handling
try:
    model_path = "salary_model.joblib"
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at: {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")
    model = joblib.load(model_path)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    logger.error(traceback.format_exc())
    model = None

class InputData(BaseModel):
    years: float

@app.get("/")
def home():
    """Health check endpoint"""
    try:
        status = {
            "message": "API is running 🚀",
            "model_loaded": model is not None,
            "status": "healthy" if model is not None else "error"
        }
        if model is None:
            status["error"] = "Model not loaded. Check server logs."
        return status
    except Exception as e:
        logger.error(f"Error in home endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "message": "API error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.get("/health")
def health_check():
    """Detailed health check"""
    try:
        health_status = {
            "status": "healthy" if model is not None else "unhealthy",
            "model_loaded": model is not None,
            "model_path": "salary_model.joblib",
            "model_exists": os.path.exists("salary_model.joblib")
        }
        
        if model is None:
            health_status["error"] = "Model is not loaded"
            return JSONResponse(status_code=503, content=health_status)
        
        return health_status
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.post("/predict")
def predict(data: InputData):
    """Predict salary based on years of experience"""
    try:
        # Check if model is loaded
        if model is None:
            error_msg = "Model not loaded. Please check server logs."
            logger.error(error_msg)
            raise HTTPException(
                status_code=503,
                detail=error_msg
            )
        
        # Validate input
        if data.years < 0:
            raise HTTPException(
                status_code=400,
                detail="Years of experience cannot be negative"
            )
        
        if data.years > 50:
            logger.warning(f"Unusually high years of experience: {data.years}")
        
        # Make prediction
        X = np.array([[data.years]])
        prediction = model.predict(X)
        
        result = {
            "years_experience": data.years,
            "predicted_salary": float(prediction[0]),
            "status": "success"
        }
        
        logger.info(f"Prediction made: {result}")
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=422,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "message": "Internal server error during prediction",
                "traceback": traceback.format_exc()
            }
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler to catch all unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "message": "An unexpected error occurred",
            "traceback": traceback.format_exc()
        }
    )
