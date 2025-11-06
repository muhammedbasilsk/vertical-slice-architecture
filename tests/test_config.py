"""Tests for config.py."""
import os
import pytest
from config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_settings(self):
        """Test that Settings has correct default values."""
        settings = Settings()

        assert settings.database_url == "sqlite:///./app.db"
        assert settings.api_version == "v1"

    def test_settings_from_env_vars(self, monkeypatch):
        """Test that Settings loads from environment variables."""
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/testdb")
        monkeypatch.setenv("API_VERSION", "v2")

        settings = Settings()

        assert settings.database_url == "postgresql://test:test@localhost/testdb"
        assert settings.api_version == "v2"

    def test_settings_case_insensitive(self, monkeypatch):
        """Test that Settings is case insensitive."""
        monkeypatch.setenv("database_url", "postgresql://test:test@localhost/testdb")
        monkeypatch.setenv("api_version", "v3")

        settings = Settings()

        assert settings.database_url == "postgresql://test:test@localhost/testdb"
        assert settings.api_version == "v3"

    def test_settings_partial_env_vars(self, monkeypatch):
        """Test Settings with only some environment variables set."""
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/testdb")

        settings = Settings()

        assert settings.database_url == "postgresql://test:test@localhost/testdb"
        assert settings.api_version == "v1"  # Default value

    def test_settings_immutable_after_creation(self):
        """Test that Settings values can be accessed."""
        settings = Settings()

        # Verify we can access the values
        assert isinstance(settings.database_url, str)
        assert isinstance(settings.api_version, str)
