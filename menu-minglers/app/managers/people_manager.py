
# Load environment variables first
import logging
import random
from typing import List

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinySocialNetwork, TinyWorld
from tinytroupe.factory import TinyPersonFactory

# Configure logging
logger = logging.getLogger(__name__)


class PeopleManager:

    family_context: str = """
HomeBite is a typical Swiss family household where meals bring everyone together.
Each family member has their own busy life with work, school, and hobbies, yet they all gather around the table to share food and ideas.
Their conversations reflect the diversity of modern Swiss life: some focus on health, others on tradition, some on saving time, and others on experimenting with new flavors.
The family has a reputation for balancing everyday routines with a sense of curiosity, turning ordinary dinners into lively discussions about taste, culture, and practicality.
Every member of the family lives in Switzerland—whether in Zürich, Basel, Geneva, Bern, Lugano, or a smaller town—bringing regional habits, dialects, and traditions into their shared meals.
Family members say HomeBite is the “kitchen compass” that best translates their different jobs, personalities, and cravings into meals everyone can enjoy.
"""

    agent_context: str = """
HomeBite Experts are a diverse circle of Swiss specialists who each bring deep knowledge in their respective fields.
They are passionate about their expertise and see themselves as guardians of quality, accuracy, and best practice.
Although they are approachable and friendly in tone, they do not hesitate to enforce standards, correct misconceptions, or insist on discipline when their topic requires it.
Their role is not only to advise but also to challenge—pushing others to respect the importance of their domain while remaining open to questions and mistakes.
They strive for clarity, balance, and precision, yet are forgiving when someone learns or grows through their guidance.
Each Expert lives in a different Swiss city—whether Zürich, Basel, Lugano, Lausanne, or a smaller town—adding a unique regional flavor to their perspective.
Together, the Experts form a collective voice of authority that keeps discussions grounded, practical, and reliably anchored in professional Swiss insight.
"""

    person_role_template: str = """
A {gender} person named {name} who likes {preferences}. Has {intolerances} food-intolerances. Has {short_term_goals} as short-term goals and {long_term_goals} as long-term goals.
"""

    agent_role_template: str = """
A {gender} person named {name} with the following expertise: {expertise}.
"""

    def __init__(self):
        pass

    def generate_person(self, gender: str, name: str, preferences: list[str], intolerances: list[str], short_term_goals: list[str], long_term_goals: list[str]) -> TinyPerson:
        """Generate a person with a given name, preferences, intolerances, short-term goals, and long-term goals."""
        person_spec = self.person_role_template.format(
            gender=gender,
            name=name,
            preferences=", ".join(preferences),
            intolerances=", ".join(intolerances),
            short_term_goals=", ".join(short_term_goals),
            long_term_goals=", ".join(long_term_goals)
        )

        family_factory = TinyPersonFactory(self.family_context)

        return family_factory.generate_person(person_spec)

    def generate_agent_person(self, gender: str, name: str, expertise: str) -> TinyPerson:
        """Generate an agent person with a given name and role."""
        agent_spec = self.agent_role_template.format(
            gender=gender,
            name=name,
            expertise=expertise
        )

        agent_factory = TinyPersonFactory(self.agent_context)
        return agent_factory.generate_person(agent_spec)
