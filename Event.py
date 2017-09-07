from database import CursorFromConnectionFromPool

class Event:
    def __init__(self, event_description, event_date, organizer_id, participant_id, event_footprint, id):
        self.event_description = event_description,
        self.event_date = event_date,
        self.organizer_id = organizer_id,
        self.participant_id = participant_id,
        self.event_footprint = event_footprint,
        self.id = id

    def __repr__(self):
        return "<Event {}".format(self.event_description)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO events (event_description, event_date, organizer_id, participant_id, event_footprint) VALUES (%s, %s, %s, %s, %s)',
                           (self.event_description, self.event_date, self.organizer_id, self.participant_id, self.event_footprint))

    @classmethod
    def load_from_db_by_organizer_id(cls, organizer_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM events WHERE organizer_id=%s', (organizer_id,))
            event_data = cursor.fetchone()
            #but we really need to fetch more than one in the future! Not just the first one.
            if event_data:
                return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=[3], id=event_data[0])