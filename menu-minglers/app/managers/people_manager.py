
# Load environment variables first
import logging
import random

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
Family members say HomeBite is the “kitchen compass” that best translates their different jobs, personalities, and cravings into meals everyone can enjoy.
"""

    family_roles = [
        "A mother, a Swiss primary school teacher, who cares deeply about healthy, balanced meals.",
        "A father, an IT specialist from Zurich, who loves grilling and hearty comfort food.",
        "A teenage daughter, a Swiss gymnasium student, who is vegetarian and experiments with new recipes.",
        "A teenage son, an apprentice electrician, who prefers quick, filling snacks over full meals.",
        "A grandmother, a retired nurse from Bern, who values traditional family recipes.",
        "A grandfather, a retired SBB train conductor, who has a sweet tooth and always pushes for dessert.",
        "An aunt, a Swiss travel agent, who is adventurous and likes to try exotic cuisines.",
        "An uncle, a local banker from St. Gallen, who insists on sticking to simple, familiar dishes.",
        "A cousin, a university student in Lausanne, who follows a strict vegan diet.",
        "A cousin, an apprentice carpenter, who is allergic to nuts and needs safe alternatives.",
        "A little sister, a primary school pupil, who only eats 'kid-friendly' meals like pasta and pizza.",
        "A little brother, a football-obsessed schoolboy, who loves anything spicy.",
        "A family friend, a Swiss civil engineer, who brings structured opinions even into food discussions.",
        "A neighbor, a shop assistant from Basel, who often joins the family dinners and has picky tastes.",
        "A fitness-obsessed sibling, a Swiss ski instructor, who demands high-protein meals.",
        "A sibling, a university student working part-time in a café, who follows intermittent fasting and eats only at certain times.",
        "A grandparent, a retired post office clerk, who requires low-salt, heart-healthy dishes.",
        "A sibling, an aspiring journalist, who critiques every meal as if writing a review.",
        "A cousin, a Swiss medical student, who gives evidence-based advice on nutrition.",
        "A partner, an office clerk in Zug, who is budget-conscious and tries to keep meals affordable."
    ]

    def __init__(self):
        pass

    def get_family_members(self, person_count: int) -> list[TinyPerson]:
        factory = TinyPersonFactory(self.family_context)

        random.shuffle(self.family_roles)
        random_family_roles = self.family_roles[:person_count]

        family_members = []
        for i, role in enumerate(random_family_roles, 1):
            logger.info(
                f"Generating person {i}/{person_count} with role: {role}")
            person = factory.generate_person(role)
            logger.info(f"Generated person {i}: {person.minibio()}")
            family_members.append(person)

        logger.info(
            f"Successfully generated {len(family_members)} family members")
        return family_members
