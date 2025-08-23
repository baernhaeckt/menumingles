
import asyncio

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinySocialNetwork, TinyWorld
from tinytroupe.extraction import ResultsExtractor
from tinytroupe.factory import TinyPersonFactory

from app.core.logging import logger
from app.managers.discussion_websocket_logger import DiscussionWebsocketLogger
from app.services.websocket_service import WebSocketService


class DiscussionManager:

    situation = """
You are a focused group chat that discusses the menu for the next week for all the people in the group.
The menu is a list of dishes with the ingredients for each day.
"""

    menu_description_template = """
    The menu for the next week is:
    {menu}
"""

    task = """
Be brief and utilitarian, concise and answer directly. Answer in one to three sentences. Think about the menu and the ingredients for each day. Tell if you like the dish or not. Do not tell things that others already know or said. Always give feedback about all dishes and ingredients in one message.
"""

    chef_thoughts = """
I am the chef and I am responsible for the menu. I will make the final decision for delicous dishes. I am able to switch ingredients based on the wishes of the group and the suggestions of the consultants. I do not discuss about my personal like or dislike of the dishes and their ingredients, but only about my professional opinion about the ingredients.
"""

    consultant_thoughts = """
I am a consultant and I am here to help in my specific field. I am able to suggest ingredients based on the wishes of the group and the suggestions of the chef. I do not discuss about my personal like or dislike of the dishes and their ingredients, but only about my professional opinion about the ingredients.
"""

    extraction_objective = """
Quickly extract the final weekly menu (one menu per day) as a SINGLE JSON object with EXACTLY this schema and nothing else:
{
    "monday": {
        "name": "The name of the dish for Monday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    },
    "tuesday": {
        "name": "The name of the dish for Tuesday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    },
    "wednesday": {
        "name": "The name of the dish for Wednesday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    },
    "thursday": {
        "name": "The name of the dish for Thursday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    },
    "friday": {
        "name": "The name of the dish for Friday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    },
    "saturday": {
        "name": "The name of the dish for Saturday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    },
    "sunday": {
        "name": "The name of the dish for Sunday",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
    }
}
    """

    def __init__(self):
        self.websocket_service = WebSocketService.get_instance()

    def discuss_menus(self, people: list[dict], chef: dict, consultants: list[dict], menu: list[dict]) -> dict:
        """Start a menu discussion with the given participants and menu."""
        logger.log_info("Starting menu discussion", additional_context={
            "participants_count": len(people),
            "consultants_count": len(consultants),
            "menu_items_count": len(menu),
            "chef_name": chef.get("name", "Unknown")
        })

        try:
            # Load chef specification
            logger.log_debug("Loading chef specification")
            chef = TinyPerson.load_specification(chef)
            logger.log_info("Chef loaded successfully", additional_context={
                "chef_name": chef["name"]
            })

            # Load people specifications
            logger.log_debug("Loading people specifications")
            persons = [
                TinyPerson.load_specification(person)
                for person in people
            ]
            logger.log_info("People loaded successfully", additional_context={
                "people_count": len(persons),
                "people_names": [person["name"] for person in persons]
            })

            # Load consultants specifications
            logger.log_debug("Loading consultants specifications")
            consultants = [
                TinyPerson.load_specification(consultant)
                for consultant in consultants
            ]
            logger.log_info("Consultants loaded successfully", additional_context={
                "consultants_count": len(consultants),
                "consultant_names": [consultant["name"] for consultant in consultants]
            })

            # Combine all participants
            persons.append(chef)
            persons.extend(consultants)
            logger.log_info("All participants combined", additional_context={
                "total_participants": len(persons)
            })

            # Create focus group
            logger.log_debug("Creating focus group")
            focus_group = TinyWorld(
                "Group chat for menu discussion",
                persons
            )
            logger.log_info("Focus group created successfully")

            # Create websocket logger
            websocket_logger = DiscussionWebsocketLogger(
                focus_group, self.websocket_service)
            websocket_logger.start_logging()

            # Prepare discussion content
            menu_description = self.menu_description_template.format(menu=menu)
            task = self.task.format(chef_name=chef["name"])
            logger.log_debug("Discussion content prepared", additional_context={
                "task_chef_name": chef["name"]
            })

            # Broadcast initial messages
            logger.log_debug("Broadcasting initial messages to focus group")
            focus_group.broadcast(self.situation)
            focus_group.broadcast(menu_description)
            focus_group.broadcast(task)
            logger.log_info("Initial messages broadcasted successfully")

            # Initialize thoughts
            logger.log_debug("Initializing chef thoughts")
            chef.think(self.chef_thoughts)
            logger.log_info("Chef thoughts initialized")

            logger.log_debug("Initializing consultant thoughts")
            for consultant in consultants:
                consultant.think(self.consultant_thoughts)
            logger.log_info("Consultant thoughts initialized", additional_context={
                "consultants_initialized": len(consultants)
            })

            # Run initial discussion
            logger.log_debug("Running initial discussion round")
            focus_group.run(1)
            logger.log_info("Initial discussion round completed")

            # Broadcast final decision request
            final_decision_message = """
Make the final decision for the weekly menu. Announce exactly which dishes are chosen for each day of the week, including their full list of ingredients.

Rules:

* Respect all requests and preferences expressed by the group and the consultants.
* Each day must have exactly one dish. No day may remain empty or contain a placeholder.
* Use existing proposed dishes whenever possible, but do not repeat the same dish.
* If there are not enough dishes, create new ones. New dishes must be unique, clearly different from the existing ones, and include complete ingredient lists.
* Ensure the final menu contains only unique dishes—no duplicates.
* Replace any ingredients that the group rejected or that are not seasonally available with suitable alternatives.
* Do not overthink or add commentary. Deliver the final, concrete list of dishes with ingredients, covering all days.
"""
            logger.log_debug("Broadcasting final decision request")
            focus_group.broadcast(final_decision_message)

            # Chef makes final decision
            logger.log_debug("Chef making final decision")
            chef.act()
            logger.log_info("Chef final decision completed")

            # Extract results
            logger.log_debug("Extracting results from discussion")
            extractor = ResultsExtractor()
            results = extractor.extract_results_from_world(
                focus_group,
                extraction_objective=self.extraction_objective,
                fields=["monday", "tuesday", "wednesday",
                        "thursday", "friday", "saturday", "sunday"],
            )
            logger.log_info("Results extracted successfully", additional_context={
                "result_keys": list(results.keys()) if isinstance(results, dict) else "No results"
            })

            websocket_logger.end_logging()

            return results

        except Exception as e:
            logger.log_error(e, additional_context={
                "method": "discuss_menus",
                "participants_count": len(people),
                "consultants_count": len(consultants),
                "menu_items_count": len(menu)
            })
            raise
