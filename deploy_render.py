"""
Render Deployment Script
This script helps deploy your FastAPI application to Render using their API.

Usage:
1. Get your Render API key from: https://dashboard.render.com/account/api-keys
2. Set it as environment variable: set RENDER_API_KEY=your_key_here
3. Run: python deploy_render.py
"""

import os
import requests
import json
import time

# Render API configuration
RENDER_API_BASE = "https://api.render.com/v1"
API_KEY = os.getenv("RENDER_API_KEY")

if not API_KEY:
    print("❌ Error: RENDER_API_KEY environment variable not set")
    print("\nTo get your API key:")
    print("1. Go to https://dashboard.render.com/account/api-keys")
    print("2. Create a new API key")
    print("3. Set it: set RENDER_API_KEY=your_key_here (Windows)")
    print("   or: export RENDER_API_KEY=your_key_here (Linux/Mac)")
    exit(1)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_owner_id():
    """Get the owner ID (your account ID)"""
    try:
        response = requests.get(f"{RENDER_API_BASE}/owners", headers=headers)
        response.raise_for_status()
        owners = response.json()
        if owners:
            return owners[0]["owner"]["id"]
        return None
    except Exception as e:
        print(f"❌ Error getting owner ID: {e}")
        return None

def check_existing_service():
    """Check if service already exists"""
    try:
        response = requests.get(f"{RENDER_API_BASE}/services", headers=headers)
        response.raise_for_status()
        services = response.json()
        for service in services:
            if service.get("service", {}).get("name") == "salary-prediction-api":
                return service["service"]["id"]
        return None
    except Exception as e:
        print(f"⚠️  Could not check existing services: {e}")
        return None

def create_service(owner_id):
    """Create a new web service on Render"""
    service_data = {
        "type": "web_service",
        "name": "salary-prediction-api",
        "ownerId": owner_id,
        "repo": "https://github.com/joshi510/mldeployment",
        "branch": "main",
        "rootDir": "",
        "runtime": "python",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "uvicorn modelwithdepapi:app --host 0.0.0.0 --port $PORT --log-level info",
        "planId": "starter",  # Free tier
        "region": "oregon",  # You can change this
        "envVars": [
            {
                "key": "PYTHON_VERSION",
                "value": "3.11.0"
            },
            {
                "key": "PYTHONUNBUFFERED",
                "value": "1"
            }
        ]
    }
    
    try:
        print("🚀 Creating web service on Render...")
        response = requests.post(
            f"{RENDER_API_BASE}/services",
            headers=headers,
            data=json.dumps(service_data)
        )
        response.raise_for_status()
        service = response.json()
        return service.get("service", {}).get("id")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 409:
            print("⚠️  Service already exists. Use Render dashboard to manage it.")
            return None
        print(f"❌ Error creating service: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_service_url(service_id):
    """Get the service URL"""
    try:
        response = requests.get(
            f"{RENDER_API_BASE}/services/{service_id}",
            headers=headers
        )
        response.raise_for_status()
        service = response.json()
        return service.get("service", {}).get("serviceDetails", {}).get("url")
    except Exception as e:
        print(f"⚠️  Could not get service URL: {e}")
        return None

def main():
    print("=" * 60)
    print("Render Deployment Script")
    print("=" * 60)
    print()
    
    # Get owner ID
    print("📋 Getting account information...")
    owner_id = get_owner_id()
    if not owner_id:
        print("❌ Failed to get owner ID. Check your API key.")
        return
    
    print(f"✅ Owner ID: {owner_id}")
    print()
    
    # Check if service exists
    print("🔍 Checking for existing service...")
    existing_id = check_existing_service()
    if existing_id:
        print(f"⚠️  Service 'salary-prediction-api' already exists!")
        print(f"   Service ID: {existing_id}")
        url = get_service_url(existing_id)
        if url:
            print(f"   URL: {url}")
        print("\n💡 To redeploy, use the Render dashboard or trigger a new deploy via API.")
        return
    
    # Create service
    service_id = create_service(owner_id)
    if not service_id:
        print("\n❌ Failed to create service.")
        print("💡 You may need to:")
        print("   1. Connect your GitHub account in Render dashboard first")
        print("   2. Or create the service manually via dashboard")
        return
    
    print(f"✅ Service created! Service ID: {service_id}")
    print()
    print("⏳ Deployment is starting...")
    print("   This may take 2-5 minutes.")
    print("   Check progress at: https://dashboard.render.com")
    print()
    
    # Try to get URL (may take a moment)
    time.sleep(5)
    url = get_service_url(service_id)
    if url:
        print(f"🌐 Your API will be available at: {url}")
    else:
        print("💡 Check your Render dashboard for the service URL")
    
    print()
    print("=" * 60)
    print("✅ Deployment initiated!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Go to https://dashboard.render.com")
    print("2. Find your service 'salary-prediction-api'")
    print("3. Watch the deployment logs")
    print("4. Once deployed, test your API!")

if __name__ == "__main__":
    main()

