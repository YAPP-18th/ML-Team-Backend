from sqlalchemy     import and_
from sqlalchemy.orm import Session

from app.crud.base  import CRUDBase
from app.models     import Disturbances
from app.schemas    import DisturbanceCreate, DisturbanceUpdate

class CRUDDisturbance(CRUDBase[Disturbances, DisturbanceCreate, DisturbanceUpdate]):
    def create(self, db: Session, disturbances: list):
        try: 
            db.bulk_insert_mappings(self.model, disturbances)
            db.commit()
            
        except:
            raise Exception

        finally:
            db.close()
        

    def update_or_create(
        self,
        db: Session,
        type: str,
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
                instance.count += 1
                instance.time  += time

            else:
                instance = self.model(
                    type        = type,
                    count       = 1,
                    time        = time,
                    my_study_id = my_study_id,
                    report_id   = report_id
                )
                db.add(instance)

            db.commit()

        except:
            raise Exception

        finally:
            db.close()


disturbances = CRUDDisturbance(Disturbances)