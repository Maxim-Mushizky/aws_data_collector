import pytest
from src.connection.instance_connectors import EC2ClientsGenerator
from src.data_handlers.data_loaders import EC2DataLoader


@pytest.fixture(scope='module', autouse=True)
def ec2_client_generator():
    return EC2ClientsGenerator()


@pytest.fixture(scope='module')
def ec2_populate(ec2_client_generator):
    ec2_client_generator.populate_clients_by_available_regions()
    return ec2_client_generator


@pytest.fixture(scope='module')
def ec2_clients(ec2_populate):
    return ec2_populate.clients


@pytest.fixture(scope='module')
def ec2_described_instances(ec2_populate):
    return ec2_populate.described_instances


@pytest.fixture(scope='module')
def ec2_data_loader(ec2_described_instances):
    return EC2DataLoader(described_instances=ec2_described_instances)


@pytest.fixture(scope='module')
def ec2_data_loader_populated(ec2_data_loader):
    return ec2_data_loader.populate_instances_containers()
