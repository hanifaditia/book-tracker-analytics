
-- 1. Books Table

CREATE TABLE books (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    genre VARCHAR(100),
    pages INT,
    rating DECIMAL(3,2)
);


-- 2. User Interactions Table

CREATE TABLE user_interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    action VARCHAR(50) CHECK (action IN ('view', 'read', 'complete')),
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id)
);


-- 3. Reading Progress Table

CREATE TABLE reading_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    pages_read INT,
    completion_rate DECIMAL(4,2),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- 4. User Segments Table

CREATE TABLE user_segments (
    user_id INT PRIMARY KEY,
    segment VARCHAR(50),
    total_books_read INT
);
