import src.data_handlers.data_containers as dc
from typing import (
    List,
    Dict,
    Generator
)
import abc


class DataLoader:

    @property
    @abc.abstractmethod
    def instances_data(self) -> List:
        raise NotImplementedError

    @abc.abstractmethod
    def populate_instances_containers(self) -> 'DataLoader':
        raise NotImplementedError

    @abc.abstractmethod
    def _populate_ids(self, instance_response: Dict) -> dc.Ids:
        raise NotImplementedError


class EC2DataLoader(DataLoader):

    def __init__(self, described_instances: List[Dict]) -> None:
        # self.__client_generator: EC2ClientGenerator = ec2_client_generator
        # self.__client_generator.populate_clients_by_available_regions()
        self.described_instances = described_instances
        self._instances_data: List[dc.EC2Data] = []

    @property
    def instances_data(self) -> List:
        return self._instances_data

    def yield_data(self) -> Generator:
        for instance in self.instances_data:
            yield instance

    def populate_instances_containers(self) -> 'EC2DataLoader':
        for instance_response in self.described_instances:
            ec2_data = self._populate_data(instance_response)
            self._instances_data.append(ec2_data)
        return self

    def _populate_data(self, instance_response) -> dc.EC2Data:
        return dc.EC2Data(
            ids=self._populate_ids(instance_response),
            network_settings=self._populate_network_settings(instance_response),
            times=self._populate_times(instance_response),
            security_groups=self._populate_security_groups(instance_response),
            specs=self._populate_specs(instance_response),
            platform_details=self._populate_platform_details(instance_response)
        )

    def _populate_ids(self, instance_response: Dict) -> dc.Ids:
        ids = dc.Ids()
        for reservation in instance_response['Reservations']:
            for inst in reservation['Instances']:
                ids = dc.Ids(
                    image_id=inst.get('ImageId'),
                    instance_id=inst.get('InstanceId')
                )

        return ids

    def _populate_specs(self, instance_response: Dict) -> dc.Specs:
        specs = dc.Specs()
        for reservation in instance_response['Reservations']:
            for inst in reservation['Instances']:
                specs = dc.Specs(
                    instance_type=inst.get('InstanceType'),
                    cpu=inst.get('CpuOptions')
                )
        return specs

    def _populate_network_settings(self, instance_response: Dict) -> dc.NetworkSettings:
        network_settings = dc.NetworkSettings()
        for reservation in instance_response['Reservations']:
            for inst in reservation['Instances']:
                for network in inst['NetworkInterfaces']:
                    network_settings = dc.NetworkSettings(
                        ip6_address=network.get('Ipv6Addresses'),
                        subnet_id=network.get('SubnetId'),
                        interface_type=network.get('InterfaceType'),
                        status=network.get('Status'),
                        private_dns_name=network.get("PrivateIpAddresses", [{}])[0].get("PrivateDnsName"),
                        private_ip_address=network.get("PrivateIpAddresses", [{}])[0].get("PrivateIpAddress")
                    )

        return network_settings

    def _populate_times(self, instance_response: Dict) -> dc.Times:
        times = dc.Times()
        for reservation in instance_response['Reservations']:
            for inst in reservation['Instances']:
                times = dc.Times(
                    launch_time=inst.get('LaunchTime'),
                    usage_operation_update_time=inst.get('UsageOperationUpdateTime')
                )

        return times

    def _populate_security_groups(self, instance_response: Dict) -> dc.SecurityGroups:
        security_groups = dc.SecurityGroups()
        for reservation in instance_response['Reservations']:
            for inst in reservation['Instances']:
                for network in inst['NetworkInterfaces']:
                    security_groups = dc.SecurityGroups(
                        groups=network.get('Groups', [])
                    )
        return security_groups

    def _populate_platform_details(self, instance_response: Dict) -> dc.PlatformDetails:
        platform_details = dc.PlatformDetails()
        for reservation in instance_response['Reservations']:
            for inst in reservation['Instances']:
                platform_details = dc.PlatformDetails(
                    os=inst.get('PlatformDetails')
                )
        return platform_details
