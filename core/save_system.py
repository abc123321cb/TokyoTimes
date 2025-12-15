import json
from pathlib import Path


class SaveSystem:
    def __init__(self, base: Path):
        self.base = base
        self.base.mkdir(parents=True, exist_ok=True)

    def capture_run_state(self, game) -> dict:
        """Snapshot the current run state for saving."""
        current_scene = "unknown"
        player = None
        for scene in game.stack._stack:
            if hasattr(scene, "scene_name") and scene.scene_name:
                current_scene = scene.scene_name
            if hasattr(scene, "player") and scene.player:
                player = scene.player
                break

        player_state = {}
        selected_inventory_slot = 0
        if player:
            player_state = {
                "x": getattr(player, "x", 0),
                "y": getattr(player, "y", 0),
                "direction": getattr(player, "direction", "down"),
                "inventory": list(getattr(getattr(player, "inventory", None), "items", [])),
            }
        # Get the current scene's selected inventory slot
        for scene in game.stack._stack:
            if hasattr(scene, "selected_inventory_slot"):
                selected_inventory_slot = scene.selected_inventory_slot
                break

        # Capture persistent world objects
        from world import world_registry

        world_state = world_registry.snapshot_world_state()

        return {
            "scene": current_scene,
            "room": current_scene,  # Kept for compatibility with load UI
            "player": player_state,
            "world": world_state,
            "dropped_items": game.dropped_items,
            "picked_up_items": list(getattr(game, "picked_up_items", set())),
            "selected_inventory_slot": selected_inventory_slot,
        }

    def apply_run_state(self, game, run_state: dict) -> None:
        """Restore parts of the run state onto the live game objects."""
        if not run_state:
            return

        # Restore global item tracking
        game.dropped_items = run_state.get("dropped_items", {})
        game.picked_up_items = set(run_state.get("picked_up_items", []))

        from world import world_registry

        world_registry.apply_world_state(run_state.get("world", {}), game)

        # Restore player basics and inventory slot if present
        player_state = run_state.get("player", {})
        selected_inventory_slot = run_state.get("selected_inventory_slot", 0)
        if player_state:
            applied = False
            for scene in game.stack._stack:
                if hasattr(scene, "player") and scene.player:
                    self.apply_player_state(scene.player, player_state, selected_inventory_slot)
                    applied = True
                    break
            if not applied:
                # Store for later application after a new scene creates the player
                game.pending_player_state = player_state
                game.pending_inventory_slot = selected_inventory_slot

    def apply_player_state(self, player, player_state: dict, selected_inventory_slot: int = 0) -> None:
        """Apply player-specific state onto an existing player instance."""
        if not player_state or not player:
            return
        player.x = player_state.get("x", getattr(player, "x", 0))
        player.y = player_state.get("y", getattr(player, "y", 0))
        player.direction = player_state.get("direction", getattr(player, "direction", "down"))
        if hasattr(player, "inventory") and "inventory" in player_state:
            # Restore inventory list - preserve all slots including empty ones
            saved_items = player_state.get("inventory", [])
            player.inventory.items = list(saved_items) if saved_items else []

    def save(self, slot: str, run_state: dict, knowledge_state: dict) -> None:
        payload = {"run": run_state, "knowledge": knowledge_state}
        # Save with None values preserved (null in JSON)
        (self.base / f"{slot}.sav").write_text(json.dumps(payload, indent=2, default=str))

    def load(self, slot: str) -> tuple[dict, dict]:
        p = self.base / f"{slot}.sav"
        if not p.exists():
            return {}, {}
        data = json.loads(p.read_text())
        return data.get("run", {}), data.get("knowledge", {})
