import logging
import DEFINITIONS
import os

_LOGGER_NAME = 'app.log'
_FILEMODE = 'w'

logger_folder = os.path.join(DEFINITIONS.ROOT, "log")
if not os.path.exists(logger_folder):
    os.mkdir(logger_folder)
if os.path.exists(os.path.join(logger_folder, _LOGGER_NAME)):
    _FILEMODE = 'a'
logging.basicConfig(filename=os.path.join(logger_folder, _LOGGER_NAME),
                    filemode=_FILEMODE,
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger("aws_data_collector")
