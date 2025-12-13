from typing import List

class SceneStack:
    def __init__(self):
        self._stack: List[object] = []

    def push(self, scene: object) -> None:
        self._stack.append(scene)

    def pop(self) -> object | None:
        return self._stack.pop() if self._stack else None

    def top(self) -> object | None:
        return self._stack[-1] if self._stack else None

    def draw(self, surface) -> None:
        for scene in self._stack:
            scene.draw(surface)

    def update_lower(self, dt: float) -> None:
        for scene in self._stack[:-1]:
            scene.update(dt)
