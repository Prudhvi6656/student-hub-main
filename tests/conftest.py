import pytest

from app import create_app, db


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False,
                      "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, email="a@test.com", name="Asha"):
    return client.post("/register", data={"name": name, "email": email, "password": "secret1"},
                       follow_redirects=True)
