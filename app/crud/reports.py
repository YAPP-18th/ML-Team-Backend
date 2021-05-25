from datetime         import date, datetime
from sqlalchemy       import and_
from sqlalchemy.orm   import Session
from fastapi.encoders import jsonable_encoder

from app.models       import Reports, Disturbances
from app.schemas      import ReportsCreate, ReportsUpdate
from app.crud.base    import CRUDBase


class CRUDReport(CRUDBase[Reports, ReportsCreate, ReportsUpdate]):
    def get(self, db: Session, user_id: str, date: date):
        try:
            data = db.query(self.model).filter(and_(
                self.model.user_id == user_id,
                self.model.date    == date
            )).outerjoin(
                Disturbances,
                Disturbances.report_id == self.model.id
            ).with_entities(

            ).first()

            if data:
                return jsonable_encoder(data) 
            else:
                # Not Found
                pass

        except:
            raise Exception


    def get_or_create(self, db: Session, today: date, user_id: int):
        try:
            if (today.hour >= 0) and (today.hour < 5):
                date = datetime(today.year, today.month, today.day - 1)
            else:
                date = date = datetime(today.year, today.month, today.day)
            
            instance = db.query(self.model).filter(and_(
                self.model.user_id == user_id,
                self.model.date    == date
            )).first()
            
            if instance:
                return jsonable_encoder(instance)
            else:
                instance = self.model(user_id = user_id, date = date)
                db.add(instance)
                db.commit()
                db.refresh(instance)
                return jsonable_encoder(instance)

        except:
            raise Exception

        finally:
            db.close()


    def update(self, db: Session, id: int, total_time: int):
        try:
            instance = db.query(self.model).filter(
                self.model.id == id
            ).update({'total_time': self.model.total_time + total_time})
            if instance:
                db.commit()
            else:
                # Not Found
                pass

        except:
            raise Exception

        finally:
            db.close()           


reports = CRUDReport(Reports)