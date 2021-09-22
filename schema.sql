CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    hashed_password TEXT
);

CREATE TABLE bands (
    id SERIAL PRIMARY KEY,
    band_name TEXT UNIQUE,
    band_description TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE gigs (
    id SERIAL PRIMARY KEY,
    gig_date DATE,
    city TEXT,
    venue TEXT,
    gig_description TEXT,
    band_id INTEGER REFERENCES bands ON DELETE CASCADE
);

CREATE TABLE instruments (
    id SERIAL PRIMARY KEY,
    instrument_name TEXT UNIQUE
);

CREATE TABLE gigsInstruments (
    gig_id INTEGER REFERENCES gigs ON DELETE CASCADE,
    instrument_id INTEGER REFERENCES instruments ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE usersGigs (
    gig_id INTEGER REFERENCES gigs ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    own_gig BOOLEAN
);

CREATE TABLE bandsInstruments (
    instrument_id INTEGER REFERENCES instruments ON DELETE CASCADE,
    band_id INTEGER REFERENCES bands ON DELETE CASCADE
);

CREATE TABLE usersBands (
    band_id INTEGER REFERENCES bands ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

-- CREATE TABLE gigsNeededRoles (
--     instrument_id INTEGER REFERENCES instruments,
--     gig_id INTEGER REFERENCES gigs ON DELETE CASCADE
-- );

INSERT INTO instruments (instrument_name) VALUES ('Kitara');
INSERT INTO instruments (instrument_name) VALUES ('Kitara / Laulu');
INSERT INTO instruments (instrument_name) VALUES ('Basso');
INSERT INTO instruments (instrument_name) VALUES ('Basso / Laulu');
INSERT INTO instruments (instrument_name) VALUES ('Koskettimet');
INSERT INTO instruments (instrument_name) VALUES ('Koskettimet / Laulu');
INSERT INTO instruments (instrument_name) VALUES ('Rummut');
INSERT INTO instruments (instrument_name) VALUES ('Rummut / Laulu');
INSERT INTO instruments (instrument_name) VALUES ('Laulu');
INSERT INTO instruments (instrument_name) VALUES ('Saksofoni');
INSERT INTO instruments (instrument_name) VALUES ('Perkussiot');
INSERT INTO instruments (instrument_name) VALUES ('Perkussiot / Laulu');
INSERT INTO instruments (instrument_name) VALUES ('Klarinetti');
INSERT INTO instruments (instrument_name) VALUES ('None')