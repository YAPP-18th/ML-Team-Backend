from fastapi.testclient import TestClient

from app.database.session import SessionLocal
from app.database.base    import Base
from app.api.deps         import get_db
from app.main             import app
<<<<<<< HEAD

Base.metadata

def overried_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
=======

Base.metadata

def overried_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

>>>>>>> 1e939ba... 추가: Study Room

def client():
    with TestClient(app) as client:
        yield client

<<<<<<< HEAD
def client():
    with TestClient(app) as client:
        yield client
=======
>>>>>>> 1e939ba... 추가: Study Room

app.dependency_overrides[get_db] = overried_get_db

<<<<<<< HEAD
app.dependency_overrides[get_db] = overried_get_db

<<<<<<< HEAD
@pytest.fixture(scope="module")
def random_product() -> Dict[str, str]:
    return {
        "id": 1,
        "name": "Test Product",
        "price": 80,
    }


def test_user() -> Dict[str, str]:
    return {
        "id": 1,
        "provider": "Google",
        "email": "test@test.com",
        "nickname": "test"
    }
=======
client = TestClient(app)
>>>>>>> 15048eb... 수정: 전체적인 폴더 구조 리팩토링
=======
client = TestClient(app)
>>>>>>> 1e939ba... 추가: Study Room
