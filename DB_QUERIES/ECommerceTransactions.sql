CREATE TABLE ECommerceTransactions (
    id UUID PRIMARY KEY,
    payment_id UUID,
    order_id UUID,
    product_id UUID,
    quantity INT,
    total_price DECIMAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (payment_id) REFERENCES Payments(id),
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);
