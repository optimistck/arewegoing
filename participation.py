from database import CursorFromConnectionFromPool

class Participation:
    def __init__(self, event_id, joined_date, participant_id, id):
        self.event_id = event_id,
        self.joined_date = joined_date,
        self.participant_id = participant_id,
        self.id = id

    def __repr__(self):
        return "<Participation {}".format(self.id)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO participation (event_id, participant_id) VALUES (%s, %s)',
                           (self.event_id, self.participant_id))


    def load_event_participant_names(event_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select SecondSet.name from (SELECT participant_id FROM participation WHERE event_id = %s) as FirstSet inner join (SELECT name, id FROM users) as SecondSet ON FirstSet.participant_id = SecondSet.id', (event_id,))
            event_participants = cursor.fetchall()
            if event_participants:
                return event_participants