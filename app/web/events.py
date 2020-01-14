from flask_socketio import SocketIO, emit
from flask_login import current_user
from .models import Message, db
import json

socketio = SocketIO(engineio_logger=True)


@socketio.on('messages', namespace='/websocket/chat')
def text(message):
    message_db = Message(user_id=current_user.id, text=message)
    db.session.add(message_db)
    db.session.commit()
    emit('messages', json.dumps({'username': current_user.username, 'text': message}))
