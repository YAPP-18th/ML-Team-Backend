from uuid             import UUID
from datetime         import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy       import and_
from sqlalchemy.orm   import Session

from app.crud.base    import CRUDBase
from app.models       import MyStudies, Reports, Disturbances, StudyRooms
from app.schemas      import MyStudiesCreate, MyStudiesUpdate
from app.errors       import NoSuchElementException
from app.core         import time_settings


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
                my_study['disturbances'] = jsonable_encoder(
                db.query(Disturbances).filter(
                    Disturbances.my_study_id == my_study['id']
                ).with_entities(
                    Disturbances.id,
                    Disturbances.type,
                    Disturbances.count,
                    Disturbances.time,
                ).all()
            )
            return jsonable_encoder(data)
        else:
            raise NoSuchElementException(message='not found')

    def create(self, db: Session, room_id: str, report_id: int):
        try:
            instance = self.model(
                study_room_id = UUID(room_id),
                report_id     = report_id,
                started_at    = datetime.utcnow() + time_settings.KST
            )
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return jsonable_encoder(instance)

        except:
            raise Exception

        finally:
            db.close()


    def update(self, db: Session, id: int):
        try:
            instance = db.query(self.model).filter(
                self.model.id == id
            ).first() 
            
            if instance:
                instance.ended_at   = datetime.utcnow() + time_settings.KST
                instance.total_time = (
                    instance.ended_at - instance.started_at
                ).seconds
                db.commit()
                db.refresh(instance)
                return jsonable_encoder(instance)

        except:
            raise Exception

        finally:
            db.close()


my_studies = CRUDMyStudy(MyStudies)