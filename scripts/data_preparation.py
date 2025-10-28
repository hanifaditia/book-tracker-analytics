# Import library
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os

### Data Cleaning (Python/pandas): ###
# 1. Load book.json
with open('./data/raw/books.json', 'r') as f:
    data = json.load(f)
books = pd.json_normalize(data['books'])

# 2. Data Cleaning
# Drop missing value
books.dropna(subset=['title', 'author'], inplace=True)

# standardize format title, author and genre
books['title'] = books['title'].str.title().str.strip()
books['author'] = books['author'].str.title().str.strip()
books['genre'] = books['genre'].str.title().str.strip()

# Drop duplicate book ID
books = books.drop_duplicates(subset='id')

# Make "processed" directory
os.makedirs("./data/processed", exist_ok=True)

# save to csv
books.to_csv("./data/processed/clean_books.csv", index=False)