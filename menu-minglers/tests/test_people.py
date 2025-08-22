"""Tests for people endpoints."""

from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestFamilyMembersEndpoint:
    """Test cases for the family members endpoint."""

    def test_generate_family_members_default_count(self):
        """Test generating family members with default count."""
        with patch('app.api.v1.endpoints.people.PeopleManager') as mock_manager:
            # Mock the TinyPerson objects with _persona attribute
            mock_person = Mock()
            mock_person._persona = {
                "name": "Sarah Johnson",
                "role": "A mother who cares deeply about healthy, balanced meals.",
                "personality": "Sarah is nurturing and organized.",
                "preferences": "Prefers organic ingredients."
            }

            mock_manager_instance = Mock()
            mock_manager_instance.get_family_members.return_value = [
                mock_person]
            mock_manager_instance.family_context = "HomeBite is a close-knit family kitchen collective..."
            mock_manager.return_value = mock_manager_instance

            response = client.get("/api/v1/family-members")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 5  # Default count
            assert len(data["family_members"]) == 1
            assert data["family_members"][0]["persona"]["name"] == "Sarah Johnson"
            assert "context" in data

    def test_generate_family_members_custom_count(self):
        """Test generating family members with custom count."""
        with patch('app.api.v1.endpoints.people.PeopleManager') as mock_manager:
            # Mock the TinyPerson objects with _persona attribute
            mock_person1 = Mock()
            mock_person1._persona = {
                "name": "John Smith",
                "role": "A father who loves grilling.",
                "personality": "John is adventurous and loves cooking outdoors.",
                "preferences": "Prefers grilled meats and hearty dishes."
            }

            mock_person2 = Mock()
            mock_person2._persona = {
                "name": "Emma Smith",
                "role": "A teenage daughter who is vegetarian.",
                "personality": "Emma is creative and health-conscious.",
                "preferences": "Prefers plant-based meals and experiments with new recipes."
            }

            mock_manager_instance = Mock()
            mock_manager_instance.get_family_members.return_value = [
                mock_person1, mock_person2]
            mock_manager_instance.family_context = "HomeBite is a close-knit family kitchen collective..."
            mock_manager.return_value = mock_manager_instance

            response = client.get("/api/v1/family-members?count=2")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 2
            assert len(data["family_members"]) == 2
            assert data["family_members"][0]["persona"]["name"] == "John Smith"
            assert data["family_members"][1]["persona"]["name"] == "Emma Smith"

    def test_generate_family_members_invalid_count_too_low(self):
        """Test generating family members with count too low."""
        response = client.get("/api/v1/family-members?count=0")

        assert response.status_code == 422  # FastAPI validation error
        assert "Input should be greater than or equal to 1" in response.json()[
            "detail"][0]["msg"]

    def test_generate_family_members_invalid_count_too_high(self):
        """Test generating family members with count too high."""
        response = client.get("/api/v1/family-members?count=21")

        assert response.status_code == 422  # FastAPI validation error
        assert "Input should be less than or equal to 20" in response.json()[
            "detail"][0]["msg"]

    def test_generate_family_members_manager_exception(self):
        """Test handling of manager exceptions."""
        with patch('app.api.v1.endpoints.people.PeopleManager') as mock_manager:
            mock_manager_instance = Mock()
            mock_manager_instance.get_family_members.side_effect = Exception(
                "Test error")
            mock_manager.return_value = mock_manager_instance

            response = client.get("/api/v1/family-members")

            assert response.status_code == 500
            assert "Failed to generate family members" in response.json()[
                "detail"]
