from typing import List
from os import mkfifo, path
from dnry.srvhost.builder import SrvHostBase
from dnry.config import IConfigSection

from pylightd.interface import IActionBroker
from pylightd.action import Action


class ActionBroker(IActionBroker):

    _fifo: str

    def __init__(self, config: IConfigSection):
        self._fifo = config.get("Ipc:Fifo")
        self._messages = None

    def receive_message(self) -> Action:
        if self._messages is None:
            self._messages = self._create_message_generator()
        return next(self._messages)

    def send_message(self, action: Action):
        self._init_fifo()
        with open(self._fifo, 'w') as fd:
            fd.write(f"{action.serialize()}\n")

    def _create_message_generator(self) -> Action:
        self._init_fifo()
        while True:
            for command in self._get_command():
                action = Action.deserialize(command)
                if action is not None:
                    yield action

    def _get_command(self) -> List[Action]:
        commands = list()
        with open(self._fifo, 'r') as fd:
            while True:
                ## Blocks until message is available
                l = fd.readline()
                if len(l) == 0:
                    break
                commands.append(l[:-1])
        return commands

    def _init_fifo(self):
        if not path.exists(self._fifo):
            mkfifo(self._fifo)
