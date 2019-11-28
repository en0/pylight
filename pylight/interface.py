from abc import ABC, abstractmethod

from pylightd.action import Action


class IActionBroker(ABC):
    @abstractmethod
    def receive_message(self) -> Action:
        raise NotImplementedError()
    def send_message(self, action: Action):
        raise NotImplementedError()


class IBacklight(ABC):
    @property
    @abstractmethod
    def level(self) -> int:
        raise NotImplementedError()

    @level.setter
    @abstractmethod
    def level(self, val: int):
        raise NotImplementedError()


class IBacklightManager(ABC):
    @abstractmethod
    def apply(self, action: Action):
        raise NotImplementedError()
