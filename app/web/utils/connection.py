class Connection:
    connection: dict = dict()

    def set(self, user_id, sid):
        if user_id in self.connection:
            self.connection[user_id].append(sid)
        else:
            self.connection[user_id] = [sid]

    def get(self, user_id):
        return self.connection[user_id]

    def delete(self, user_id, sid):
        for key, connect in enumerate(self.connection[user_id]):
            if connect == sid:
                del (self.connection[user_id][key])

    def has_connections(self, user_id):
        return bool(self.connection.get(user_id))
