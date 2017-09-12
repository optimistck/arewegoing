from database import CursorFromConnectionFromPool

class Participation:
    def __init__(self, event_id, joined_date, participant_id, id):
        self.event_id = event_id,
        self.joined_date = joined_date,
        self.participant_id = participant_id,
        self.id = id

    def __repr__(self):
        return "<Participation {}".format(self.id)

    #needs work ### INCORRECT FROM COPY AND PASTE TO BE EDITED WHEN INSERTING PARTICIPANTS### Also, need one for taking people out.
    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO events (event_description, event_date, organizer_id, event_footprint) VALUES (%s, %s, %s, %s)',
                           (self.event_description, self.event_date, self.organizer_id, self.event_footprint))


    def load_event_participant_names(event_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select SecondSet.name from (SELECT participant_id FROM participation WHERE event_id = %s) as FirstSet inner join (SELECT name, id FROM users) as SecondSet ON FirstSet.participant_id = SecondSet.id', (event_id,))
            event_participants = cursor.fetchall()
            if event_participants:
                return event_participants