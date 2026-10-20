import pytest

from labbook.app import create_app_from_env, health


def test_config_from_environment(tmp_path):
    svc, _, _ = create_app_from_env({})
    assert health(svc) == {"status": "ok", "storage": "InMemoryBookingRepository"}
    db = str(tmp_path / "labbook.db")
    svc, _, _ = create_app_from_env({"LABBOOK_STORAGE": "sqlite", "LABBOOK_DB": db})
    assert health(svc) == {"status": "ok", "storage": "SqliteBookingRepository"}
    assert (tmp_path / "labbook.db").exists()


def test_config_errors_fail_fast():
    with pytest.raises(ValueError):
        create_app_from_env({"LABBOOK_STORAGE": "mongodb"})
    with pytest.raises(ValueError):
        create_app_from_env({"LABBOOK_STORAGE": "sqlite"})


def test_health_reports_storage_failure():
    svc, _, _ = create_app_from_env({})
    svc.repo.for_user = None          # simulate a broken storage adapter
    assert health(svc) == {"status": "error", "detail": "TypeError"}
