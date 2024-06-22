CREATE TABLE EducationsVideoClips (
    id UUID PRIMARY KEY,
    education_id UUID,
    link VARCHAR(250),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (education_id) REFERENCES Educations(id)
);
