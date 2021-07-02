from fastapi.encoders import jsonable_encoder
from sqlalchemy       import and_
from sqlalchemy.orm   import Session

from app.crud.base    import CRUDBase
from app.models       import Statuses
from app.schemas      import StatusCreate, StatusUpdate

class CRUDStatus(CRUDBase[Statuses, StatusCreate, StatusUpdate]):
    def create(self, db: Session, statuses: dict):
        try:            
            # instance = db.bulk_insert_mappings(self.model, statuses)
            db.commit()
            
        except Exception as error:
            print(error)
            raise Exception

        finally:
            db.close()
        

    def update_or_create(
        self,
        db: Session,
        type: str,
        cnt: int,
        time: int,
        my_study_id: int,
        report_id: int
    ):
        try:
            instance = db.query(self.model).filter(and_(
                self.model.type        == type,
                self.model.my_study_id == my_study_id,
                self.model.report_id   == report_id
            )).first()
            
            if instance:
                instance.count += cnt
                instance.time  += time

            else:
                instance = self.model(
                    type        = type,
                    count       = cnt,
                    time        = time,
                    my_study_id = my_study_id,
                    report_id   = report_id
                )
                db.add(instance)

            db.commit()
            db.refresh(instance)

            return jsonable_encoder(instance)

        except:
            raise Exception

        finally:
            db.close()


statuses = CRUDStatus(Statuses)