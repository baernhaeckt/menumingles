
import asyncio
import threading
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinySocialNetwork, TinyWorld
from tinytroupe.extraction import ResultsExtractor
from tinytroupe.factory import TinyPersonFactory

from app.core.logging import logger
from app.managers.discussion_websocket_logger import DiscussionWebsocketLogger
from app.services.websocket_service import WebSocketService


class DiscussionStatus(Enum):
    """Status of a discussion task."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class DiscussionTask:
    """Represents a discussion task with its state."""

    def __init__(self, task_id: str, request_data: dict):
        self.task_id = task_id
        self.request_data = request_data
        self.status = DiscussionStatus.PENDING
        self.result: Optional[dict] = None
        self.error: Optional[str] = None
        self.created_at = datetime.now(timezone.utc)
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None


class BackgroundDiscussionManager:
    """Manages background discussion tasks with singleton pattern."""

    _instance: Optional['BackgroundDiscussionManager'] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._tasks: Dict[str, DiscussionTask] = {}
            self._current_task_id: Optional[str] = None
            self._task_lock = threading.Lock()
            self._initialized = True

    def start_discussion(self, request_data: dict) -> str:
        """
        Start a new discussion task.

        Args:
            request_data: The discussion request data

        Returns:
            str: The task ID

        Raises:
            RuntimeError: If another discussion is already running
        """
        with self._task_lock:
            if self._current_task_id is not None:
                current_task = self._tasks.get(self._current_task_id)
                if current_task and current_task.status in [DiscussionStatus.PENDING, DiscussionStatus.RUNNING]:
                    raise RuntimeError("Another discussion is already running")

            # Create new task
            task_id = str(uuid.uuid4())
            task = DiscussionTask(task_id, request_data)
            self._tasks[task_id] = task
            self._current_task_id = task_id

            # Start background thread
            thread = threading.Thread(
                target=self._run_discussion_task,
                args=(task_id,),
                daemon=True
            )
            thread.start()

            return task_id

    def get_task_status(self, task_id: str) -> Optional[DiscussionTask]:
        """Get the status of a discussion task."""
        return self._tasks.get(task_id)

    def _run_discussion_task(self, task_id: str):
        """Run the discussion task in a background thread."""
        task = self._tasks.get(task_id)
        if not task:
            return

        try:
            # Update status to running
            task.status = DiscussionStatus.RUNNING
            task.started_at = datetime.now(timezone.utc)

            # Create discussion manager and run discussion
            discussion_manager = DiscussionManager()
            result = discussion_manager.discuss_menus(
                people=task.request_data["people"],
                chef=task.request_data["chef"],
                consultants=task.request_data["consultants"],
                menu=task.request_data["menu"]
            )

            # Update task with result
            task.result = result
            task.status = DiscussionStatus.COMPLETED
            task.completed_at = datetime.now(timezone.utc)

            logger.log_info("Background discussion completed successfully", additional_context={
                "task_id": task_id,
                "duration_seconds": (task.completed_at - task.started_at).total_seconds()
            })

        except Exception as e:
            # Update task with error
            task.error = str(e)
            task.status = DiscussionStatus.FAILED
            task.completed_at = datetime.now(timezone.utc)

            logger.log_error(e, additional_context={
                "task_id": task_id,
                "method": "_run_discussion_task"
            })

        finally:
            # Clear current task if this was the active one
            with self._task_lock:
                if self._current_task_id == task_id:
                    self._current_task_id = None


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
