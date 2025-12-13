from collections import defaultdict
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable) -> None:
        self._subscribers[topic].append(callback)

    def publish(self, topic: str, *args, **kwargs) -> None:
        for cb in self._subscribers.get(topic, []):
            cb(*args, **kwargs)
