import src.app as app_module


class TestGetActivities:
    def test_returns_all_activities(self, client):
        # Arrange
        expected_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_count

    def test_each_activity_has_required_keys(self, client):
        # Arrange
        required_keys = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        for activity in response.json().values():
            assert required_keys <= activity.keys()


class TestSignup:
    def test_signup_adds_participant(self, client):
        # Arrange
        activity_name = "Tennis Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        assert email in app_module.activities[activity_name]["participants"]

    def test_signup_duplicate_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already enrolled

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "someone@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregister:
    def test_unregister_removes_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already enrolled

        # Act
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        assert email not in app_module.activities[activity_name]["participants"]

    def test_unregister_not_enrolled_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "noone@mergington.edu"  # not enrolled

        # Act
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_unregister_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "someone@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
