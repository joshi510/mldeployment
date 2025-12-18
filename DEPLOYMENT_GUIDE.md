# Step-by-Step Render Deployment Guide

## ✅ Prerequisites Completed
- ✅ Code pushed to GitHub: https://github.com/joshi510/mldeployment
- ✅ All required files are in the repository
- ✅ Error handling and logging configured

## 🚀 Deployment Steps

### Step 1: Sign up/Login to Render
1. Go to https://dashboard.render.com
2. Sign up for a free account (or login if you already have one)
3. You can sign up with your GitHub account for easier integration

### Step 2: Create New Web Service
1. Click the **"New +"** button (top right)
2. Select **"Web Service"** from the dropdown

### Step 3: Connect GitHub Repository
1. Click **"Connect account"** if you haven't connected GitHub yet
2. Authorize Render to access your GitHub repositories
3. Select your repository: **`joshi510/mldeployment`**
4. Click **"Connect"**

### Step 4: Configure Service (Auto-detected)
Render will automatically detect your `render.yaml` file and configure:
- **Name**: salary-prediction-api (or you can change it)
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn modelwithdepapi:app --host 0.0.0.0 --port $PORT --log-level info`
- **Python Version**: 3.11.0

**You don't need to change anything** - it's all configured!

### Step 5: Deploy
1. Scroll down and click **"Create Web Service"**
2. Render will start building and deploying your application
3. Wait for the deployment to complete (usually 2-5 minutes)

### Step 6: Monitor Deployment
- Watch the **"Logs"** tab to see the build progress
- You'll see:
  - Installing dependencies
  - Loading the model
  - Starting the server
- If there are any errors, they'll be displayed here

### Step 7: Test Your API
Once deployed, you'll get a URL like:
- `https://salary-prediction-api.onrender.com` (or similar)

Test endpoints:
- **Home**: `https://your-app.onrender.com/`
- **Health Check**: `https://your-app.onrender.com/health`
- **API Docs**: `https://your-app.onrender.com/docs`
- **Predict**: `https://your-app.onrender.com/predict` (POST request)

## 🔍 Troubleshooting

### If deployment fails:
1. Check the **Logs** tab in Render dashboard
2. Common issues:
   - Model file not found → Make sure `salary_model.joblib` is in the repo
   - Dependencies error → Check `requirements.txt`
   - Port error → Already handled in `render.yaml`

### View errors:
- Go to your service → **Logs** tab
- All errors are logged with full details
- Use `/health` endpoint to check model status

## 📝 Notes
- **Free tier**: Your app may sleep after 15 minutes of inactivity
- **First request**: May take 30-60 seconds to wake up
- **Logs**: All errors are visible in the Render dashboard logs

## ✅ Your API is Ready!
Once deployed, share your Render URL and start making predictions!

