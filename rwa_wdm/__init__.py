import logging

from .sim import simulator

# https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules/15729700#15729700
logging.basicConfig(
    format="[%(asctime)s] [%(module)s] %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO)

# https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules
logging.getLogger("matplotlib").setLevel(logging.WARNING)
