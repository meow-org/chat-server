from flask_socketio import SocketIO, emit
from flask import request
from flask_login import current_user
from ..models import User, db
from ..utils.connection import Connection
import json
from .data_watcher_callables import get_users, get_current_user, get_notifications,\
                                   get_user_msgs, set_msg

connections = Connection()

socket_io = SocketIO(engineio_logger=True)


def action_create(action_type, **kwargs):
    return json.dumps({'forType': action_type, 'payload': kwargs})


@socket_io.on('connect', namespace='/websocket/chat')
def connect_user():
    if current_user.id is not None:
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
    if current_user.id is not None:
        user = User.query.get(current_user.id)
        connections.delete(current_user.id, request.sid)
        if connections.has_connections(current_user.id) is False:
            user.set_online(False)
            db.session.add(user)
            db.session.commit()
            user_disconnect = action_create(action_type='@SERVER/USER_DISCONNECT', id=current_user.id)
            emit('data', user_disconnect, broadcast=True)


@socket_io.on('data', namespace='/websocket/chat')
def data_watcher(data):
    #where from does this function get User???????????!
    #data_type is some single thing?? I changed multiple if to if, elif... else
    data_type = data.get('type')
    if data_type == '@SERVER/GET_USERS':
        get_users(data)
    elif data_type == '@SERVER/GET_CURRENT_USER':
        get_current_user(data)
    elif data_type == '@SERVER/GET_NOTIFICATIONS':
        get_notifications(data)
    elif data_type == '@SERVER/GET_MESSAGES_FOR_USER':
        get_user_msgs(data)
    elif data_type == '@SERVER/SET_MESSAGE':
        set_msg(data)