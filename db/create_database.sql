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


DROP TABLE IF EXISTS "public"."events" CASCADE;

CREATE TABLE events
(
	id SERIAL PRIMARY KEY,
    event_description text NOT NULL,
    event_date TIMESTAMP NOT NULL,
    organizer_id int4 REFERENCES users(id) NOT NULL,
    event_footprint varchar(9)
);


DROP TABLE IF EXISTS "public"."participation";

CREATE TABLE participation
(
	id SERIAL PRIMARY KEY,
    event_id int4 REFERENCES events(id) NOT NULL,
    joined_date TIMESTAMP default current_timestamp,
    participant_id int4 REFERENCES users(id) NOT NULL
);
