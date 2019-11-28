from pyioc3 import StaticContainerBuilder
from dnry.srvhost.builder import ISrvHostContext
from dnry.config.yaml import YamlSource
from dnry.config import IConfigFactory

from pylightd.backlight import Backlight
from pylightd.action_broker import ActionBroker
from pylightd.backlight_manager import BacklightManager
from pylightd.interface import IActionBroker, IBacklight, IBacklightManager

def setup_config(ctx: ISrvHostContext, conf: IConfigFactory):
    conf.add_source(YamlSource([
        "./pylightd.yaml",
        "/etc/pylight/pylightd.yaml"
    ], True))


def setup_services(ctx: ISrvHostContext, services: StaticContainerBuilder):
    services.bind(IActionBroker, ActionBroker)
    services.bind(IBacklight, Backlight)
    services.bind(IBacklightManager, BacklightManager)
