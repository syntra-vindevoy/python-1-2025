from settings import Settings

settings = Settings()
settings.init()

def test_get_user():
    assert settings.get_user() == "postgres"

def test_get_password():
    assert len(settings.get_password() ) > 0
