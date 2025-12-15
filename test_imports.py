#!/usr/bin/env python3
"""Quick test to check if modules import without errors."""

try:
    print("Importing ai.state_machine...")
    from ai.state_machine import StateMachine, IdleState, WanderState, TravelToSceneState
    print("  OK")
    
    print("Importing entities.npc...")
    from entities.npc import NPC
    print("  OK")
    
    print("Importing scenes.base_scene...")
    from scenes.base_scene import MaskedScene
    print("  OK")
    
    print("\nAll imports successful!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
