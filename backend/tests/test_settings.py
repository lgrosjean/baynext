from app.core.settings import Settings


def test_settings_initialization():
    # Test valid initialization
    settings = Settings(
        ml_api_secret_api_key="test_secret_key",
        database_url="postgresql://user:password@host:port/dbname",
        blob_read_write_token="blob_read_write_token",
    )
    assert settings.app_name == "Baynext API"
    assert settings.ml_api_secret_api_key.get_secret_value() == "test_secret_key"
    assert (
        settings.database_url.get_secret_value()
        == "postgresql://user:password@host:port/dbname"
    )
    assert settings.blob_read_write_token.get_secret_value() == "blob_read_write_token"


def test_settings_env_file_loading(monkeypatch):
    # Mock environment variable
    monkeypatch.setenv("ML_API_SECRET_API_KEY", "env_secret_key")

    # Test loading from environment variable
    settings = Settings()
    assert settings.ml_api_secret_api_key.get_secret_value() == "env_secret_key"
