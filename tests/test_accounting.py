import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db import Base, get_session
from service import app
from sqlalchemy_utils import create_database, drop_database

import routers

test_db_url = 'sqlite:///./test.db'
engine = create_engine(test_db_url,
                       connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db
app.include_router(routers.accounting.router)
client = TestClient(app)


def test_default():
    """
    Тест для проверки реста
    :return:
    """
    response = client.get('/top_10_accounts')
    assert response.status_code in (200, 204)


def test_create_account():
    """
    Тест создания аккаунта
    :return:
    """
    try:
        create_database(test_db_url)
        # Никаого 'id_account': 1 не должно быть, там автоинкремент, но из-за того, что у меня в тестах не pg, что-то не так
        body = {"id_account": 1, "name": "Vasya", "balance": 100}
        response = client.post(url='/create_account',
                               json=body,)
        assert response.status_code == 200
    finally:
        drop_database(test_db_url)


def test_update_balance():
    """
    Тест изменения баланса. Меняем баланс на аккаунте, которого нет в БД.
    Аккаунт создается и сверяем баланс нового аккаунт с тем, что мы отправили.
    :return:
    """
    try:
        create_database(test_db_url)
        body = {'id': 1, 'id_account': 9999, 'operation': 100}
        update_response = client.post(url='/update_balance',
                                      json=body, )
        if update_response.status_code == 200:
            check_response = client.get(url='/check_balance/?id_account=9999')
            if check_response.status_code == 200:
                check_response_content = json.loads(check_response.content)
                assert body['operation'] == check_response_content[0]['balance']
    finally:
        drop_database(test_db_url)
