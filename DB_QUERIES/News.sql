CREATE TABLE News (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(1000),
    new_image VARCHAR(255),
    new_link VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
