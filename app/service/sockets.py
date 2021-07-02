import socketio
import traceback

import time



from app.crud               import (
                                study_rooms,
                                reports,
                                my_studies,
                                statuses,
                                redis_function
                            )
from app.database           import SessionLocal
from app.errors   import NoSuchElementException, RequestInvalidException

clients = dict()


class StudyNamespace(socketio.AsyncNamespace):
    def __init__(self, sio, namespace, *args, **kwargs):
        super(socketio.Namespace, self).__init__(namespace)
        self.sio     = sio
        self.db      = SessionLocal()
        self.redis   = redis_function()


    async def on_connect(self, sid, environ, auth):
        try:
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
            }

            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'connect',
                    'data': {}
                },
                namespace = self.namespace
            )      

            print('connect success')      
                

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {
                    'statusCode': 500,
                    'message': f'SERVER_ERROR_{error}',
                    'eventName': 'connect',
                    'data': {}
                },
                namespace = self.namespace
            )      

    
    async def on_joinRoom(self, sid, room_id):
        try:            
            print('join room')
            self.enter_room(sid=sid, room=room_id, namespace=self.namespace)
            instance = my_studies.create(
                db         = self.db,
                room_id    = room_id,
                report_id  = clients[sid]['report_id']
            )
            clients[sid]['room_id']     = room_id
            clients[sid]['my_study_id'] = instance['id']
            # redis table init
            self.redis.start_study_init(user_id = clients['user_id'], study_room_id=room_id)
            
            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'joinRoom',
                    'dat': {}
                },
                room      = room_id,
                namespace = self.namespace
            )

            print('join room success')

        except NoSuchElementException:
            print('not found')
            await self.emit(
                'response',
                {
                    'statusCode': 404,
                    'message': 'NOT_FOUND',
                    'eventName': 'joinRoom',
                    'data': {}
                },
                namespace = self.namespace
            )     

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {
                    'statusCode': 500,
                    'message': f'SERVER_ERROR_{error}',
                    'eventName': 'joinRoom',
                    'data': {}
                },
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
            print('leave room')
            
            await self.emit(
                'disconnect',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'leaveRoom',
                    'data': {}
                },
                room      = room_id,
                namespace = self.namespace
            )
            await self.disconnect(sid, namespace=self.namespace)

            print('leave room success')

        except RequestInvalidException:
            print('invalid request')
            await self.emit(
                'response',
                {
                    'statusCode': 400,
                    'message': 'INVALID_REQUEST',
                    'eventName': 'leaveRoom',
                    'data': {}
                }
            )

        except NoSuchElementException:
            print('not found')
            await self.emit(
                'response',
                {
                    'statusCode': 404,
                    'messgae': 'NOT_FOUND',
                    'eventName': 'leaveRoom',
                    'data': {}
                },
                namespace = self.namespace
            )    

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {
                    'statusCode': 500,
                    'message': f'SERVER_ERROR_{error}',
                    'eventName': 'leaveRoom',
                    'data': {}
                },
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

            self.redis.add_current_log(clients['user_id'], status, time.time())


            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'status',
                    'data': status
                },
                room = clients[sid]['room_id'],
                namespace = self.namespace
            )

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {
                    'statusCode': 500,
                    'message': f'SERVER_ERROR_{error}',
                    'eventName': 'status',
                    'data': {}
                },
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
            print('disconnect')
            study_rooms.leave(self.db, room_id=clients[sid]['room_id'])
            self.leave_room(sid=sid, room=clients[sid]['room_id'], namespace=self.namespace)

            result = self.redis.end_study(clients['user_id'])

            for status in ['sleep', 'smartphone', 'await', 'rest']:
                self.__create_status__(sid, status, result[status])

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
            print(f'sid: {sid}, clients: {clients}')
            print('disconnect success')

        except NoSuchElementException:
            print('not found')
            await self.emit(
                'response',
                {
                    'statusCode': 404,
                    'messgae': 'NOT_FOUND',
                    'eventName': 'leaveRoom',
                    'data': {}
                },
                namespace = self.namespace
            )              

        except Exception as error:
            print(traceback.print_exc())
            await self.emit(
                'response',
                {
                    'statusCode': 500,
                    'message': f'SERVER_ERROR_{error}',
                    'eventName': 'disconnect',
                    'data' : {}
                },
                namespace = self.namespace
            )

    async def __create_status__(self, sid, type, study_result: dict):
        statuses.update_or_create(
            db = self.db,
            type = type,
            cnt = study_result['count'],
            time = study_result['sec'],
            my_study_id = clients[sid]['my_study_id'],
            report_id = clients[sid]['report_id']
        )
