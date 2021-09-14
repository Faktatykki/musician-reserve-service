CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    hashed_password TEXT
);

CREATE TABLE bands (
    id SERIAL PRIMARY KEY,
    band_name TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE gigs (
    id SERIAL PRIMARY KEY,
    gig_date DATE,
    gig_description TEXT,
    band_id INTEGER REFERENCES bands
);

CREATE TABLE instruments (
    id SERIAL PRIMARY KEY,
    instrument_name TEXT
);

CREATE TABLE usersInstruments (
    instrument_id INTEGER REFERENCES instruments,
    user_id INTEGER REFERENCES users
);

CREATE TABLE usersGigs (
    gig_id INTEGER REFERENCES gigs,
    user_id INTEGER REFERENCES users
);

CREATE TABLE usersBands (
    band_id INTEGER REFERENCES bands,
    user_id INTEGER REFERENCES users
);
