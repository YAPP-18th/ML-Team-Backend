import socketio
import traceback
import time

from app.crud    import (
                    users,
                    study_rooms,
                    reports,
                    my_studies,
                    statuses,
                    redis_function
                    )
from app.database import SessionLocal
from app.errors   import NoSuchElementException, RequestInvalidException


clients = dict()


"""
To Do
- joinRoom, leaveRoom, status, disconnect 때 방에 입장해 있는 사용자 수를 알려줘야 한다.
  clients 객체에 접근하여 room_id가 동일한 객체의 수를 세는 방법이 있다.
  또는 Redis에 저장하는 형태를 아예 바꾸는 방법이 있다.
  노동과 시간은 후자가 더 많이 들어가지만 효율성이나 속도를 생각했을 때는 더 좋은 것 같다.
  전자, 후자 모두 효율적으로 코드를 만들 방법을 고려 할 필요가 있다.
- 오류가 발생했을 때 자동으로 disconnect 되게 하는 게 좋을 것 같다.
  오류가 발생한 상황은 다시 말하면 허용되지 않은 방법으로 소켓에 접근하는 것이기도 하다.
  response 이벤트로 이를 알려주기 보다는 바로 연결을 해제 시켜버리는 게 더 좋을 것 같다. 
"""


class StudyNamespace(socketio.AsyncNamespace):
    def __init__(self, sio, namespace, *args, **kwargs):
        super(socketio.Namespace, self).__init__(namespace)
        self.sio     = sio
        self.db      = SessionLocal()
        self.redis   = redis_function()

    async def get_users(self, room_id):
        users = [
            value for value in clients.values() if value['room_id'] == room_id
        ]
        return users

    async def on_connect(self, sid, environ, auth):
        try:
            print('connect')
            user_instance = users.get(
                db = self.db,
                user_id = auth['user_id']
            )
            report_instance = reports.get_or_create(
                db      = self.db,
                user_id = auth['user_id']
            )
            clients[sid] = {
                'user_id': auth['user_id'],
                'user_nickname': user_instance['nickname'],
                'status': 'study',
                'room_id': '',
                'report_id':  report_instance['id'],
                'my_study_id': '',
            }
            
            # redis init
            self.redis.start_study_init(user_id = auth['user_id'])

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
            print(room_id)
            self.enter_room(sid=sid, room=room_id, namespace=self.namespace)
            instance = my_studies.create(
                db         = self.db,
                room_id    = room_id,
                report_id  = clients[sid]['report_id']
            )
            clients[sid]['room_id']     = room_id
            clients[sid]['my_study_id'] = instance['id']

            # redis set study room
            self.redis.set_study_room(user_id = clients[sid]['user_id'], study_room_id = room_id)
            
            # 사용자 수를 알려줄 방법에 대해서 생각해봐야 한다.
            users = await self.get_users(room_id = room_id)

            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'joinRoom',
                    'data': users
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
            
            # 사용자 수를 알려줄 방법에 대해서 생각해봐야 한다.
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

            self.redis.add_current_log(clients[sid]['user_id'], status, time.time())
            clients[sid]['status'] = status
            users = await self.get_users(room_id = clients[sid]['room_id'])

            # 사용자 수를 알려줄 방법에 대해서 생각해봐야 한다.            
            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'status',
                    'data': users
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

            result = self.redis.end_study(clients[sid]['user_id'])

            if result:
                for status in ['sleep', 'smartphone', 'await', 'rest']:
                    await self.__create_status__(sid, status, result[status])

                my_study = my_studies.update(
                    db = self.db,
                    id = clients[sid]['my_study_id']
                )
                reports.update(
                    db         = self.db,
                    id         = clients[sid]['report_id'],
                    total_time = my_study['total_time']
                )
            room_id = clients[sid]['room_id']
            clients.pop(sid)
            print(f'sid: {sid}, clients: {clients}')
            print('disconnect success')
            users = await self.get_users(room_id = room_id)

            # 사용자 수를 알려줄 방법에 대해서 생각해봐야 한다.
            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'message': 'SUCCESS',
                    'eventName': 'disconnect',
                    'data': users
                }
            )

        except NoSuchElementException:
            # 입장 전에 공부방을 종료하는 경우
            # 사용자 수를 알려줄 방법에 대해서 생각해봐야 한다.
            await self.emit(
                'response',
                {
                    'statusCode': 200,
                    'messgae': 'SUCCESS',
                    'eventName': 'disconnect',
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
        saved_status = statuses.update_or_create(
            db = self.db,
            type = type,
            cnt = study_result['count'],
            time = study_result['sec'],
            my_study_id = clients[sid]['my_study_id'],
            report_id = clients[sid]['report_id']
        )

        print(saved_status)