import pytest
from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "testuser@example.com"

    signup_url = f"/activities/{quote(activity)}/signup"
    # sign up succeeds
    r = client.post(signup_url, params={"email": email})
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup returns 400
    r2 = client.post(signup_url, params={"email": email})
    assert r2.status_code == 400

    # unregister the participant
    del_url = f"/activities/{quote(activity)}/participants"
    r3 = client.delete(del_url, params={"email": email})
    assert r3.status_code == 200
    assert email not in activities[activity]["participants"]


def test_signup_nonexistent_activity():
    r = client.post("/activities/DoesNotExist/signup", params={"email": "a@b.com"})
    assert r.status_code == 404
