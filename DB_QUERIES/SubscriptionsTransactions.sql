CREATE TABLE SubscriptionsTransactions (
    id UUID PRIMARY KEY,
    subscription_id UUID,
    payment_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES SubscriptionPackages(id)
);
