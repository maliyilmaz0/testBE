CREATE TABLE EducationTransactions (
    id UUID PRIMARY KEY,
    payment_id UUID,
    education_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (payment_id) REFERENCES Payments(id),
    FOREIGN KEY (education_id) REFERENCES Educations(id)
);
