# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
books = pd.read_csv("./data/processed/clean_books.csv")
interactions = pd.read_csv("./data/processed/user_interactions.csv")
reading = pd.read_csv("./data/processed/reading_progress.csv")
segments = pd.read_csv("./data/processed/user_segments.csv")

# Combine book info and reading activity
reading_full = reading.merge(books, left_on='book_id', right_on='id', how='left')
reading_full = reading_full.merge(segments, on='user_id', how='left')


st.title("Book Analysis Dashboard")

# Book Distribution by Genre (Bar Chart)
st.subheader("Book Distribution by Genre")

genre_counts = books['genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Book Count']

fig1 = px.bar(genre_counts, x='Genre', y='Book Count',
              color='Genre', title='Book Distribution by Genre')
st.plotly_chart(fig1)

# Reading Completion Rates (Histogram)
st.subheader("Distribution of Reading Completion Rates")
fig2 = px.histogram(reading, x='completion_rate', nbins=10,
                    title='Distribution of Reading Completion Rates',
                    labels={'completion_rate': 'Completion Rate'})
st.plotly_chart(fig2)

# Top-Rated Books (Table)
st.subheader("Top-Rated Books")
top_books = books.sort_values('rating', ascending=False).head(10)
st.dataframe(top_books[["title", "author", "rating"]],hide_index=True)

# User Activity Over Time (Line Chart)
st.subheader("User Activity Over Time")
interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])
daily_activity = interactions.groupby(interactions['timestamp'].dt.date)['action'].count().reset_index()
daily_activity.columns = ['Date', 'Activity Count']

fig4 = px.line(daily_activity, x='Date', y='Activity Count',
               title='User Activity Over Time',
               markers=True)
st.plotly_chart(fig4)

# Reader Segmentation Breakdown (Pie Chart)
st.subheader("Reader Segmentation Breakdown")
segment_summary = segments['segment'].value_counts().reset_index()
segment_summary.columns = ['Segment', 'User Count']

fig5 = px.pie(segment_summary, names='Segment', values='User Count',
              title='Reader Segmentation Breakdown',
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig5)

