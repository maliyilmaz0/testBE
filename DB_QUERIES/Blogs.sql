CREATE TABLE Blogs (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    text TEXT,
    like_count INT,
    dislike_count INT,
    label_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
