from flask_socketio import SocketIO, emit
from flask import request
from flask_login import current_user
from ..models import Message, User, db
from ..utils.connection import Connection
from sqlalchemy import or_, and_, func
from sqlalchemy.sql.expression import false
import json

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
            emit('data', action_create(action_type='@SERVER/USER_CONNECT', id=current_user.id), broadcast=True)


@socket_io.on('disconnect', namespace='/websocket/chat')
def disconnect_user():
    if current_user.id is not None:
        user = User.query.get(current_user.id)
        connections.delete(current_user.id, request.sid)
        if connections.has_connections(current_user.id) is False:
            user.set_online(False)
            db.session.add(user)
            db.session.commit()
            emit('data', action_create(action_type='@SERVER/USER_DISCONNECT', id=current_user.id), broadcast=True)


@socket_io.on('data', namespace='/websocket/chat')
def data_watcher(data):
    data_type = data.get('type')
    if data_type == '@SERVER/GET_USERS':
        data_search = data.get('payload').get('search') or ''
        data_offset = data.get('payload').get('offset') or 0
        search = "%{}%".format(data_search)

        users = [c._asdict() for c in
                 db.session.query(User.id, User.username, User.online, User.bg, User.img)
                     .filter(User.id != current_user.id, User.username.ilike(search))
                     .offset(data_offset)
                     .limit(30)
                     .all()]

        count = User.query.filter(User.id != current_user.id, User.username.ilike(search)).count()
        emit('data', action_create(
            action_type='@SERVER/GET_USERS',
            data=users,
            count=count,
            offset=bool(data_offset),
            search=data_search
        ))
    if data_type == '@SERVER/GET_CURRENT_USER':
        current = User.query.get(current_user.id).as_dict('id', 'username', 'img')
        emit('data', action_create(
            current=current,
            action_type='@SERVER/GET_CURRENT_USER'
        ))

    if data_type == '@SERVER/GET_NOTIFICATIONS':
        notifications = db.session.query(Message.user_from_id, func.count(Message.user_from_id))\
            .filter(Message.user_to_id == current_user.id, Message.read == false())\
            .group_by(Message.user_from_id)\
            .all()
        emit('data', action_create(
            notifications=dict(notifications),
            action_type='@SERVER/GET_NOTIFICATIONS'
        ))

    if data_type == '@SERVER/GET_MESSAGES_FOR_USER':
        data_user_id = data.get('payload').get('id') or ''
        messages = [c._asdict() for c in
                    db.session.query(Message.id, Message.text, Message.user_from_id, Message.user_to_id)
                        .filter(or_(and_(Message.user_from_id == current_user.id, Message.user_to_id == data_user_id),
                                    and_(Message.user_to_id == current_user.id, Message.user_from_id == data_user_id)))
                        .all()]
        current = User.query.get(current_user.id).as_dict('id', 'username', 'img', 'bg')
        second = User.query.get(data_user_id).as_dict('id', 'username', 'img', 'bg')
        emit('data', action_create(
            data=messages,
            users={current_user.id: current, data_user_id: second},
            selectedUserId=data_user_id,
            action_type='@SERVER/GET_MESSAGES_FOR_USER'
        ))

    if data_type == '@SERVER/SET_MESSAGE':
        data_user_id = data.get('payload').get('id')
        data_text = data.get('payload').get('text')
        message = Message(text=data_text, user_from_id=current_user.id, user_to_id=data_user_id)
        db.session.add(message)
        db.session.commit()
        action = action_create(
            action_type='@SERVER/SET_MESSAGE',
            text=data_text,
            user_from_id=current_user.id,
            user_to_id=data_user_id,
            id=message.id
        )
        emit('data', action)
        if connections.has_connections(data_user_id):
            for connection in connections.get(data_user_id):
                connection.emit('data', action)
