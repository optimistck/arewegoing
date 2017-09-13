select FirstSet.event_description, FirstSet.event_date, FirstSet.event_footprint, SecondSet.name

from
(
    SELECT event_description, event_date, organizer_id, event_footprint
    FROM events
    WHERE event_footprint = '672370'
) as FirstSet
inner join
(
    SELECT name, id
    FROM users
    WHERE id = 3
) as SecondSet
ON FirstSet.organizer_id = SecondSet.id



-- Give me all the participants
select SecondSet.name, FirstSet.participant_id

from
(
    SELECT participant_id
    FROM participation
    WHERE event_id = 3
) as FirstSet
inner join
(
    SELECT name, id
    FROM users
) as SecondSet
ON FirstSet.participant_id = SecondSet.id


-- Give me all the events for which I'm a participant
-- TO DO
select SecondSet.name, FirstSet.participant_id

from
(
    SELECT participant_id
    FROM participation
    WHERE event_id = 3
) as FirstSet
inner join
(
    SELECT name, id
    FROM users
) as SecondSet
ON FirstSet.participant_id = SecondSet.id



--get the event_id out of the participant table based on the participant_id and join on the events table to show event details.

select FirstSet.id, FirstSet.event_description, FirstSet.event_date
from
(
    SELECT event_description, event_date, id
    FROM events
) as FirstSet
inner join
(
    SELECT event_id
    FROM participation
    WHERE participant_id = 6
) as SecondSet
ON FirstSet.id = SecondSet.event_id





--this led to decision to create another table to show who is actually going to the event. This will lead to other tables being
--reorganized, and also will allow for historical tracking and may be even post-event information

--UP NEXT: refactor the existing tables to add to the participation table when adding a new entry. And remove participants from the event table.

select * from events

INSERT INTO events (event_description, event_date, organizer_id, event_footprint) VALUES ('hi', '2018-1-1', '3', 232442)

INSERT INTO participation (event_id, joined_date, participant_id) VALUES (9, '2017-09-12', 4)