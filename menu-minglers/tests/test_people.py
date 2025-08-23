"""Tests for people endpoints."""

import pytest
from pydantic import ValidationError

from app.models.people import (
    AgentPersonGenerationRequest,
    AgentPersonResponse,
    Persona,
    PersonGenerationRequest,
    PersonResponse,
)


class TestPersonModels:
    """Test cases for person models."""

    def test_person_generation_request_valid(self):
        """Test valid person generation request."""
        request_data = {
            "gender": "female",
            "name": "Sarah Johnson",
            "preferences": ["organic food", "quick meals"],
            "intolerances": ["lactose"],
            "short_term_goals": ["lose weight"],
            "long_term_goals": ["maintain healthy lifestyle"]
        }

        request = PersonGenerationRequest(**request_data)
        assert request.gender == "female"
        assert request.name == "Sarah Johnson"
        assert request.preferences == ["organic food", "quick meals"]
        assert request.intolerances == ["lactose"]
        assert request.short_term_goals == ["lose weight"]
        assert request.long_term_goals == ["maintain healthy lifestyle"]

    def test_person_generation_request_missing_fields(self):
        """Test person generation request with missing fields."""
        request_data = {
            "gender": "female",
            "name": "Sarah Johnson"
            # Missing required fields
        }

        with pytest.raises(ValidationError):
            PersonGenerationRequest(**request_data)

    def test_agent_person_generation_request_valid(self):
        """Test valid agent person generation request."""
        request_data = {
            "gender": "female",
            "name": "Dr. Maria Schmidt",
            "expertise": "nutrition science"
        }

        request = AgentPersonGenerationRequest(**request_data)
        assert request.gender == "female"
        assert request.name == "Dr. Maria Schmidt"
        assert request.expertise == "nutrition science"

    def test_agent_person_generation_request_missing_fields(self):
        """Test agent person generation request with missing fields."""
        request_data = {
            "gender": "female"
            # Missing required fields
        }

        with pytest.raises(ValidationError):
            AgentPersonGenerationRequest(**request_data)

    def test_person_response_valid(self):
        """Test valid person response."""
        persona_data = {
            "name": "Sarah Johnson",
            "role": "A female person named Sarah Johnson who likes ['organic food', 'quick meals'].",
            "personality": "Sarah is nurturing and organized."
        }

        response_data = {
            "person": {"persona": persona_data},
            "context": "HomeBite is a typical Swiss family household..."
        }

        response = PersonResponse(**response_data)
        assert response.person.persona["name"] == "Sarah Johnson"
        assert "HomeBite is a typical Swiss family household" in response.context

    def test_agent_person_response_valid(self):
        """Test valid agent person response."""
        persona_data = {
            "name": "Dr. Maria Schmidt",
            "role": "A female person named Dr. Maria Schmidt that is an absolute expert in nutrition science.",
            "personality": "Dr. Schmidt is passionate about nutrition science."
        }

        response_data = {
            "agent": {"persona": persona_data},
            "context": "HomeBite Experts are a diverse circle of specialists..."
        }

        response = AgentPersonResponse(**response_data)
        assert response.agent.persona["name"] == "Dr. Maria Schmidt"
        assert "HomeBite Experts are a diverse circle of specialists" in response.context

    def test_persona_model_valid(self):
        """Test valid persona model."""
        persona_data = {
            "name": "Test Person",
            "role": "Test role",
            "personality": "Test personality"
        }

        persona = Persona(persona=persona_data)
        assert persona.persona["name"] == "Test Person"
        assert persona.persona["role"] == "Test role"
        assert persona.persona["personality"] == "Test personality"
