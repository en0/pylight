from argparse import ArgumentParser
from dnry.srvhost.builder import SrvHostBuilder, SrvHostBase, ISrvHost

from pylightd.interface import IActionBroker
from pylightd.action import Action
from pylightd.configure import setup_config, setup_services


class ServiceHost(SrvHostBase):

    _broker: IActionBroker

    @classmethod
    def create_builder(cls):
        return SrvHostBuilder("pylightctl") \
            .config_services(lambda _, ioc: ioc.bind(ISrvHost, ServiceHost))

    def __init__(self, broker: IActionBroker):
        self._broker = broker

    def _get_opts(self):
        ap = ArgumentParser()
        ap.add_argument("ACTION", help="A value or delta to apply to the backlight.")
        return ap.parse_args()

    def run(self):
        opts = self._get_opts()
        action = Action.deserialize(opts.ACTION)
        self._broker.send_message(action)


def main():
    ServiceHost \
        .create_builder() \
        .config_configuration(setup_config) \
        .config_services(setup_services) \
        .build() \
        .run()

if __name__ == "__main__":
    main()
