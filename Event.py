from database import CursorFromConnectionFromPool

class Event:
    def __init__(self, event_description, event_date, organizer_id, id):
        self.event_description = event_description,
        self.event_date = event_date,
        self.organizer_id = organizer_id,
        self.id = id

    def __repr__(self):
        return "<Event {}".format(self.event_description)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO events (event_description, event_date, organizer_id) VALUES (%s, %s, %s)',
                           (self.event_description, self.event_date, self.organizer_id))

