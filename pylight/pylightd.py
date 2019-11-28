import signal
from logging import getLogger, Logger
from dnry.srvhost.builder import SrvHostBuilder, SrvHostBase, ISrvHost

from pylight.interface import IActionBroker, IBacklightManager
from pylight.configure import setup_config, setup_services
from pylight.action import Action


class Pylightd(SrvHostBase):

    _broker: IActionBroker
    _manager: IBacklightManager
    _log: Logger

    @classmethod
    def create_builder(cls):
        return SrvHostBuilder("pylight") \
            .config_services(lambda _, ioc: ioc.bind(ISrvHost, Pylightd))

    def __init__(self, manager: IBacklightManager, broker: IActionBroker):
        self._manager = manager
        self._broker = broker
        self._log = getLogger(__name__)

    def run(self):
        self._log.info("Starting up daemon.")
        while True:
            try:
                action = self._broker.receive_message()
                self._log.debug(f"Received message: {action}")
                self._manager.apply(action)
            except KeyboardInterrupt:
                break
            
        self._log.info("Shuting down daemon.")


def main():
    Pylightd \
        .create_builder() \
        .config_configuration(setup_config) \
        .config_services(setup_services) \
        .build() \
        .run()

if __name__ == "__main__":
    main()
