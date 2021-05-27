import traceback
import socketio

from sqlalchemy.orm.session import Session

from app.core               import socket_settings
from app.crud               import (
                                study_rooms,
                                reports,
                                my_studies,
                                disturbances
                            )
from app.database           import SessionLocal


db            = SessionLocal()
sio           = socketio.AsyncServer(
    async_mode           = 'asgi',
    cors_allowed_origins = '*',
    debug                = True
)
namespace_url = socket_settings.NAMESPACE_URL
clients       = dict()


@sio.event(namespace=namespace_url)
async def connect(sid, environ, auth):
    try:
        instance     = reports.get_or_create(
            db      = db,
            user_id = auth['user_id']
        )
        clients[sid] = {
            'user_id': auth['user_id'],
            'report_id':  instance['id'],
            'my_study_id': ''
        }
        await sio.emit(
            'response',
            {'message': 'connect success'},
            namespace = namespace_url
        )

    except Exception as error:
        print(traceback.print_exc())    
        await sio.emit(
            'response',
            {'message': f'server error {error}'},
            namespace = namespace_url
        )        


@sio.event(namespace=namespace_url)
async def joinRoom(sid, room_id, db: Session = db):
    try:
        sio.enter_room(sid=sid, room=room_id, namespace=namespace_url)
        instance = my_studies.create(
            db         = db,
            room_id    = room_id,
            report_id  = clients[sid]['report_id']
        )
        clients[sid]['my_study_id'] = instance['id']
        await sio.emit(
            'response',
            {'message': 'join success'},
            room      = room_id,
            namespace = namespace_url
        )
    
    except Exception as error:
        print(traceback.print_exc())
        await sio.emit(
            'response',
            {'message': f'server error {error}'},
            room      = room_id,
            namespace = namespace_url
        )        


@sio.event(namespace=namespace_url)
async def leaveRoom(sid, room_id, db: Session = db):
    try:
        """
        Todo
        - Disturbance 테이블 생성 필요
        - Redis 넘겨 받는 데이터의 형태에 따라 구현 메서드 변경
        - bulk_insert_mappings 사용시 속도는 훨씬 빠르다.
          하지만 배열 형태의 데이터가 들어가야 하며 각 리스트에는 객체로 disturbance 데이터가 들어가야 한다.
          또한 객체 내에 report_id 와 my_study_id 에 대한 정보도 포함되어 있어야 한다.
          ex. [ {type: smartphone, time: 124, count: 2, report_id: 1, my_study_id: 2}, ... ]
        - update_or_create 사용시 속도는 훨씬 느리다. (개별적인 데이터에 for loop을 돌려야 하기 때문)
          이때 장점은 type과 time만 Redis에서 get 하면 된다는 점이다.
        - report_id, my_study_id는 이미 글로벌하게 clients 객체에 저장되어 있다.
        """

        # disturbances.create(db, disturbances) > disturbances 부분이 Redis에서 get 한 Array[JSON]

        study_rooms.leave(db, room_id=room_id)
        sio.leave_room(sid=sid, room=room_id, namespace=namespace_url)

        instance = my_studies.update(
            db          = db,
            id          = clients[sid]['my_study_id']
        )
        reports.update(
            db         = db,
            id         = clients[sid]['report_id'],
            total_time = instance['total_time']
        )
        
        clients.pop(sid)
        await sio.emit(
            'response',
            {'message': 'leave success'},
            room      = room_id,
            namespace = namespace_url
        )
        
    except Exception as error:
        print(traceback.print_exc())
        await sio.emit(
            'response',
            {'message': f'server error {error}'},
            room      = room_id,
            namespace = namespace_url
        )


@sio.event(namespace=namespace_url)
async def status(sid, disturbance):
    try:
        """
        TODO:
        - Client에서 disturbance 데이터에 room_id 포함하여 줘야 한다.
        - response 이벤트로 message에 disturbance 상태를 보내줘야 한다.
        """

        await sio.emit(
            'response',
            {'message': ''},
            room      = disturbance['room_id'],
            namespace = namespace_url
        )

    except Exception as error:
        print(traceback.print_exc())
        await sio.emit(
            'response',
            {'message': f'server error {error}'},
            room      = disturbance['room_id'],
            namespace = namespace_url
        )
