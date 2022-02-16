import src.data_handlers.data_containers as dc
from typing import (
    List,
    Dict,
    Generator,
    Optional
)


class EC2DataLoader:

    def __init__(self, described_instances: List[Dict], credentials: Optional[Dict[str, str]] = None) -> None:
        self.described_instances = described_instances
        self._instances_data: List[dc.EC2Data] = []
        if credentials is None:
            credentials = {}
        self.__token = credentials

    @property
    def instances_data(self) -> List:
        return self._instances_data

    def yield_data(self) -> Generator:
        for instance in self.instances_data:
            yield instance

    def populate_instances_containers(self) -> 'EC2DataLoader':
        for instance_response in self.described_instances:
            for reservation in instance_response['Reservations']:
                ec2_data = self._populate_data(reservation)
            self._instances_data.append(ec2_data)
        return self

    def _populate_data(self, reservation) -> dc.EC2Data:
        return dc.EC2Data(
            token=self._parse_token_keys(),
            ids=self._populate_ids(reservation),
            network_settings=self._populate_network_settings(reservation),
            times=self._populate_times(reservation),
            security_groups=self._populate_security_groups(reservation),
            specs=self._populate_specs(reservation),
            platform_details=self._populate_platform_details(reservation),
            placement=self._populate_placement(reservation)
        )

    def _populate_ids(self, reservation: Dict) -> dc.Ids:
        ids = dc.Ids()
        for inst in reservation['Instances']:
            ids = dc.Ids(
                image_id=inst.get('ImageId'),
                instance_id=inst.get('InstanceId')
            )

        return ids

    def _populate_specs(self, reservation: Dict) -> dc.Specs:
        specs = dc.Specs()
        for inst in reservation['Instances']:
            specs = dc.Specs(
                instance_type=inst.get('InstanceType'),
                cpu=inst.get('CpuOptions')
            )
        return specs

    def _populate_network_settings(self, reservation: Dict) -> dc.NetworkSettings:
        network_settings = dc.NetworkSettings()
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

    def _populate_times(self, reservation: Dict) -> dc.Times:
        times = dc.Times()
        for inst in reservation['Instances']:
            times = dc.Times(
                launch_time=inst.get('LaunchTime'),
                usage_operation_update_time=inst.get('UsageOperationUpdateTime')
            )

        return times

    def _populate_security_groups(self, reservation: Dict) -> dc.SecurityGroups:
        security_groups = dc.SecurityGroups()
        for inst in reservation['Instances']:
            for network in inst['NetworkInterfaces']:
                security_groups = dc.SecurityGroups(
                    groups=network.get('Groups', [])
                )
        return security_groups

    def _populate_platform_details(self, reservation: Dict) -> dc.PlatformDetails:
        platform_details = dc.PlatformDetails()
        for inst in reservation['Instances']:
            platform_details = dc.PlatformDetails(
                os=inst.get('PlatformDetails')
            )
        return platform_details

    def _populate_placement(self, reservation: Dict):
        placement = dc.Placement()
        for inst in reservation['Instances']:
            placement = dc.Placement(
                availability_zone=inst.get("Placement").get("AvailabilityZone")
            )
        return placement

    def _parse_token_keys(self):
        return dc.Token(
            access_key_id=self.__token.get("aws_access_key_id"),
            secret_access_key=self.__token.get("aws_secret_access_key")
        )
