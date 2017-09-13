from database import CursorFromConnectionFromPool

class Event:
    def __init__(self, event_description, event_date, organizer_id, event_footprint, id):
        self.event_description = event_description,
        self.event_date = event_date,
        self.organizer_id = organizer_id,
        self.event_footprint = event_footprint,
        self.id = id

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
            cursor.execute('INSERT INTO events (event_description, event_date, organizer_id, event_footprint) VALUES (%s, %s, %s, %s)',
                           (self.event_description, self.event_date, self.organizer_id, self.event_footprint))

    @classmethod
    def load_from_db_by_organizer_id(cls, organizer_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM events WHERE organizer_id=%s', (organizer_id,))
            event_data = cursor.fetchone()
            #but we really need to fetch more than one in the future! Not just the first one.
            if event_data:
                return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=[3], event_footprint=event_data[4], id=event_data[0])

    @classmethod
    def load_event_from_db_by_event_footprint(cls, event_footprint):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from events where event_footprint = %s', (event_footprint,))
            event_data = cursor.fetchone()
            if event_data:
                return cls(event_description=event_data[1], event_date=event_data[2], organizer_id=event_data[3], event_footprint=event_data[4], id=event_data[0], )


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
