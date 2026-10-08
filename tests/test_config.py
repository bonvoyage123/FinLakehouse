from src.config.settings import Settings


def test_project_settings_default_values():
    settings = Settings()
    assert settings.project_name == "FinLakehouse"
    assert settings.raw_prefix == "raw"


def test_project_settings_use_fmp_api_environment_names(monkeypatch):
    monkeypatch.setenv(
        "FMP_API_BASE_URL",
        "https://example.test/stable/",
    )
    monkeypatch.setenv("FMP_API_KEY", "test-key")

    settings = Settings()

    assert settings.fmp_api_base_url == "https://example.test/stable/"
    assert settings.fmp_api_key == "test-key"
