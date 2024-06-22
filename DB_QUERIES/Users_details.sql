CREATE TABLE UserDetails (
    id UUID PRIMARY KEY,
    user_id UUID,
    avatar VARCHAR(250),
    born_date TIMESTAMP,
    horoscope_id UUID,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (horoscope_id) REFERENCES horoscopes(id)
);
