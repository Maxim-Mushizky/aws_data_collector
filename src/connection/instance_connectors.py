import boto3

from botocore.exceptions import (
    ClientError,
    PartialCredentialsError
)
from botocore.client import BaseClient
from typing import (
    List,
    Dict,
    Optional
)
from src.logger import logger


class EC2ClientsGenerator:
    _service_name: str = 'ec2'

    def __init__(self, *args, **kwargs) -> None:
        self.default_client: BaseClient = self._connect_to_client_by_region(*args, **kwargs)
        self._clients: List[BaseClient] = []
        self._described_instances: List[Dict] = []

    @property
    def default_region(self) -> str:
        return self.client_region(self.default_client)

    def client_region(self, client: BaseClient) -> str:
        return client.meta.region_name

    @property
    def clients(self) -> List[BaseClient]:
        return self._clients

    @property
    def described_instances(self) -> List[Dict]:
        return self._described_instances

    def _connect_to_client_by_region(self, region_name: Optional[str] = None, *args, **kwargs) -> Optional[BaseClient]:
        if kwargs.get("region_name") is None and region_name is not None:
            kwargs["region_name"] = region_name
        kwargs["service_name"] = self._service_name
        try:
            client = boto3.client(*args, **kwargs)
        except (ClientError, PartialCredentialsError) as e:
            logger.info(f"Connecting to client failed with client arguments {kwargs}: {type(e)}:{e}")

        else:
            return client
        return None

    def _try_describe_instances_by_region(self, new_client: BaseClient,
                                          region_name: str,
                                          paginate_val: str = 'describe_instances') -> Optional[Dict]:
        try:
            paginator = new_client.get_paginator(paginate_val).paginate()
            described_inst = paginator.build_full_result()
        except ClientError as e:
            logger.info(f"Connection failure to {region_name}. Error details: {type(e)}:{e}")
            print(f"Connection request to region {region_name}: FAILURE")
        else:
            print(f"Connection request to region {region_name}: SUCCESS")
            return described_inst
        return None

    def _try_describe_regions(self) -> Optional[Dict]:
        try:
            regions_data = self.default_client.describe_regions()
        except ClientError as e:
            logger.info(f"Failed to fetch regions data. Error details: {type(e)}:{e}")
        else:
            return regions_data
        return None

    def populate_clients_by_available_regions(self) -> List[BaseClient]:
        regions_data = self._try_describe_regions()
        if regions_data is None:
            return []
        for region in regions_data['Regions']:
            region_name = region['RegionName']
            if region_name == self.default_region:
                new_client = self.default_client
            else:
                new_client = self._connect_to_client_by_region(region_name=region_name)
            instance = self._try_describe_instances_by_region(new_client=new_client,
                                                              region_name=region['RegionName'])
            if instance is not None:
                self._clients.append(new_client)
                self._described_instances.append(instance)
        logger.info(
            f"Connection was established to regions {[self.client_region(client) for client in self._clients]}"
            f" for service {self._service_name}")
        return self._clients
