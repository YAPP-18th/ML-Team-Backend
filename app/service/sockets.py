from app.service.auth import check_access_token_valid
import socketio

from uuid         import UUID
from fastapi.encoders import jsonable_encoder

from app.core     import socket_settinngs
from app.service  import check_access_token_valid
from app.models   import StudyRooms
from app.database import SessionLocal


sio           = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
namespace_url = socket_settinngs.NAMESPACE_URL
db            = SessionLocal()
model         = StudyRooms


@sio.event(namespace=namespace_url)
async def connect(sid, environ, auth):
    print('sid: ', sid)
    print('token: ', auth)
    # token = auth['access_token']
    # email = check_access_token_valid(token)
    # await sio.save_session(sid, {'user_email': email}, namespace=namespace_url)


@sio.event(namespace=namespace_url)
async def joinRoom(sid, room_id):
    sio.enter_room(sid=sid, room=room_id, namespace=namespace_url)
    print(sio.rooms(sid=sid, namespace=namespace_url))
    # session = await sio.get_session(sid, namespace=namespace_url)
    await sio.emit('response', {'message': 'room joined'}, room=room_id, namespace=namespace_url)
    print(sio.rooms(sid=sid, namespace=namespace_url))


@sio.event(namespace=namespace_url)
async def leaveRoom(sid, room_id):
    print('sid: ', sid)
    print('room_id: ', room_id)
    print('leave')
    print(sio.rooms(sid=sid, namespace=namespace_url))
    sio.leave_room(sid=sid, room=room_id, namespace=namespace_url)
    print(sio.rooms(sid=sid, namespace=namespace_url))
    study_room = db.query(model).filter(model.id == UUID(room_id)).update(
        {'current_join_counts': model.current_join_counts - 1}
    )
    if study_room:
        db.commit()
        db.close()
        print('here')
        await sio.emit('response', {'message': 'room leaved'}, room=room_id, namespace=namespace_url)
        print('emit done')
    else:
        await sio.emit('response', {'message': 'error'}, room=room_id, namespace=namespace_url)


@sio.event(namespace=namespace_url)
async def status(sid, data):
    # Redis
    pass