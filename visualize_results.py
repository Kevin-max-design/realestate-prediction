"""
Visualization Script for Model Performance
==========================================
Generates confusion matrix (binned) and correlation heatmap 
for the high-accuracy GNN model.
"""

import os
import sys
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from train_max_accuracy import create_graph, prepare_max_features, MaxAccuracyGNN
from src.data_loader import load_raw_data
from src.data_cleaner import clean_data
from src.feature_engineering import create_features
from src.advanced_features import create_advanced_features
from train_max_accuracy import create_target_encoded_features

def generate_visualizations():
    print("\n📊 Generating visualization plots...")
    
    # 1. Load Data & Model
    print("  Loading data and best model...")
    data_path = Path(__file__).parent / 'data' / 'Bengaluru_House_Data.csv'
    df = load_raw_data(str(data_path))
    df = clean_data(df)
    df = create_features(df)
    df = create_advanced_features(df)
    df = create_target_encoded_features(df)
    
    X, y, feature_names, scaler = prepare_max_features(df)
    
    # Normalize target for model
    y_mean, y_std = y.mean(), y.std()
    y_norm = (y - y_mean) / y_std
    
    # Create graph
    data = create_graph(X, y_norm, k=25)
    
    # Load model
    model = MaxAccuracyGNN(in_channels=X.shape[1], hidden=256, heads=8, dropout=0.15)
    checkpoint_path = Path(__file__).parent / 'checkpoints' / 'max_accuracy_gnn.pt'
    
    if not checkpoint_path.exists():
        print(f"Error: Checkpoint not found at {checkpoint_path}")
        return
        
    model.load_state_dict(torch.load(checkpoint_path))
    model.eval()
    
    # Get predictions
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        out_denorm = out * y_std + y_mean
        y_true = data.y * y_std + y_mean
        
        y_pred = out_denorm.numpy().flatten()
        y_actual = y_true.numpy().flatten()
    
    # Create results directory
    results_dir = Path(__file__).parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    # =========================================================================
    # 2. CONFUSION MATRIX (Binned)
    # =========================================================================
    print("  Generating confusion matrix...")
    
    # Create price bins for classification-style confusion matrix
    # Bins: <3000, 3000-5000, 5000-7000, 7000-10000, >10000
    bins = [0, 3000, 5000, 7000, 10000, float('inf')]
    labels = ['<3k', '3k-5k', '5k-7k', '7k-10k', '>10k']
    
    y_true_binned = pd.cut(y_actual, bins=bins, labels=labels)
    y_pred_binned = pd.cut(y_pred, bins=bins, labels=labels)
    
    cm = confusion_matrix(y_true_binned, y_pred_binned, labels=labels)
    
    # Plot Confusion Matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)
    plt.title('Price Range Confusion Matrix (Actual vs Predicted)', fontsize=14)
    plt.xlabel('Predicted Price Range (₹/sqft)', fontsize=12)
    plt.ylabel('Actual Price Range (₹/sqft)', fontsize=12)
    plt.tight_layout()
    plt.savefig(results_dir / 'confusion_matrix.png', dpi=300)
    print(f"  ✓ Saved confusion_matrix.png")
    
    # =========================================================================
    # 3. HEATMAP (Feature Correlations)
    # =========================================================================
    print("  Generating correlation heatmap...")
    
    # Select important features for heatmap
    heatmap_cols = [
        'price_per_sqft', 'total_sqft_clean', 'bhk', 'bath', 
        'loc_target_mean', 'quality_score', 'loc_price_tier'
    ]
    
    # Create temp dataframe with predictions
    df_corr = df[heatmap_cols].copy()
    df_corr['predicted_price'] = y_pred
    
    # Compute correlation
    corr = df_corr.corr()
    
    # Plot Heatmap
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', fmt='.2f',
                linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Feature Correlation Heatmap', fontsize=16)
    plt.tight_layout()
    plt.savefig(results_dir / 'correlation_heatmap.png', dpi=300)
    print(f"  ✓ Saved correlation_heatmap.png")
    
    # =========================================================================
    # 4. PREDICTION ERROR HEATMAP
    # =========================================================================
    print("  Generating prediction error heatmap...")
    
    # Create 2D histogram of Actual vs Predicted
    plt.figure(figsize=(10, 8))
    plt.hist2d(y_actual, y_pred, bins=50, cmap='plasma', range=[[0, 20000], [0, 20000]], cmin=1)
    plt.colorbar(label='Count')
    plt.plot([0, 20000], [0, 20000], 'w--', linewidth=2)  # Diagonal line
    plt.title('Prediction Density Heatmap', fontsize=14)
    plt.xlabel('Actual Price (₹/sqft)', fontsize=12)
    plt.ylabel('Predicted Price (₹/sqft)', fontsize=12)
    plt.tight_layout()
    plt.savefig(results_dir / 'prediction_density.png', dpi=300)
    print(f"  ✓ Saved prediction_density.png")
    
    print("\n✅ All visualizations generated in 'results/' directory.")

if __name__ == "__main__":
    generate_visualizations()
