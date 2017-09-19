DROP TABLE IF EXISTS "public"."users" CASCADE;

CREATE TABLE users
(
	id SERIAL PRIMARY KEY,
	screen_name varchar(50),
    oauth_token varchar(50),
    oauth_token_secret varchar(50),
    name varchar(50),
    email varchar(40)
);


DROP TABLE IF EXISTS "public"."events" CASCADE;

CREATE TABLE events
(
	id SERIAL PRIMARY KEY,
    event_description text NOT NULL,
    event_date TIMESTAMP NOT NULL,
    organizer_id int4 REFERENCES users(id) NOT NULL,
    event_footprint varchar(9),
    min_participants int2,
    participants_count int2
);


DROP TABLE IF EXISTS "public"."participation";

CREATE TABLE participation
(
	id SERIAL PRIMARY KEY,
    event_id int4 REFERENCES events(id) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL,
    joined_date TIMESTAMP default current_timestamp,
    participant_id int4 REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL
);
