# Recommended Dataset Sources

This document lists recommended datasets for populating the data folders.

## Insect Images

- **Dataset:** IP102 - A Large-Scale Benchmark Dataset for Insect Pest Recognition
- **Source:** [https://github.com/xpwu95/IP102](https://github.com/xpwu95/IP102)
- **Notes:** This dataset contains over 75,000 images of 102 insect species. Download and split into `train/` and `val/` directories.

## Insect Sounds

- **Dataset:** USDA Bug Bytes
- **Source:** (Search for "USDA Bug Bytes dataset")
- **Notes:** A collection of insect sounds from the USDA. May require some processing to be useful.

## Animal Images

- **Dataset:** Open Images Dataset V7
- **Source:** [https://storage.googleapis.com/openimages/web/index.html](https://storage.googleapis.com/openimages/web/index.html)
- **Notes:** A very large dataset containing millions of images. Filter for animal classes.

- **Dataset:** Kaggle Animal Detection Datasets
- **Source:** [https://www.kaggle.com/datasets?search=animal+detection](https://www.kaggle.com/datasets?search=animal+detection)
- **Notes:** Many smaller, more focused datasets available on Kaggle.

## Grape Disease Images

- **Dataset:** Niphad Grape Leaf Disease Dataset (NGLD)
- **Source:** [https://data.mendeley.com/datasets/8nnd2ypcv3/5](https://data.mendeley.com/datasets/8nnd2ypcv3/5)
- **Notes:** 2726 high-quality grape leaf images with Downy Mildew, Powdery Mildew, Bacterial Leaf Spot, and Healthy leaves. From Nashik, India.
- **Download:** Click "Download All" on the Mendeley page, extract to `grape_diseases/` folder

- **Dataset:** Grape Disease Dataset (Environmental Parameters)
- **Source:** [https://data.mendeley.com/datasets/94j4ws2325/1](https://data.mendeley.com/datasets/94j4ws2325/1)
- **Notes:** 10,000 records with temperature, humidity, leaf wetness for predicting Powdery Mildew, Downy Mildew, Bacterial Leaf Spot.
- **Download:** Click "Download All" on the Mendeley page, extract CSV to `grape_diseases/environmental_data/`

- **Dataset:** Grapevine Disease Dataset (Original)
- **Source:** [https://www.kaggle.com/datasets/rm1000/grape-disease-dataset-original](https://www.kaggle.com/datasets/rm1000/grape-disease-dataset-original)
- **Notes:** 9027 images of Black Rot, ESCA, Leaf Blight, Healthy grape plants.
- **Download:** Download from Kaggle and organize into train/val folders with disease categories
