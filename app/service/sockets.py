import socketio
import traceback

from datetime               import datetime
from sqlalchemy.orm.session import Session

from app.core               import socket_settings
from app.crud               import study_rooms, reports, my_studies
from app.database           import SessionLocal
from app.core               import time_settings


db            = SessionLocal()
sio           = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', debug=True)
namespace_url = socket_settings.NAMESPACE_URL
clients       = dict()


@sio.event(namespace=namespace_url)
async def connect(sid, environ, auth):
    # TODO: Redis 사용자 정보 추가
    try:
        today        = datetime.utcnow() + time_settings.KST
        instance     = reports.get_or_create(db=db, today=today, user_id=1)
        clients[sid] = {
            'user_id': auth['user_id'],
            'report_id':  instance['id'],
            'my_study_id': ''
        }

    except Exception as error:
        print(traceback.print_exc())    

@sio.event(namespace=namespace_url)
async def joinRoom(sid, room_id):
    # TODO: Redis 사용자가 이용중인 스터디룸 정보 추가
    try:
        sio.enter_room(sid=sid, room=room_id, namespace=namespace_url)
        instance = my_studies.create(
            db         = db,
            room_id    = room_id,
            started_at = time_settings.KOR_NOW,
            report_id  = clients[sid]['report_id']
        )
        clients[sid]['my_study_id'] = instance['id']
        await sio.emit(
            'response',
            {'message': 'room joined'},
            room      = room_id,
            namespace = namespace_url
        )
    
    except Exception as error:
        print(traceback.print_exc())



@sio.event(namespace=namespace_url)
async def leaveRoom(sid, room_id, db: Session = db):
    try:
        # TODO: 축적된 학습 데이터 Redis > PostgreSQL 이동 필요
        message = study_rooms.leave(db, room_id=room_id)
        sio.leave_room(sid=sid, room=room_id, namespace=namespace_url)
        my_studies.update(
            db          = db,
            ended_at    = time_settings.KOR_NOW,
            disturbance = '',
            id          = clients[sid]['my_study_id']
        )
        reports.update()
        clients.pop(sid)
        await sio.emit(
            'response',
            {'message': message},
            room      = room_id,
            namespace = namespace_url
        )
        
    except Exception as error:
        print(traceback.print_exc())
        await sio.emit(
            'response',
            {'message': error},
            room      = room_id,
            namespace = namespace_url
        )



@sio.event(namespace=namespace_url)
async def status(sid, disturbance):
    # TODO
    # - Redis 사용자의 학습 상태 정보 추가
    # - 넘어 온 상태에 따른 emit > 어떤 사용자가 어떤 상태인지 보내줄 것
    # print(conn.lrange(clients[sid], 0, -1).decode())
    # await sio.emit('response', {'message': 'success'}, room=room_id, namespace=namespace_url)
    pass    
