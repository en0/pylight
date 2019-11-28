import logging
from os.path import join
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

    log_cfg = ctx.configuration.get_section("Logging")
    log_level = log_cfg.get("Level") or "INFO"
    log_path = log_cfg.get("Path")
    if log_path is None:
        logging.basicConfig(level=log_level)
    else:
        log_path = join(log_path, f"{ctx.environment.application_name}.log")
        logging.basicConfig(filename=log_path, level=log_level)
