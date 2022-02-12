import boto3
import abc
from botocore.exceptions import (
    ClientError
)
from botocore.client import BaseClient

from typing import (
    List,
    Dict,
    Optional
)

AWSClient = BaseClient


class SingletonMeta(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ClientsGenerator(metaclass=SingletonMeta):
    _service_name: str

    @property
    @abc.abstractmethod
    def clients(self) -> List[AWSClient]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def described_instances(self) -> List[Dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def populate_clients_by_available_regions(self) -> List[AWSClient]:
        raise NotImplementedError

    @abc.abstractmethod
    def connect_to_client_by_region(self, region_name: Optional[str] = None) -> AWSClient:
        raise NotImplementedError


class EC2ClientsGenerator(ClientsGenerator, metaclass=SingletonMeta):
    _service_name: str = 'ec2'

    def __init__(self):
        self.default_client: AWSClient = self.connect_to_client_by_region()
        self._clients: List[AWSClient] = [self.default_client]
        self._described_instances: List[Dict] = [self.default_client.describe_instances()]

    @property
    def clients(self) -> List[AWSClient]:
        return self._clients

    @property
    def described_instances(self) -> List[Dict]:
        return self._described_instances

    def connect_to_client_by_region(self, region_name: Optional[str] = None) -> AWSClient:
        if region_name is None:
            return boto3.client(self._service_name)
        return boto3.client(self._service_name, region_name=region_name)

    def populate_clients_by_available_regions(self) -> List[AWSClient]:
        regions_data = self.default_client.describe_regions()
        for region in regions_data['Regions']:
            region_name = region['RegionName']
            if self.default_client.meta.region_name != region_name:
                try:
                    new_client = self.connect_to_client_by_region(region_name=region_name)
                    described_inst = new_client.describe_instances()
                except ClientError:
                    print(f"Connection request to region {region['RegionName']}: FAILURE")
                else:
                    print(f"Connection request to region {region['RegionName']}: SUCCESS")
                    self._clients.append(new_client)
                    self._described_instances.append(described_inst)
        print(f"Summary: Connection was established for regions {[client.meta.region_name for client in self._clients]}"
              f" for service {self._service_name}")
        return self._clients
