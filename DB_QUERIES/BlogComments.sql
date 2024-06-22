CREATE TABLE BlogComments (
    id UUID PRIMARY KEY,
    blog_id UUID,
    user_id UUID,
    comment TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (blog_id) REFERENCES blogs(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
