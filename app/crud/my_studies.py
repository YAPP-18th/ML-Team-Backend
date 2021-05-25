from uuid             import UUID
from datetime         import date, datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy       import and_
from sqlalchemy.orm   import Session

from app.crud.base    import CRUDBase
from app.models       import MyStudies, Reports, Disturbances
from app.schemas      import MyStudiesCreate, MyStudiesUpdate


class CRUDMyStudy(CRUDBase[MyStudies, MyStudiesCreate, MyStudiesUpdate]):
    def get(self, db: Session, date: date, user_id: int):
        try:
            data = db.query(self.model).filter(and_(
                Reports.date    == date,
                Reports.user_id == user_id
            )).outerjoin(
                Reports,
                Reports.id == self.model.report_id
            ).outerjoin(
                Disturbances,
                Disturbances.report_id == self.model.id
            ).with_entities(
                
            )

            if data:
                return jsonable_encoder(data)
            else:
                # Not Found
                pass
            
        except:
            pass


    def create(self, db: Session, room_id: str, started_at: datetime, report_id: int):
        try:
            instance = self.model(
                started_at    = started_at,
                study_room_id = UUID(room_id),
                report_id     = report_id
            )
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return jsonable_encoder(instance)

        except:
            raise Exception

        finally:
            db.close()


    def update(self, db: Session, ended_at: datetime, total_time: int, id: int):
        try:
            instance = db.query(self.model).filter(
                self.model.id == id
            ).update({'ended_at': ended_at, 'total_time': total_time})

            if instance:
                db.commit()
            else:
                # Not Found
                pass

        except:
            raise Exception

        finally:
            db.close()


my_studies = CRUDMyStudy(MyStudies)