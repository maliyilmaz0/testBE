CREATE TABLE Educations (
    id UUID PRIMARY KEY,
    education_name VARCHAR(250),
    education_description TEXT,
    price DECIMAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
