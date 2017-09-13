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

    def load_participating_in_events(participant_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select FirstSet.id, FirstSet.event_description, FirstSet.event_date from (SELECT event_description, event_date, id FROM events) as FirstSet inner join (SELECT event_id FROM participation WHERE participant_id = %s) as SecondSet ON FirstSet.id = SecondSet.event_id', (participant_id,))
            event_data = cursor.fetchall()
            list_of_events = []
            if event_data:
                for event in event_data:
                    list_of_events.append(event)
                return list_of_events

    def delete_participant_from_event(event_id, paricipant_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('DELETE FROM participation WHERE participant_id = %s AND event_id=%s', (event_id, paricipant_id,))
            #execution_result = cursor.execute()
            rows_deleted = cursor.rowcount
            if rows_deleted:
                return rows_deleted