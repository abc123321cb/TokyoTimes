class StateMachine:
    def __init__(self):
        self.state = "Idle"

    def set(self, state: str) -> None:
        self.state = state

    def update(self, dt: float) -> None:
        pass
