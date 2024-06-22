CREATE TABLE Users (
    id UUID PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    password_hash VARCHAR(255),
    email VARCHAR(255),
    is_verified BIT,
    verification_code VARCHAR(255),
    role_id UUID,
    registiration_date TIMESTAMP,
    is_suspended BOOLEAN,
    is_frozen BOOLEAN,
    frozen_code INT,
    updated_at TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES Roles(id)
);
