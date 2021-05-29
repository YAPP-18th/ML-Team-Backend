import socketio
import traceback


from app.crud               import (
                                study_rooms,
                                reports,
                                my_studies,
                                statuses
                            )
from app.database           import SessionLocal


clients = dict()


class StudyNamespace(socketio.AsyncNamespace):
    def __init__(self, sio, namespace, *args, **kwargs):
        super(socketio.Namespace, self).__init__(namespace)
        self.sio     = sio
        self.db      = SessionLocal()


    async def on_connect(self, sid, environ, auth):
        try:
            print(sid)
            print('connect')
            instance = reports.get_or_create(
                db      = self.db,
                user_id = auth['user_id']
            )
            clients[sid] = {
                'user_id': auth['user_id'],
                'room_id': '',
                'report_id':  instance['id'],
                'my_study_id': '',
                # 're_joined': False
            }

            # if not clients:
            #     """
            #     TODO
            #     - Redis Initialize
            #     """
            #     # print('initial connect')

            # else:
            #     # print('re-connect')
            #     """
            #     TODO
            #     - 정상적으로 다시 진입했기 때문에 Redis ABNORMAL 삭제
            #     """
            #     # self.clients['re_joined'] = False

            await self.emit(
                'response',
                {'message': 'connection'},
                namespace = self.namespace
            )            
                

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {'message': f'server error {error}'},
                namespace = self.namespace
            )      

    
    async def on_joinRoom(self, sid, room_id):
        try:
            print('join')
            print(clients)
            
            self.enter_room(sid=sid, room=room_id, namespace=self.namespace)
            instance = my_studies.create(
                db         = self.db,
                room_id    = room_id,
                report_id  = clients[sid]['report_id']
            )
            clients[sid]['room_id']     = room_id
            clients[sid]['my_study_id'] = instance['id']
            await self.emit(
                'response',
                {'message': 'join success'},
                room      = room_id,
                namespace = self.namespace
            )
        
        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {'message': f'server error {error}'},
                room      = room_id,
                namespace = self.namespace
            )     

    async def on_leaveRoom(self, sid, room_id):
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

            study_rooms.leave(self.db, room_id=room_id)
            self.leave_room(sid=sid, room=room_id, namespace=self.namespace)

            instance = my_studies.update(
                db = self.db,
                id = clients[sid]['my_study_id']
            )
            reports.update(
                db         = self.db,
                id         = clients[sid]['report_id'],
                total_time = instance['total_time']
            )
            
            clients.pop(sid)

            await self.emit(
                'disconnect',
                {'message': 'leave success'},
                room      = room_id,
                namespace = self.namespace
            )
            await self.disconnect(sid, namespace=self.namespace)
            
        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {'message': f'server error {error}'},
                room      = room_id,
                namespace = self.namespace
            )


    async def on_status(self, sid, status):
        try:
            """
            TODO:
            - Client에서 disturbance 데이터에 room_id 포함하여 줘야 한다.
            - response 이벤트로 message에 disturbance 상태를 보내줘야 한다.
            - 개별 사용자의 휴식이 다르기 때문에 Redis에 휴식에 대한 것도 저장 할 필요가 있어 보인다.
            """
            print('status', status)
            statuses.update_or_create(
                self.db,
                status['type'],
                status['time'],
                clients[sid]['my_study_id'],
                clients[sid]['report_id']
            )

            await self.emit(
                'response',
                {'message': status['type']},
                room      = status['room_id'],
                namespace = self.namespace
            )

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {'message': f'server error {error}'},
                room      = statuses['room_id'],
                namespace = self.namespace
            )            


    async def on_disconnect(self, sid):
        try:
            """
            TODO:
            - leaveRoom을 발생시켜도 disconnect event가 발생할 것이다.
              비정상적인 종료와 차이점은 leaveRoom일 때는 clients 객체가 빈 객체다.
            - Redis에 이미 해당 사용자의 id가 저장되어 있기 때문에 clients 등을 통해 user_id에 접근하여
              발생 시점의 timstamp와 함께 ABNORMAL 타입을 저장한다.
            """
            # if self.clients:
                # Redis 저장 부분
            print('disconnect')

            study_rooms.leave(self.db, room_id=clients[sid]['room_id'])
            self.leave_room(sid=sid, room=clients[sid]['room_id'], namespace=self.namespace)


            my_study = my_studies.update(
                db = self.db,
                id = clients[sid]['my_study_id']
            )
            reports.update(
                db         = self.db,
                id         = clients[sid]['report_id'],
                total_time = my_study['total_time']
            )
            
            clients.pop(sid)

            print(clients)

        except Exception as error:
            print(traceback.print_exc())