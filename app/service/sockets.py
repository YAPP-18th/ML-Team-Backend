import socketio

from sqlalchemy.orm.session import Session

from app.core               import socket_settinngs
from app.crud               import study_rooms
from app.database           import SessionLocal


db            = SessionLocal()
sio           = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', debug=True)
namespace_url = socket_settinngs.NAMESPACE_URL
clients       = dict()



@sio.event(namespace=namespace_url)
async def connect(sid, environ, auth):
    # TODO: Redis 사용자 정보 추가
    clients[sid] = auth['email']
    

@sio.event(namespace=namespace_url)
async def joinRoom(sid, room_id):
    # TODO: Redis 사용자가 이용중인 스터디룸 정보 추가
    sio.enter_room(sid=sid, room=room_id, namespace=namespace_url)
    await sio.emit('response', {'message': 'room joined'}, room=room_id, namespace=namespace_url)


@sio.event(namespace=namespace_url)
async def leaveRoom(sid, room_id, db: Session = db):
    try:
        # TODO: 축적된 학습 데이터 Redis > PostgreSQL 이동 필요
        message = study_rooms.leave(db, room_id=room_id)
        await sio.leave_room(sid=sid, room=room_id, namespace=namespace_url)
        clients.pop(sid)
        await sio.emit('response', {'message': message}, room=room_id, namespace=namespace_url)
        
    except Exception as error:
        await sio.emit('response', {'message': error}, room=room_id, namespace=namespace_url)


@sio.event(namespace=namespace_url)
async def status(sid, data):
    # TODO: Redis 사용자의 학습 상태 정보 추가
    # await sio.emit('response', {'message': 'success'}, room=room_id, namespace=namespace_url)
    pass