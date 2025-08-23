"""Simple example demonstrating WebSocket service refactoring."""

import asyncio
import json
from typing import Dict, List

from app.services.websocket_service import WebSocketService


async def simple_websocket_example():
    """Simple example showing WebSocket service usage."""

    print("=== WebSocket Service Refactoring Example ===\n")

    # 1. Initialize WebSocket service (normally done in main.py)
    print("1. Initializing WebSocket service...")
    websocket_service = WebSocketService.get_instance()
    websocket_service.initialize_server(host="localhost", port=8765)
    print("   ✓ WebSocket service initialized\n")

    # 2. Access from different modules (simulating different parts of the app)
    print("2. Accessing WebSocket service from different modules...")

    # Simulate access from discussion manager
    discussion_service = WebSocketService.get_instance()
    print(
        f"   ✓ Discussion service same instance: {websocket_service is discussion_service}")

    # Simulate access from another manager
    another_manager = WebSocketService.get_instance()
    print(
        f"   ✓ Another manager same instance: {websocket_service is another_manager}")

    # Simulate access from an endpoint
    endpoint_service = WebSocketService.get_instance()
    print(
        f"   ✓ Endpoint service same instance: {websocket_service is endpoint_service}")
    print()

    # 3. Demonstrate broadcasting from different modules
    print("3. Broadcasting messages from different modules...")

    # Broadcast from "discussion manager"
    await discussion_service.broadcast_message({
        "type": "discussion_update",
        "update_type": "info",
        "message": "Discussion manager can now broadcast updates!",
        "timestamp": asyncio.get_event_loop().time()
    })
    print("   ✓ Message broadcasted from discussion manager")

    # Broadcast from "another manager"
    await another_manager.broadcast_message({
        "type": "system_update",
        "message": "Another manager can also broadcast messages!",
        "timestamp": asyncio.get_event_loop().time()
    })
    print("   ✓ Message broadcasted from another manager")

    # Broadcast from "endpoint"
    await endpoint_service.broadcast_message({
        "type": "endpoint_notification",
        "message": "Endpoint can broadcast too!",
        "timestamp": asyncio.get_event_loop().time()
    })
    print("   ✓ Message broadcasted from endpoint")
    print()

    # 4. Show service status
    print("4. Service status information...")
    print(f"   ✓ Initialized: {websocket_service.is_initialized()}")
    print(f"   ✓ Client count: {websocket_service.get_client_count()}")
    print(f"   ✓ Client info: {websocket_service.get_client_info()}")
    print()

    # 5. Health check
    print("5. Performing health check...")
    health_status = await websocket_service.health_check()
    print(f"   ✓ Health status: {json.dumps(health_status, indent=2)}")
    print()

    # 6. Demonstrate error handling
    print("6. Testing error handling...")

    # Create a new service instance (should be the same due to singleton)
    new_service = WebSocketService()
    print(f"   ✓ New instance is same: {websocket_service is new_service}")

    # Try to initialize again (should fail)
    try:
        new_service.initialize_server()
        print("   ✗ Should have failed - double initialization")
    except RuntimeError as e:
        print(f"   ✓ Correctly prevented double initialization: {e}")
    print()

    print("=== Example completed successfully! ===")
    print("\nKey benefits of this refactoring:")
    print("1. ✅ WebSocket server accessible from anywhere in the application")
    print("2. ✅ Singleton pattern ensures single instance")
    print("3. ✅ Clean separation of concerns")
    print("4. ✅ Easy to use from discussion manager and other modules")
    print("5. ✅ Proper error handling and initialization checks")
    print("6. ✅ No more global variables in endpoint modules")


if __name__ == "__main__":
    # Run the example
    asyncio.run(simple_websocket_example())
