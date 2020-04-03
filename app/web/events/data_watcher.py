from sqlalchemy import or_, and_, func
from ..models import db, User, Message
from sqlalchemy.sql.expression import false
from flask_socketio import emit
from flask_login import current_user
from .utils import action_create, connections
from ..utils.decorators import authenticated_only


@authenticated_only
def data_watcher(data):
    data_type = data.get('type')
    if data_type == '@SERVER/GET_USERS':
        data_search = data.get('payload').get('search') or ''
        data_offset = data.get('payload').get('offset') or 0
        search = "%{}%".format(data_search)

        last_messages_subquery = db.session.query(func.max(Message.date))\
            .filter(
                or_(
                    and_(Message.user_from_id == User.id,Message.user_to_id == current_user.id),
                    and_(Message.user_to_id == User.id,Message.user_from_id == current_user.id)
                   )
            ).as_scalar()
        users_query = db.session.query(User.id, User.username, User.online, User.bg, User.img)\
            .filter(User.id != current_user.id, User.username.ilike(search))\
            .order_by(last_messages_subquery.desc())\
            .offset(data_offset)\
            .limit(30)\
            .all()

        users = [c._asdict() for c in users_query]

        count = User.query.filter(User.id != current_user.id, User.username.ilike(search)).count()
        users_get = action_create(action_type='@SERVER/GET_USERS', data=users,
                                  count=count, offset=bool(data_offset), search=data_search)
        emit('data', users_get)

    elif data_type == '@SERVER/GET_CURRENT_USER':
        current = User.query.get(current_user.id).as_dict('id', 'username', 'img')
        current_user_get = action_create(current=current,
                                         action_type='@SERVER/GET_CURRENT_USER')
        emit('data', current_user_get)

    elif data_type == '@SERVER/GET_NOTIFICATIONS':
        notifications = db.session.query(Message.user_from_id, func.count(Message.user_from_id)) \
            .filter(Message.user_to_id == current_user.id, Message.read == false()) \
            .group_by(Message.user_from_id) \
            .all()
        notifications_get = action_create(notifications=dict(notifications),
                                          action_type='@SERVER/GET_NOTIFICATIONS')
        emit('data', notifications_get)

    elif data_type == '@SERVER/GET_MESSAGES_FOR_USER':
        data_user_id = data.get('payload').get('id') or ''
        messages = [c._asdict() for c in
                    db.session.query(Message.id, Message.text, Message.user_from_id, Message.user_to_id, Message.date)
                        .filter(or_(and_(Message.user_from_id == current_user.id, Message.user_to_id == data_user_id),
                                    and_(Message.user_to_id == current_user.id, Message.user_from_id == data_user_id)))
                        .order_by(Message.date)
                        .all()]
        current = User.query.get(current_user.id).as_dict('id', 'username', 'img', 'bg')
        second = User.query.get(data_user_id).as_dict('id', 'username', 'img', 'bg')
        msg_user_get = action_create(data=messages, users={current_user.id: current, data_user_id: second},
                                     selectedUserId=data_user_id, action_type='@SERVER/GET_MESSAGES_FOR_USER')
        emit('data', msg_user_get)
        unread_message_count = Message.query.filter_by(user_from_id=data_user_id, user_to_id=current_user.id).update(
            {'read': True})
        db.session.commit()
        if unread_message_count:
            notification = action_create(action_type='@SERVER/UPDATE_NOTIFICATIONS', notifications={data_user_id: 0})
            emit('data', notification)

    elif data_type == '@SERVER/SET_MESSAGE':
        data_user_id = data.get('payload').get('id')
        data_text = data.get('payload').get('text')
        message = Message(text=data_text, user_from_id=current_user.id, user_to_id=data_user_id)
        db.session.add(message)
        db.session.commit()
        msg_set = action_create(action_type='@SERVER/SET_MESSAGE',
                                text=data_text, user_from_id=current_user.id,
                                user_to_id=data_user_id, id=message.id)
        emit('data', msg_set)
        if connections.has_connections(data_user_id):
            for connection in connections.get(data_user_id):
                emit('data', msg_set, room=connection)

    elif data_type == '@SERVER/SET_MESSAGE_READ':
        message_id = data.get('payload').get('messageId')
        Message.query.filter_by(id=message_id).update(
            {'read': True})
        db.session.commit()
