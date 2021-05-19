from typing                     import Any
from sqlalchemy                 import inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr



@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    def as_dict(self) -> dict:
        # TODO: jsonable_encoder로 인해 발생하는 것으로 추정되는 오류 해결을 위한 함수
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
