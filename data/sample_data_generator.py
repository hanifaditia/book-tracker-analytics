import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os

# load cleaned book data
books = pd.read_csv("./data/processed/clean_books.csv")

# Sample User Interaction Data
actions = ['view', 'reading', 'complete' ]

interactions_data = []

for user in range(10):
    for book_id in books['id']:
        n_actions = random.randint(1, 3) # generate how many interaction for each book
        user_actions = random.sample(actions, n_actions)

        # Store a base date for this user–book pair
        base_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 300))
        
        reading_time = None
        for action in user_actions:
            if action == "reading":
                reading_time = base_date + timedelta(days=random.randint(0, 10))
                interactions_data.append({
                    "user_id": user,
                    "book_id": book_id,
                    "action": action,
                    "timestamp": reading_time.isoformat() + "Z"
                })
            
            elif action == "complete":
                if reading_time:
                    complete_time = reading_time + timedelta(days=random.randint(1, 10))
                else:
                    complete_time = base_date + timedelta(days=random.randint(0, 10))
                interactions_data.append({
                    "user_id": user,
                    "book_id": book_id,
                    "action": action,
                    "timestamp": complete_time.isoformat() + "Z"
                })
            
            else:
                # For other actions (like 'view'), just use a random time
                random_time = base_date + timedelta(days=random.randint(0, 10))
                interactions_data.append({
                    "user_id": user,
                    "book_id": book_id,
                    "action": action,
                    "timestamp": random_time.isoformat() + "Z"
                })

interactions = pd.DataFrame(interactions_data)


# 4. sample reading progress data
reading_data = []
for user in range(10):
    for book_id, total_pages in zip(books['id'], books['pages']):
        pages_read = random.randint(0, total_pages)
        reading_data.append({
            "user_id": user,
            "book_id": book_id,
            "pages_read": pages_read,
            "total_pages": total_pages,
            "completion_rate": round(pages_read / total_pages, 2)
        })

reading_progress = pd.DataFrame(reading_data)



### Data Transformation: ###

# calculate average user complition rate
user_completion = reading_progress.groupby('user_id')['completion_rate'].mean().reset_index()
user_completion.rename(columns={'completion_rate': 'avg_completion_rate'}, inplace=True)

# Reading Speed (pages/day)
read_actions = interactions[interactions['action'] == 'reading']
complete_actions = interactions[interactions['action'] == 'complete']
start_dates = (
    read_actions.groupby(['user_id', 'book_id'])
    .agg(start_date=('timestamp', 'min'))
    .reset_index()
)
end_dates = (
    complete_actions.groupby(['user_id', 'book_id'])
    .agg(end_date=('timestamp', 'min'))
    .reset_index()
)

start_end_dates = pd.merge(start_dates, end_dates, on=['user_id', 'book_id'], how='inner')

#Convert to datetime
start_end_dates['start_date'] = pd.to_datetime(start_end_dates['start_date'], utc=True)
start_end_dates['end_date'] = pd.to_datetime(start_end_dates['end_date'], utc=True)

# calculate day spent for reading the book
start_end_dates['days_spent'] = (start_end_dates['end_date'] - start_end_dates['start_date']).dt.days


reading_data_with_dates = pd.merge(start_end_dates, reading_progress, on=['user_id', 'book_id'], how='left')

reading_data_with_dates['reading_speed'] = (
    reading_data_with_dates['pages_read'] / reading_data_with_dates['days_spent']
)

reading_data_with_dates['reading_speed'] = reading_data_with_dates['reading_speed'].replace([float('inf'), -float('inf')], None)
reading_data_with_dates.loc[reading_data_with_dates['days_spent'] <= 0, 'reading_speed'] = None

# user segments based on reading behavior
def segment_user(rate):
    if rate >= 0.8:
        return 'Bookworm  Reader'
    elif rate >= 0.4:
        return 'Moderate Reader'
    else:
        return 'Casual Reader'

user_completion['segment'] = user_completion['avg_completion_rate'].apply(segment_user)


# Aggregate Data for Dashboard


# User summary data

# 1. Calculate total pages read by each user
total_pages_read = reading_progress.groupby('user_id')['pages_read'].sum().reset_index()
total_pages_read.rename(columns={'pages_read': 'total_pages_read'}, inplace=True)

# 2. Calculate total books completed by each user
total_books_completed = interactions[interactions['action'] == 'complete'].groupby('user_id')['book_id'].nunique().reset_index()
total_books_completed.rename(columns={'book_id': 'total_books_completed'}, inplace=True)

# 3. Merge user completion rates and segments
user_summary = pd.merge(user_completion, total_pages_read, on='user_id', how='left')
user_summary = pd.merge(user_summary, total_books_completed, on='user_id', how='left')

# 4. Calculate average reading speed for each user (from the 'reading_data_with_dates' dataframe)
user_avg_speed = reading_data_with_dates.groupby('user_id')['reading_speed'].mean().reset_index()
user_avg_speed.rename(columns={'reading_speed': 'avg_reading_speed'}, inplace=True)

# Merge reading speed
user_summary = pd.merge(user_summary, user_avg_speed, on='user_id', how='left')

# 5. Identify most read genre for each user
most_read_genres = interactions.merge(books[['id', 'genre']], left_on='book_id', right_on='id', how='left')
most_read_genres = most_read_genres.groupby('user_id')['genre'].agg(lambda x: x.mode()[0]).reset_index()
most_read_genres.rename(columns={'genre': 'most_read_genre'}, inplace=True)

# Merge most read genre
user_summary = pd.merge(user_summary, most_read_genres, on='user_id', how='left')


# Save to CSV

# Make "processed" directory
os.makedirs("./data/processed", exist_ok=True)

interactions.to_csv("./data/processed/user_interactions.csv", index=False)
reading_progress.to_csv("./data/processed/reading_progress.csv", index=False)

# Transformation data
user_completion.to_csv("./data/processed/user_segments.csv", index=False)
reading_data_with_dates.to_csv('./data/processed/reading_data_with_speed.csv', index=False)

# User summary data
user_summary.to_csv('./data/processed/user_summary.csv', index=False)