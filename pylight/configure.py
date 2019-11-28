from pyioc3 import StaticContainerBuilder
from dnry.srvhost.builder import ISrvHostContext
from dnry.config.yaml import YamlSource
from dnry.config import IConfigFactory

from pylight.backlight import Backlight
from pylight.action_broker import ActionBroker
from pylight.backlight_manager import BacklightManager
from pylight.interface import IActionBroker, IBacklight, IBacklightManager

def setup_config(ctx: ISrvHostContext, conf: IConfigFactory):
    conf.add_source(YamlSource([
        "./pylight.yaml",
        "/etc/pylight/pylight.yaml"
    ], True))


def setup_services(ctx: ISrvHostContext, services: StaticContainerBuilder):
    services.bind(IActionBroker, ActionBroker)
    services.bind(IBacklight, Backlight)
    services.bind(IBacklightManager, BacklightManager)
