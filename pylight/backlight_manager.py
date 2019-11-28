from pylight.interface import IBacklightManager, IBacklight
from pylight.action import Action


class BacklightManager(IBacklightManager):
    _bl: IBacklight
    def __init__(self, bl: IBacklight):
        self._bl = bl

    def apply(self, action: Action):
        if action.operator == '+':
            self._bl.level += action.value
        elif action.operator == '-':
            self._bl.level -= action.value
        elif action.operator == '=':
            self._bl.level = action.value
