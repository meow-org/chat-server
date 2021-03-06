import json
import datetime


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.strftime('%Y-%m-%d %H:%M')


def action_create(action_type, **kwargs):
    return json.dumps({'forType': action_type, 'payload': kwargs}, default=default)


class Connection:
    connection: dict = dict()

    def set(self, user_id, sid):
        try:
            self.connection[user_id].append(sid)
        except KeyError:
            self.connection[user_id] = [sid]

    def get(self, user_id):
        return self.connection[user_id]

    def delete(self, user_id, sid):
        for key, connect in enumerate(self.connection[user_id]):
            if connect == sid:
                del (self.connection[user_id][key])

    def has_connections(self, user_id):
        return bool(self.connection.get(user_id))


connections = Connection()
