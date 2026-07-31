import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module
from src.app import app

_original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app)


# Restores in-memory state so mutations in one test don't affect others
@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_original_activities))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_original_activities))
