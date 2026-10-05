from datetime import date, timedelta

from tests.conftest import register


def test_login_required_redirects(client):
    r = client.get("/")
    assert r.status_code == 302 and "/login" in r.headers["Location"]


def test_register_login_logout(client):
    r = register(client)
    assert b"Course performance" in r.data
    client.post("/logout")
    r = client.post("/login", data={"email": "a@test.com", "password": "wrong"})
    assert b"Invalid email or password" in r.data
    r = client.post("/login", data={"email": "a@test.com", "password": "secret1"},
                    follow_redirects=True)
    assert b"Course performance" in r.data


def test_duplicate_email_rejected(client):
    register(client)
    client.post("/logout")
    assert b"already registered" in register(client).data


def test_course_assessment_flow_updates_dashboard(client):
    register(client)
    client.post("/courses", data={"code": "cs101", "name": "Intro CS", "credits": "4"})
    r = client.get("/courses")
    assert b"CS101" in r.data
    client.post("/courses/1/assessments",
                data={"title": "Midterm", "score": "45", "max_score": "50", "weight": "40"})
    r = client.get("/courses/1")
    assert b"90.0%" in r.data and b"Grade point 10" in r.data
    r = client.get("/")
    assert b"10.0" in r.data


def test_invalid_assessment_rejected(client):
    register(client)
    client.post("/courses", data={"code": "M1", "name": "Maths", "credits": "3"})
    r = client.post("/courses/1/assessments",
                    data={"title": "Quiz", "score": "60", "max_score": "50", "weight": "10"},
                    follow_redirects=True)
    assert b"Check the assessment" in r.data


def test_task_lifecycle_and_overdue(client):
    register(client)
    past = (date.today() - timedelta(days=2)).isoformat()
    client.post("/tasks", data={"title": "Lab record", "due_date": past, "priority": "high"})
    assert b"Lab record" in client.get("/tasks").data
    assert b"overdue" in client.get("/").data
    client.post("/tasks/1/toggle")
    assert b"Lab record" not in client.get("/tasks?filter=pending").data
    assert b"Lab record" in client.get("/tasks?filter=done").data
    client.post("/tasks/1/delete")
    assert b"Lab record" not in client.get("/tasks?filter=all").data


def test_users_cannot_see_each_others_data(client):
    register(client, "a@test.com")
    client.post("/courses", data={"code": "PHY", "name": "Physics", "credits": "3"})
    client.post("/logout")
    register(client, "b@test.com", "Bala")
    assert client.get("/courses/1").status_code == 404
    assert client.post("/courses/1/delete").status_code == 404


def test_study_session_api(client):
    register(client)
    r = client.post("/api/sessions", json={"minutes": 25})
    assert r.status_code == 201 and r.get_json()["week_minutes"] == 25
    assert client.post("/api/sessions", json={"minutes": 0}).status_code == 400
    assert client.get("/api/stats").get_json()["week_minutes"] == 25
    assert client.get("/timer").status_code == 200


def test_notes_search_and_isolation(client):
    register(client)
    client.post("/notes", data={"title": "Laplace", "body": "s-domain tricks"})
    assert b"Laplace" in client.get("/notes").data
    assert b"Laplace" in client.get("/notes?q=domain").data
    assert b"Laplace" not in client.get("/notes?q=zzz").data
    client.post("/logout")
    register(client, "b@test.com", "Bala")
    assert b"Laplace" not in client.get("/notes").data
    assert client.post("/notes/1/delete").status_code == 404


def test_streak_and_target_planner(client):
    register(client)
    client.post("/api/sessions", json={"minutes": 30})
    assert client.get("/api/stats").get_json()["streak"] == 1
    assert b"1 day" in client.get("/").data
    client.post("/courses", data={"code": "EE1", "name": "Circuits", "credits": "3"})
    client.post("/courses/1/assessments", data={"title": "Final", "weight": "100"})
    assert b"Target planner" in client.get("/courses/1").data
