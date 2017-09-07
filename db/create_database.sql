DROP TABLE IF EXISTS "public"."users" CASCADE;

CREATE TABLE users
(
	id SERIAL PRIMARY KEY,
	screen_name text,
    oauth_token text,
    oauth_token_secret text,
    name text,
    email text
);


DROP TABLE IF EXISTS "public"."events";

CREATE TABLE events
(
	id SERIAL PRIMARY KEY,
    event_description text NOT NULL,
    event_date TIMESTAMP NOT NULL,
    organizer_id int4 REFERENCES users(id) NOT NULL,
    participant_id text,
    event_footprint varchar(9)
);
