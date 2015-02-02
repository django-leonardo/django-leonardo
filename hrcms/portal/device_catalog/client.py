
import logging
from roboticeclient.common.horizon import DjangoClient
from roboticeclient.control.v1.base import RoboticeControlClient

log = logging.getLogger('utils.robotice_client')

# only change base client class
RoboticeControlClient.client_class = DjangoClient

robotice_client = RoboticeControlClient(type="control")