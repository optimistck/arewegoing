select FirstSet.event_description, FirstSet.event_date, FirstSet.participant_id, FirstSet.event_footprint, SecondSet.name

from
(
    SELECT event_description, event_date, organizer_id, participant_id, event_footprint
    FROM events
    WHERE event_footprint = '788474'
) as FirstSet
inner join
(
    SELECT name, id
    FROM users
    WHERE id = 2
) as SecondSet
ON FirstSet.organizer_id = SecondSet.id



--this led to decision to create another table to show who is actually going to the event. This will lead to other tables being
--reorganized, and also will allow for historical tracking and may be even post-event information

--UP NEXT: refactor the existing tables to add to the participation table when adding a new entry. And remove participants from the event table.

