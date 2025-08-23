"""Example demonstrating WebSocket service usage from different parts of the application."""

import asyncio
import json
from typing import Dict, List

from app.managers.discussion_manager import DiscussionManager
from app.services.websocket_service import WebSocketService


async def example_websocket_usage():
    """Example showing how WebSocket service can be used from different modules."""

    print("=== WebSocket Service Usage Example ===\n")

    # 1. Initialize WebSocket service (normally done in main.py)
    print("1. Initializing WebSocket service...")
    websocket_service = WebSocketService.get_instance()
    websocket_service.initialize_server(host="localhost", port=8765)
    print("   ✓ WebSocket service initialized\n")

    # 2. Access from Discussion Manager
    print("2. Creating Discussion Manager...")
    discussion_manager = DiscussionManager()
    print("   ✓ Discussion Manager created with WebSocket service access\n")

    # 3. Demonstrate broadcasting from Discussion Manager
    print("3. Broadcasting discussion updates...")
    await discussion_manager._broadcast_discussion_update(
        "Discussion manager can now broadcast updates!",
        "info"
    )
    print("   ✓ Discussion update broadcasted\n")

    # 4. Access from any other module
    print("4. Accessing WebSocket service from another module...")
    another_service = WebSocketService.get_instance()
    print(f"   ✓ Same instance: {websocket_service is another_service}")
    print(f"   ✓ Initialized: {another_service.is_initialized()}")
    print(f"   ✓ Client count: {another_service.get_client_count()}\n")

    # 5. Demonstrate broadcasting from any module
    print("5. Broadcasting from another module...")
    await another_service.broadcast_message({
        "type": "example",
        "message": "This message was sent from another module!",
        "timestamp": asyncio.get_event_loop().time()
    })
    print("   ✓ Message broadcasted from another module\n")

    # 6. Show client information
    print("6. Getting client information...")
    client_info = another_service.get_client_info()
    print(f"   ✓ Client info: {client_info}\n")

    # 7. Health check
    print("7. Performing health check...")
    health_status = await another_service.health_check()
    print(f"   ✓ Health status: {json.dumps(health_status, indent=2)}\n")

    print("=== Example completed successfully! ===")


async def example_discussion_with_websocket():
    """Example showing how discussion manager can broadcast during discussion."""

    print("\n=== Discussion with WebSocket Broadcasting Example ===\n")

    # Initialize WebSocket service
    websocket_service = WebSocketService.get_instance()
    if not websocket_service.is_initialized():
        websocket_service.initialize_server(host="localhost", port=8765)

    # Create discussion manager
    discussion_manager = DiscussionManager()

    # Simulate discussion steps with WebSocket broadcasting
    print("Simulating discussion steps with WebSocket broadcasting...")

    # Step 1: Discussion start
    await discussion_manager._broadcast_discussion_update(
        "Starting menu discussion simulation...",
        "info"
    )

    # Step 2: Loading participants
    await discussion_manager._broadcast_discussion_update(
        "Loading participant specifications...",
        "info"
    )
    await asyncio.sleep(0.1)  # Simulate processing time

    await discussion_manager._broadcast_discussion_update(
        "Loaded 5 participants successfully",
        "success"
    )

    # Step 3: Discussion progress
    await discussion_manager._broadcast_discussion_update(
        "Running initial discussion round...",
        "info"
    )
    await asyncio.sleep(0.1)  # Simulate processing time

    await discussion_manager._broadcast_discussion_update(
        "Initial discussion round completed",
        "success"
    )

    # Step 4: Final decision
    await discussion_manager._broadcast_discussion_update(
        "Chef is making final decision...",
        "info"
    )
    await asyncio.sleep(0.1)  # Simulate processing time

    await discussion_manager._broadcast_discussion_update(
        "Chef final decision completed",
        "success"
    )

    # Step 5: Results
    sample_results = {
        "monday": {
            "name": "Pasta Carbonara",
            "ingredients": ["pasta", "eggs", "bacon", "parmesan"]
        },
        "tuesday": {
            "name": "Chicken Curry",
            "ingredients": ["chicken", "rice", "curry spices", "coconut milk"]
        }
    }

    await discussion_manager._broadcast_discussion_result(sample_results)

    print("   ✓ Discussion simulation completed with WebSocket broadcasting\n")
    print("=== Discussion Example completed! ===")


if __name__ == "__main__":
    # Run examples
    asyncio.run(example_websocket_usage())
    asyncio.run(example_discussion_with_websocket())
