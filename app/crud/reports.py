from datetime         import datetime
from sqlalchemy       import and_, func, not_
from sqlalchemy.orm   import Session
from fastapi.encoders import jsonable_encoder

from app.models       import Reports, Statuses
from app.schemas      import ReportsCreate, ReportsUpdate
from app.crud.base    import CRUDBase
from app.errors       import NoSuchElementException
from app.core         import time_settings


class CRUDReport(CRUDBase[Reports, ReportsCreate, ReportsUpdate]):
    def get(self, db: Session, user_id: int, date: str):
        date = datetime.strptime(date, '%Y-%m-%d')
        instance = db.query(
            self.model,
        ).filter(and_(
            self.model.user_id    == user_id,
            self.model.date       == date,
            self.model.total_time != 0
        )).outerjoin(
            Statuses,
            Statuses.report_id == self.model.id
        ).with_entities(
            self.model.id,
            self.model.date,
            self.model.achievement,
            self.model.concentration,
            self.model.total_time,
            self.model.total_star_count,
            func.sum(Statuses.time).filter(not_(
                Statuses.type == 'rest'
            )).label('total_status_time')
        ).group_by(self.model.id).first()

        if instance:
            report   = jsonable_encoder(instance)
            statuses = db.query(Statuses).filter(
                Statuses.report_id == report['id']
            ).with_entities(
                Statuses.type.label('name'),
                func.sum(Statuses.count).label('total_count'),
                func.sum(Statuses.time).label('value')
            ).group_by(Statuses.type).all()
            report['statuses'] = jsonable_encoder(statuses)
            report['max_status'] =  [status['name'] for status in report['statuses'] if status['value'] == max(report['statuses'], key=lambda x: x['value'])['value']]
            return [report]
        else:
            raise NoSuchElementException(message='not found')


    def get_or_create(self, db: Session, user_id: int):
        try:
            today = datetime.utcnow() + time_settings.KST
            if (today.hour >= 0) and (today.hour < 5):
                date = datetime(today.year, today.month, today.day - 1)
            else:
                date = datetime(today.year, today.month, today.day)
            
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

        except Exception as error:
            print(error)
            raise Exception

        finally:
            db.close()


    def update(self, db: Session, id: int, total_time: int):
        try:
            instance = db.query(self.model).filter(
                self.model.id == id
            ).first()

            statuses = db.query(Statuses).filter(
                Statuses.report_id == instance.id
            ).with_entities(
                func.sum(Statuses.time).filter(not_(
                    Statuses.type == 'rest'
                )).label('total_time')
            ).first()
            
            if instance:
                instance.total_time += total_time
                instance.concentration = 100 - int(jsonable_encoder(statuses)['total_time'] / instance.total_time * 100)
                db.commit()

        except:
            raise Exception

        finally:
            db.close()           


reports = CRUDReport(Reports)