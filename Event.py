from database import CursorFromConnectionFromPool

class Event:
    def __init__(self, event_description, event_date, organizer_id, event_footprint, id, min_participants, participants_count):
        self.event_description = event_description,
        self.event_date = event_date,
        self.organizer_id = organizer_id,
        self.event_footprint = event_footprint,
        self.id = id,
        self.min_participants = min_participants,
        self.participants_count = participants_count


    def __repr__(self):
        return "<Event {}".format(self.event_description)

    def json(self):
        return {
            'event_description': self.name,
            'event_date': self.genre,
            'organizer_id': self.watched,
            'event_footprint': self.event_footprint,
            'id': self.id
        }

    @classmethod
    def from_json(cls, json_data):
        return Event(**json_data)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO events (event_description, event_date, organizer_id, event_footprint, min_participants, participants_count) VALUES (%s, %s, %s, %s, %s, %s)',
                           (self.event_description, self.event_date, self.organizer_id, self.event_footprint, self.min_participants, 0))

    @classmethod
    def load_from_db_by_organizer_id(cls, organizer_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM events WHERE organizer_id=%s', (organizer_id,))
            event_data = cursor.fetchone()
            #but we really need to fetch more than one in the future! Not just the first one.
            if event_data:
                return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=[3], event_footprint=event_data[4], id=event_data[0], min_participants=event_data[5], participants_count=event_data[6],)

    @classmethod
    def load_event_from_db_by_event_footprint(cls, event_footprint):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from events where event_footprint = %s', (event_footprint,))
            event_data = cursor.fetchone()
            if event_data:
                return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=event_data[3], event_footprint=event_data[4], id=event_data[0], min_participants=event_data[5], participants_count=event_data[6],)
    @classmethod
    def load_event_from_db_by_event_id(cls, id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from events where id = %s', (id,))
            event_data = cursor.fetchone()
            if event_data:
                return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=event_data[3], event_footprint=event_data[4], id=event_data[0], min_participants=event_data[5], participants_count=event_data[6],)


    def workbench_load_all_events():
        ## GOAL: take the output of the database, and put it into a JSON or a list to present to the web page. LIST!
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM events')
            event_data = cursor.fetchall()
            list_of_events = []
            #but we really need to fetch more than one in the future! Not just the first one.
            if event_data:
                # iterate over the events data and return JSON
                for event in event_data:
                    list_of_events.append(event)
                return list_of_events
                #return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=[3], event_footprint=event_data[4], id=event_data[0])

    def load_from_db_all_events_by_organizer_id(organizer_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM events WHERE organizer_id=%s', (organizer_id,))
            event_data = cursor.fetchall()
            list_of_events = []
            if event_data:
                for event in event_data:
                    list_of_events.append(event)
                return list_of_events

    def delete_event(event_id, organizer_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('DELETE FROM events WHERE id = %s AND organizer_id=%s', (event_id, organizer_id,))
            #execution_result = cursor.execute()
            rows_deleted = cursor.rowcount
            if rows_deleted:
                return rows_deleted

    def get_event_id_from_event_footprint(event_footprint):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT id FROM events WHERE event_footprint = %s', (event_footprint,))
            event_id = cursor.fetchone()
            if event_id:
                return event_id

        #UPDATE events SET participants_count = participants_count + 1 WHERE id = 12
    def add_one_to_event(event_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('UPDATE events SET participants_count = participants_count + 1 WHERE id = %s', (event_id,))
            # rows_deleted = cursor.rowcount
            # if rows_deleted:
            #     return rows_deleted
