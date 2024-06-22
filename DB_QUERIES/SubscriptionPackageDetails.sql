CREATE TABLE SubscriptionPackageDetails (
    id UUID PRIMARY KEY,
    subscription_id UUID,
    feature_id UUID,
    feature_value VARCHAR(255),
    feature_limit VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES SubscriptionPackages(id),
    FOREIGN KEY (feature_id) REFERENCES Features(id)
);
