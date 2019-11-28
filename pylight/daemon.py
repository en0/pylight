from threading import Event
from dnry.srvhost.builder import SrvHostBuilder, SrvHostBase, ISrvHost

from pylight.interface import IActionBroker, IBacklightManager
from pylight.configure import setup_config, setup_services


class ServiceHost(SrvHostBase):

    _broker: IActionBroker
    _manager: IBacklightManager
    _event: Event

    @classmethod
    def create_builder(cls):
        return SrvHostBuilder("pylight") \
            .config_services(lambda _, ioc: ioc.bind(ISrvHost, ServiceHost))

    def __init__(self, manager: IBacklightManager, broker: IActionBroker):
        self._manager = manager
        self._broker = broker
        self._event = Event()

    def run(self):
        # TODO: Shutdown hooks?
        while not self._event.is_set():
            action = self._broker.receive_message()
            self._manager.apply(action)


def main():
    ServiceHost \
        .create_builder() \
        .config_configuration(setup_config) \
        .config_services(setup_services) \
        .build() \
        .run()

if __name__ == "__main__":
    main()
