import asyncio
import json
import threading
from typing import Any, Dict, List

from tinytroupe.environment import TinyWorld

from app.core.logging import logger
from app.services.websocket_service import WebSocketService


class DiscussionWebsocketLogger:
    def __init__(self, world: TinyWorld, websocket_service: WebSocketService):
        self.world = world
        self.websocket_service = websocket_service
        self._polling_thread: threading.Thread | None = None
        self._stop_polling = threading.Event()
        self._loop: asyncio.AbstractEventLoop | None = None
        # track by id(message) to avoid duplicates
        self._forwarded_ids: set[int] = set()
        print("DiscussionWebsocketLogger initialized")

    # ---------- public control ----------

    def start_logging(self) -> None:
        """Start the message polling loop in a separate thread with its own event loop."""
        if self._polling_thread and self._polling_thread.is_alive():
            return  # already running

        self._stop_polling.clear()
        self._polling_thread = threading.Thread(
            target=self._thread_entrypoint,
            daemon=True,
            name="DiscussionWebsocketLogger-Polling",
        )
        self._polling_thread.start()
        logger.log_info("DiscussionWebsocketLogger polling thread started")

    def end_logging(self) -> None:
        """Stop the message polling loop."""
        self._stop_polling.set()
        if self._loop and self._loop.is_running():
            # Wake up the loop if it's sleeping
            asyncio.run_coroutine_threadsafe(asyncio.sleep(0), self._loop)

        if self._polling_thread and self._polling_thread.is_alive():
            self._polling_thread.join(timeout=2.0)
            if self._polling_thread.is_alive():
                logger.log_warning(
                    "DiscussionWebsocketLogger polling thread did not stop gracefully")
            else:
                logger.log_info(
                    "DiscussionWebsocketLogger polling thread stopped")

        self._polling_thread = None
        self._loop = None

    # ---------- threading / asyncio plumbing ----------

    def _thread_entrypoint(self) -> None:
        """Create and run an asyncio event loop in this background thread."""
        self._loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._message_polling_loop())
        except Exception as e:
            logger.log_error(f"Polling loop crashed: {e}")
        finally:
            try:
                pending = asyncio.all_tasks(loop=self._loop)
                for t in pending:
                    t.cancel()
                if pending:
                    self._loop.run_until_complete(
                        asyncio.gather(*pending, return_exceptions=True))
            finally:
                self._loop.close()

    # ---------- helpers ----------

    @staticmethod
    def _parse_message(message: Dict[str, Any]) -> str:
        try:
            return message.get("content", {}).get("action", {}).get("content", "") or ""
        except Exception as e:
            logger.log_error(f"Error parsing message content: {e}")
            return ""

    @staticmethod
    def _parse_sender_name(message: Dict[str, Any]) -> str:
        try:
            return message.get("source", "Unknown") or "Unknown"
        except Exception as e:
            logger.log_error(f"Error parsing sender name: {e}")
            return "Unknown"

    # ---------- async polling ----------

    async def _message_polling_loop(self) -> None:
        logger.log_info("Starting message polling loop")
        try:
            while not self._stop_polling.is_set():
                try:
                    # Copy buffer to avoid concurrent mutation surprises
                    messages: List[Dict[str, Any]] = list(self.world._displayed_communications_buffer)  # noqa: SLF001

                    for message in messages:
                        if message is None:
                            continue

                        # Ensure dict structure
                        if not isinstance(message, dict):
                            continue

                        if message.get("content") is None:
                            continue

                        action = message.get("content").get("action")
                        if not isinstance(action, dict):
                            continue

                        if action.get("type") is None:
                            continue

                        if action.get("type") != "TALK":
                            continue

                        # De-dup by object identity; adjust if you have stable IDs
                        mid = id(message)
                        if mid in self._forwarded_ids:
                            continue
                        self._forwarded_ids.add(mid)

                        message_text = self._parse_message(message).strip()
                        sender_name = self._parse_sender_name(message).strip()

                        payload = {
                            "type": "chat",
                            "name": sender_name,
                            "message": message_text
                        }
                        await self.websocket_service.broadcast_message(json.dumps(payload))

                    # cooperative pause (don’t block the loop)
                    await asyncio.sleep(0.25)

                except Exception as e:
                    logger.log_error(
                        f"Error in message polling iteration: {e}")
                    await asyncio.sleep(1.0)

        finally:
            logger.log_info("Message polling loop stopped")
