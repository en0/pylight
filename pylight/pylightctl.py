import logging
from argparse import ArgumentParser
from dnry.srvhost.builder import SrvHostBuilder, SrvHostBase, ISrvHost

from pylight.interface import IActionBroker
from pylight.action import Action
from pylight.configure import setup_config, setup_services


class PylightCtl(SrvHostBase):

    _broker: IActionBroker

    @classmethod
    def create_builder(cls):
        return SrvHostBuilder("pylightctl") \
            .config_services(lambda _, ioc: ioc.bind(ISrvHost, PylightCtl))

    def __init__(self, broker: IActionBroker):
        self._broker = broker
        self._log = logging.getLogger(__name__)

    def _get_opts(self):
        ap = ArgumentParser()
        ap.add_argument("ACTION", help="A value or delta to apply to the backlight.")
        return ap.parse_args()

    def run(self):
        opts = self._get_opts()
        action = Action.deserialize(opts.ACTION)
        if action == None:
            self._log.critical("Cannot parse action.")
            exit(1)
        self._log.info(f"Sending action {action}")
        self._broker.send_message(action)


def main():
    PylightCtl \
        .create_builder() \
        .config_configuration(setup_config) \
        .config_services(setup_services) \
        .build() \
        .run()

if __name__ == "__main__":
    main()
