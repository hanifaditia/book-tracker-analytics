-- Most Popular Books by User Interaction Count
SELECT 
    b.title,
    b.author,
    COUNT(ui.interaction_id) AS total_interactions
FROM user_interactions ui
JOIN books b ON ui.book_id = b.id
GROUP BY b.id, b.title, b.author
ORDER BY total_interactions DESC
LIMIT 10;

-- Average Completion Rate by Genre
SELECT 
    b.genre,
    ROUND(AVG(rp.completion_rate), 2) AS avg_completion_rate
FROM reading_progress rp
JOIN books b ON rp.book_id = b.id
GROUP BY b.genre
ORDER BY avg_completion_rate DESC;

-- Average Rating per User Segment
SELECT 
    us.segment,
    ROUND(AVG(b.rating), 2) AS avg_book_rating
FROM user_segments us
JOIN reading_progress rp ON us.user_id = rp.user_id
JOIN books b ON rp.book_id = b.id
GROUP BY us.segment
ORDER BY avg_book_rating DESC;

-- Most Active Users by Interaction Type
SELECT 
    user_id,
    action,
    COUNT(*) AS total_actions
FROM user_interactions
GROUP BY user_id, action
ORDER BY total_actions DESC
LIMIT 10;
