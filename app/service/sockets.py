import socketio

from uuid         import UUID

from app.core     import socket_settinngs
from app.models   import StudyRooms
from app.database import SessionLocal


sio           = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
namespace_url = socket_settinngs.NAMESPACE_URL
db            = SessionLocal()
model         = StudyRooms
clients       = dict()


@sio.event(namespace=namespace_url)
async def connect(sid, environ, auth):
    # Redis 사용자 정보 추가
    clients[sid] = auth['email']
    

@sio.event(namespace=namespace_url)
async def joinRoom(sid, room_id):
    # Redis 사용자가 이용중인 스터디룸 정보 추가
    sio.enter_room(sid=sid, room=room_id, namespace=namespace_url)
    await sio.emit('response', {'message': 'room joined'}, room=room_id, namespace=namespace_url)


@sio.event(namespace=namespace_url)
async def leaveRoom(sid, room_id):
    sio.leave_room(sid=sid, room=room_id, namespace=namespace_url)
    study_room = db.query(model).filter(model.id == UUID(room_id)).update(
        {'current_join_counts': model.current_join_counts - 1}
    )
    if study_room:
        clients.pop(sid)
        db.commit()
        db.close()
        await sio.emit('response', {'message': 'room leaved'}, room=room_id, namespace=namespace_url)
    else:
        await sio.emit('response', {'message': 'database error'}, room=room_id, namespace=namespace_url)


@sio.event(namespace=namespace_url)
async def status(sid, data):
    # Redis 사용자의 학습 상태 정보 추가
    # await sio.emit('response', {'message': 'success'}, room=room_id, namespace=namespace_url)
    pass