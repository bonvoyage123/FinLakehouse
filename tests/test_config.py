from src.config.settings import Settings


def test_project_settings_default_values():
    settings = Settings()
    assert settings.project_name == "FinLakehouse"
    assert settings.raw_prefix == "raw"
