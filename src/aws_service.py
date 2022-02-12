from src.data_handlers.data_loaders import EC2DataLoader
from src.data_handlers.data_containers import EC2Data
from src.connection.instance_connectors import EC2ClientsGenerator

from typing import (
    List
)


class Service:

    def __init__(self, service: str):
        self.service_factory(service)
        self._data: List[EC2Data] = []

    @property
    def data(self) -> List[EC2Data]:
        return self._data

    def service_factory(self, service: str) -> None:
        if service.lower() == 'ec2':
            self.__generator = EC2ClientsGenerator()
            self.__data_loader = EC2DataLoader
        else:
            raise NameError(f"The requested service {service} doesnt exist in list of avilable services")

    def __generate_for_regions(self) -> 'Service':
        self.__generator.populate_clients_by_available_regions()
        return self

    def __load_data(self) -> 'Service':
        self.__data_loader = self.__data_loader.__call__(described_instances=self.__generator.described_instances)
        self.__data_loader.populate_instances_containers()

        return self

    def populate_data(self) -> 'Service':
        self.__generate_for_regions().__load_data()
        self._data = self.__data_loader.instances_data
        return self
