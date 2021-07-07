from datetime         import datetime
from uuid             import UUID
from typing           import Union, Optional
from datetime         import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy       import and_
from sqlalchemy.orm   import Session
from sqlalchemy.exc   import IntegrityError

from app.core         import study_rooms_settings
from app.crud.base    import CRUDBase
from app.models       import StudyRooms
from app.schemas      import (
                        StudyRoomsCreate,
                        StudyRoomsUpdate,
                        StudyRoomJoin
                        )
from app.errors       import (
                        NoSuchElementException,
                        InvalidArgumentException,
                        RequestConflictException,
                        RequestInvalidException,
                        ForbiddenException
                        )
from app.core         import time_settings

from app.crud.redis_function         import redis_function


MAX_CAPACITY = study_rooms_settings.MAX_CAPACITY
redis_session = redis_function()

def check_password_exist(room_info: Union[StudyRoomsCreate, StudyRoomsUpdate]):
    return False if (not room_info.is_public) and (not room_info.password) else True


class CRUDStudyRoom(CRUDBase[StudyRooms, StudyRoomsCreate, StudyRoomsUpdate]):
    def get(self, db: Session, room_id: UUID):
        try:
            data = db.query(self.model).filter(
                self.model.id == UUID(room_id)
            ).with_entities(
                self.model.id,
                self.model.title,
                self.model.style,
                self.model.description,
                self.model.is_public,
                self.model.current_join_counts,
                self.model.created_at,
                self.model.owner_id
            ).first()

            if data:
                return [jsonable_encoder(data)]
            else:
                raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')


    def get_multi(
        self,
        db: Session,
        skip: Optional[int],
        limit: Optional[int],
        owner_id: Optional[int],
        option: Optional[str]
    ):
        query = db.query(self.model)
        if owner_id:
            query = query.filter(self.model.owner_id == owner_id)

        data = query.filter(
                self.model.current_join_counts < MAX_CAPACITY
            ).with_entities(
                self.model.id,
                self.model.title,
                self.model.style,
                self.model.description,
                self.model.is_public,
                self.model.current_join_counts,
                self.model.created_at,
                self.model.owner_id
            ).order_by(f'study_room_{option}').offset(skip).limit(limit).all()

        if data:
            return jsonable_encoder(data)
        else:
            raise NoSuchElementException(message='not found')


    def create(self, db: Session, room_info: StudyRoomsCreate):
        try:
            if not check_password_exist(room_info):
                raise InvalidArgumentException(message='field required')

            # room_info.current_join_counts += 1
            room_info.created_at = datetime.utcnow() + time_settings.KST
            data = self.model(**jsonable_encoder(room_info))
            db.add(data)
            db.commit()

        except IntegrityError:
            raise NoSuchElementException(message='not found')


    def update(self, db: Session, room_id: str, room_info: StudyRoomsUpdate):
        try:
            if not check_password_exist(room_info):
                raise InvalidArgumentException(message='field required')
                
            update_data = room_info.dict(exclude_none=True)
            data = db.query(self.model).filter(and_(
                self.model.id == UUID(room_id),
                self.model.owner_id == room_info.owner_id
            )).update(update_data)

            if data:
                db.commit()
            else:
                raise ForbiddenException(message='forbidden')    

        except ValueError:
            raise NoSuchElementException(message='not found')


    def remove(self, db: Session, room_id: str, user_id: int):
        try:
            data = db.query(self.model).filter(and_(
                self.model.id       == UUID(room_id),
                self.model.owner_id == user_id
            )).first()

            if data:
                db.delete(data)
                db.commit()
            else:
                raise ForbiddenException(message='forbidden')

        except ValueError:
            raise NoSuchElementException(message='not found')


    def join(self, db: Session, room_id: str, room_info: StudyRoomJoin):
        try:
            if redis_session.check_join(room_info.user_id):
                raise RequestInvalidException(message='Already Connect a Study-Room')
                
            data = db.query(self.model).filter(
                self.model.id == UUID(room_id)
            ).first()
            study_room = jsonable_encoder(data)
            
            if study_room:
                if study_room['current_join_counts'] >= MAX_CAPACITY:
                    raise RequestConflictException(message='no empty')

                if study_room['owner_id'] != room_info.user_id:
                    if study_room['is_public']:
                        if room_info.password:
                            raise InvalidArgumentException(message='field not required')
                    else:
                        if not room_info.password:
                            raise InvalidArgumentException(message='field required')
                        elif room_info.password != study_room['password']:
                            raise ForbiddenException(message='forbidden')

                # data.current_join_counts += 1

                print(f"join study-room(id : {room_id}. current count : {data.current_join_counts})")

                db.commit()

            else:
                raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')

        finally:
            db.close()


    def leave(self, db: Session, room_id: str):
        try: 
            if not room_id:
                raise NoSuchElementException(message='not found')
            
            study_room = db.query(self.model).filter(
                self.model.id == UUID(room_id)
            )

            print(study_room.first().current_join_counts)

            if (int(study_room.first().current_join_counts) < 1):
                raise RequestInvalidException(message='invalid request')

            study_room.update({'current_join_counts': self.model.current_join_counts - 1})
            db.commit()

        except AttributeError:
            raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')

        except IntegrityError:
            raise NoSuchElementException(message='not found')

        finally:
            db.close()

    
    def current_check(self, db: Session, user_id: int):
        try:
            """
            TODO
            - Redis에 접근해서 user_id가 존재하는지 확인한다.
            - 만약 있을 경우 공부 중이던 사람이기 때문에 ABNORMAL의 TIMESTAMP를 확인한다.
            - 만약 5분이 지난 경우 삭제하고 Redis Initialize를 종료한다.
              이때 해당 사용자가 포함되어 있던 study_room의 current_join_count도 차감한다.
              이를 수행하기 위해 Redis에 room_id 또한 포함되어야 할 것으로 판단된다.
            - 5분이 지나지 않은 경우 재접속 할 것인지 묻는다.
            - user_id가 존재하지 않는 경우와 5분이 지난 경우 200 status_code로 응답한다.
            - 만약 5분이 지나지 않아서 재접속 여부를 물어봐야 할 경우 409 conflict 응답한다.
            """

            pass

        except Exception:
            raise Exception


    def re_join(self, db: Session, user_id: int, is_re_joined: bool):
        try:
            """
            TODO
            - current_check 엔드포인트에 이어서 만약 재접속하겠다고 한 경우
              data에 해당 room_id를 포함해서 보내준다.
              페이지 랜더링을 통해 해당 방으로 가야하기 때문이다.
            - 만약 재접속하지 않겠다고 한 경우 data에 빈 문자열을 보내준다.
            - 그리고 재접속하지 않겠다고 한 경우 해당 마이스터디 테이블을 삭제한다.
            - 재접속과 그렇지 않은 경우 모두 status_code 200으로 응답한다.
            """
        
            pass

        except Exception:
            raise Exception


study_rooms = CRUDStudyRoom(StudyRooms)