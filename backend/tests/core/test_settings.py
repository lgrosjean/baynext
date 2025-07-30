from app.core.settings import Env, Settings


def test_settings_initialization():
    """Test that Settings can be initialized with default values."""
    # Test valid initialization
    settings = Settings(
        ml_api_secret_api_key="test_secret_key",
        database_url="test_database_url",
        blob_read_write_token="test_blob_token",
    )
    assert settings.environment == Env.development
    assert settings.APP_NAME == "Baynext API"
    assert settings.ml_api_secret_api_key.get_secret_value() == "test_secret_key"
    assert settings.database_url.get_secret_value() == "test_database_url"
    assert settings.blob_read_write_token.get_secret_value() == "test_blob_token"


def test_settings_env_file_loading(monkeypatch):
    """Test that settings can be loaded from environment variables."""
    # Mock environment variable
    ml_api_secret_api_key = "env_secret_key"
    monkeypatch.setenv("ML_API_SECRET_API_KEY", ml_api_secret_api_key)
    monkeypatch.setenv("ENVIRONMENT", "production")

    # Test loading from environment variable
    settings = Settings()
    assert settings.ml_api_secret_api_key.get_secret_value() == ml_api_secret_api_key
    assert settings.environment == Env.production
    assert settings.BUCKET_NAME == "bucket_name"  # Default value from Settings
