from uuid             import UUID
from datetime         import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy       import and_, func
from sqlalchemy.orm   import Session
from sqlalchemy.exc   import IntegrityError

from app.crud.base    import CRUDBase
from app.models       import MyStudies, Reports, Statuses, StudyRooms
from app.schemas      import MyStudiesCreate, MyStudiesUpdate
from app.errors       import NoSuchElementException
from app.core         import time_settings, my_studies_settings


class CRUDMyStudy(CRUDBase[MyStudies, MyStudiesCreate, MyStudiesUpdate]):
    def get(self, db: Session, date: str, user_id: int):
        # TODO: 3차 Dev Camp 이후 구현 사항. 관련 쿼리 수정 필요.
        date = datetime.strptime(date, '%Y-%m-%d')
        instance = db.query(
            self.model
        ).filter(and_(
            Reports.date    == date,
            Reports.user_id == user_id
        )).outerjoin(
            StudyRooms,
            StudyRooms.id == self.model.study_room_id
        ).with_entities(
            self.model.id,
            self.model.started_at,
            self.model.ended_at,
            self.model.total_time,
            self.model.star_count,
            self.model.study_room_id,
            StudyRooms.title,
        ).all()

        data = jsonable_encoder(instance)

        if data:
            for my_study in data:
                my_study['statuses'] = jsonable_encoder(
                db.query(Statuses).filter(
                    Statuses.my_study_id == my_study['id']
                ).with_entities(
                    Statuses.id,
                    Statuses.type,
                    Statuses.count,
                    Statuses.time,
                ).all()
            )
            return jsonable_encoder(data)
        else:
            raise NoSuchElementException(message='not found')

    def get_by_id(self, db: Session, my_study_id: int):
        try:
            data = db.query(self.model).filter(
                self.model.id == my_study_id
            ).outerjoin(
                Reports,
                Reports.id == self.model.report_id
            ).with_entities(
                self.model.id,
                Reports.date.label('date'),
                self.model.total_time
            ).first()

            return jsonable_encoder(data)

        except ValueError:
            raise NoSuchElementException(message='not found')

        

    def create(self, db: Session, room_id: str, report_id: int):
        try:
            if not room_id:
                raise NoSuchElementException(message='not found')

            study_room = db.query(StudyRooms).filter(
                StudyRooms.id == UUID(room_id)
            ).first()

            study_room.current_join_counts += 1

            instance = self.model(
                study_room_id = UUID(room_id),
                report_id     = report_id,
                started_at    = datetime.utcnow() + time_settings.KST
            )
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return jsonable_encoder(instance)

        except AttributeError:
            raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')

        except IntegrityError:
            raise NoSuchElementException(message='not found') 

        finally:
            db.close()


    def update(self, db: Session, id: int):
        try:
            instance = db.query(self.model).filter(
                self.model.id == id
            ).first()

            statuses = db.query(Statuses).filter(
                Statuses.my_study_id == instance.id
            ).with_entities(
                func.sum(Statuses.time).label('total_time')
            ).first()
            

            if instance:
                print('statuses', jsonable_encoder(statuses))
                print('before ended_at', jsonable_encoder(instance))
                instance.ended_at   = datetime.utcnow() + time_settings.KST
                print('after ended_at: ', jsonable_encoder(instance))
                instance.total_time = (
                    instance.ended_at - instance.started_at
                ).seconds
                
                if jsonable_encoder(statuses)['total_time']:
                    instance.total_time -= jsonable_encoder(statuses)['total_time']
                    
                db.commit()
                db.refresh(instance)
                return jsonable_encoder(instance)

        except Exception as error:
            print(error)
            raise Exception

        finally:
            db.close()


my_studies = CRUDMyStudy(MyStudies)