import logging
from dnry.config import IConfigSection

from pylight.interface import IBacklight


class Backlight(IBacklight):

    def __init__(self, config: IConfigSection):
        self._min = config.get("Backlight:Min")
        self._max = config.get("Backlight:Max")
        self._file = config.get("Backlight:File")
        self._log = logging.getLogger(__name__)

    @property
    def level(self) -> int:
        with open(self._file, 'r') as fd:
            val = int(fd.read())
            self._log.debug(f"Read level {val}")
            return val


    @level.setter
    def level(self, val: int):
        val = min([self._max, val])
        val = max([self._min, val])
        self._log.debug(f"Setting level {val}")
        with open(self._file, 'w') as fd:
            fd.write(str(val))
