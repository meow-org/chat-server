from flask_socketio import SocketIO, emit
from flask import request
from flask_login import current_user
from ..models import User, db
from .data_watcher import data_watcher
from .utils import action_create, connections
from ..utils.decorators import authenticated_only

socket_io = SocketIO(engineio_logger=True)


@socket_io.on('connect', namespace='/websocket/chat')
@authenticated_only
def connect_user():
    connections.set(current_user.id, request.sid)
    user = User.query.get(current_user.id)
    if user.online is not True:
        user.set_online(True)
        db.session.add(user)
        db.session.commit()
        user_connect = action_create(action_type='@SERVER/USER_CONNECT', id=current_user.id)
        emit('data', user_connect, broadcast=True)


@socket_io.on('disconnect', namespace='/websocket/chat')
def disconnect_user():
    user = User.query.get(current_user.id)
    connections.delete(current_user.id, request.sid)
    if connections.has_connections(current_user.id) is False:
        user.set_online(False)
        db.session.add(user)
        db.session.commit()
        user_disconnect = action_create(action_type='@SERVER/USER_DISCONNECT', id=current_user.id)
        emit('data', user_disconnect, broadcast=True)


socket_io.on_event('data', data_watcher, namespace='/websocket/chat')
