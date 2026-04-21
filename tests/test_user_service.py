from app.services import user_service


class DummyUser:
    def __init__(self, email, hashed_password, is_active=True, is_admin=False):
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_admin = is_admin


class DummyQuery:
    def __init__(self, user=None):
        self.user = user

    def filter(self, *_args, **_kwargs):
        return self

    def first(self):
        return self.user


class DummyDB:
    def __init__(self, existing_user=None):
        self.existing_user = existing_user
        self.added = None
        self.committed = False
        self.refreshed = False

    def query(self, *_args, **_kwargs):
        return DummyQuery(self.existing_user)

    def add(self, obj):
        self.added = obj

    def commit(self):
        self.committed = True

    def refresh(self, _obj):
        self.refreshed = True


class DummyUserCreate:
    def __init__(self, email, password):
        self.email = email
        self.password = password


def test_create_user_creates_and_persists_user(monkeypatch):
    db = DummyDB()
    user_data = DummyUserCreate("unit@test.com", "clave123")

    monkeypatch.setattr(user_service, "User", DummyUser)
    monkeypatch.setattr(user_service, "hash_password", lambda password: f"hashed_{password}")

    created_user = user_service.create_user(db, user_data)

    assert created_user.email == "unit@test.com"
    assert created_user.hashed_password == "hashed_clave123"
    assert db.added is not None
    assert db.committed is True
    assert db.refreshed is True

def test_authenticate_user_returns_user_when_credentials_are_valid(monkeypatch):
    user = DummyUser(email="login@test.com", hashed_password="hashed_ok")
    db = DummyDB(existing_user=user)

    monkeypatch.setattr(user_service, "verify_password", lambda plain, hashed: plain == "clave123" and hashed == "hashed_ok")

    authenticated_user = user_service.authenticate_user(db, "login@test.com", "clave123")

    assert authenticated_user is user


def test_authenticate_user_returns_none_when_password_is_invalid(monkeypatch):
    user = DummyUser(email="login@test.com", hashed_password="hashed_ok")
    db = DummyDB(existing_user=user)

    monkeypatch.setattr(user_service, "verify_password", lambda plain, hashed: False)

    authenticated_user = user_service.authenticate_user(db, "login@test.com", "incorrecta")

    assert authenticated_user is None