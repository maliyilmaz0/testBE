CREATE TABLE SubscriptionPackages (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL,
    is_active BOOLEAN,
    created_at TIMESTAMP
);
