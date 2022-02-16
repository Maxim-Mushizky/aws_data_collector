from src.data_handlers.data_loaders import EC2DataLoader
from src.data_handlers.data_containers import EC2Data
from src.connection.instance_connectors import EC2ClientsGenerator
from src.logger import logger

from typing import (
    List,
    Dict,
    Optional
)


class EC2DataReader:

    def __init__(self, credentials: Optional[List[Dict[str, str]]] = None):
        self.__credentials = credentials
        self._data: List = []

    @property
    def data(self) -> List[EC2Data]:
        return self._data

    def __read_data(self, **genkwargs):
        generator = EC2ClientsGenerator(**genkwargs)
        generator.populate_clients_by_available_regions()
        data_loader = EC2DataLoader(generator.described_instances)
        data_loader.populate_instances_containers()
        return data_loader.instances_data

    def populate_data(self):
        if self.__credentials is not None:
            for cred in self.__credentials:
                self._data.append(self.__read_data(**cred))
        else:
            self._data = self.__read_data()
        logger.info("finished populating data. Can now access it with dataclass interface")
        return self.data
