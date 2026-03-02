#!/usr/bin/env python3
"""
Dataset Organization Script for Grape Disease Detection
This script helps organize downloaded grape disease datasets into the proper structure.
"""

import os
import shutil
import pandas as pd
from pathlib import Path

def organize_grape_datasets(base_path):
    """
    Organize grape disease datasets into train/val structure
    """
    base_path = Path(base_path)

    # Create directories if they don't exist
    categories = [
        'healthy', 'downy_mildew', 'powdery_mildew', 'bacterial_leaf_spot',
        'black_rot', 'esca', 'leaf_blight'
    ]

    for split in ['train', 'val']:
        for category in categories:
            (base_path / split / category).mkdir(parents=True, exist_ok=True)

    print("Directory structure created successfully!")

    # Check for environmental data
    env_data_path = base_path / "environmental_data"
    if env_data_path.exists():
        csv_files = list(env_data_path.glob("*.csv"))
        if csv_files:
            print(f"Found environmental dataset: {csv_files[0]}")
            # Load and show basic info
            df = pd.read_csv(csv_files[0])
            print(f"Dataset shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("Sample data:")
            print(df.head())
        else:
            print("No CSV files found in environmental_data folder")
    else:
        print("Environmental data folder not found")

    print("\nNext steps:")
    print("1. Download image datasets from the sources listed in README.md")
    print("2. Extract images into appropriate train/val/category folders")
    print("3. Run your ML training scripts with the organized data")

if __name__ == "__main__":
    # Run from datasets/grape_diseases directory
    current_dir = Path(__file__).parent
    organize_grape_datasets(current_dir)