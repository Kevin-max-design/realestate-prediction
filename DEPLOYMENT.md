# Deployment Guide for Bangalore Real Estate Predictor

This guide outlines the steps to deploy your application to [Render](https://render.com).

## Prerequisites

- [GitHub Account](https://github.com)
- [Render Account](https://render.com)
- Git installed locally

## Step 1: Push to GitHub

1.  **Initialize Git** (if not already done):
    ```bash
    git init
    ```

2.  **Commit Changes**:
    The `.gitignore` has been updated to exclude large training files (`checkpoints/*.joblib`, `data/*.csv`, `files/`, `results/`) while keeping necessary inference artifacts (`best_gat_model.pt`, scalers).
    
    ```bash
    git add .
    git commit -m "Prepare for deployment"
    ```

3.  **Create a Repository on GitHub**:
    - Go to GitHub and create a new public repository (e.g., `bangalore-real-estate-predictor`).
    - Do *not* initialize with README/gitignore (we have them).

4.  **Push Code**:
    ```bash
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/bangalore-real-estate-predictor.git
    git push -u origin main
    ```

## Step 2: Deploy on Render

1.  **Create New Web Service**:
    - Log in to Render.
    - Click **New +** -> **Web Service**.
    - Connect your GitHub repository.

2.  **Configure Service**:
    - **Name**: `bangalore-price-predictor` (or similar)
    - **Region**: Closest to you (e.g., Singapore)
    - **Branch**: `main`
    - **Runtime**: `Python 3`
    - **Build Command**:
        ```bash
        pip install -r requirements.txt
        ```
    - **Start Command**:
        ```bash
        uvicorn api.main:app --host 0.0.0.0 --port $PORT
        ```

3.  **Environment Variables**:
    - No specific env vars are strictly required for the basic app.
    - `PORT` is automatically set by Render (our code respects this).

4.  **Deploy**:
    - Click **Create Web Service**.
    - Wait for the build to finish. Render will install dependencies and start the server.

## Step 3: Verification

Once deployed, Render will provide a URL (e.g., `https://bangalore-price-predictor.onrender.com`).

1.  **Visit the App**: Open the URL in your browser. You should see the prediction interface.
2.  **Test Prediction**:
    - Enter a location (e.g., "Whitefield").
    - Enter square footage (e.g., "1500").
    - Click **Predict Price**.
3.  **Verify Results**: Ensure the price, map, and comparables load correctly.

## Debugging

- **Logs**: Check the "Logs" tab in Render dashboard if the deployment fails.
- **Port**: Ensure the Start Command uses `$PORT` (our `api/main.py` is updated to support this).
- **Files**: If `FileNotFoundError` occurs, ensure `checkpoints/` artifacts were committed to GitHub.
