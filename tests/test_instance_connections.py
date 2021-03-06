from src.connection.instance_connectors import EC2ClientsGenerator
import pytest
from botocore.client import BaseClient
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError
)


@pytest.mark.ec2
@pytest.mark.parametrize('credentials', [
    {"aws_access_key_id": "ASDASD", "aws_secret_access_key": "ASDASDasd"},
    {"aws_access_key_id": None, "aws_secret_access_key": "ASDASDasd"},
    {"aws_access_key_id": "ASDASD", "aws_secret_access_key": None}
])
def test_connect_to_client_by_bad_credentials(ec2_client_generator, credentials):
    try:
        ec2_client_generator._connect_to_client_by_region(**credentials)
    except Exception as e:
        pytest.fail(f"Test failed and the exception was not caught. details {type(e)}:{e}")


@pytest.mark.ec2
def test_default_region_type(ec2_client_generator):
    region_name = ec2_client_generator.default_region
    assert isinstance(region_name, str), f"The default_region propety has to be str, instead it's a value {region_name}"


@pytest.mark.ec2
def test_connection_to_ec2_default(ec2_client_generator: EC2ClientsGenerator):
    client_connection = ec2_client_generator._connect_to_client_by_region()
    try:
        client_connection.describe_instances()
    except ClientError:
        pytest.fail("Fail to draw instance data")


@pytest.mark.ec2
@pytest.mark.parametrize('fake_region', [
    # Would normally use a faker or string method to generate random str, but this to make a point
    "zvc-east-1",
    "xc-east-2",
    "yy-east-4",
])
def test_connection_to_wrong_region_name(fake_region, ec2_client_generator: EC2ClientsGenerator):
    client_connection = ec2_client_generator._connect_to_client_by_region(region_name=fake_region)
    with pytest.raises(EndpointConnectionError):
        client_connection.describe_instances()


@pytest.mark.ec2
def test_populate_clients_by_available_regions(ec2_clients):
    client_instances = ec2_clients.copy()
    assert isinstance(client_instances, list), "No list item returned"
    assert client_instances != [], "The list is None, was unable to connect to any region"
    for instance in client_instances:
        assert isinstance(instance, BaseClient), f"Object {instance} isn't an instance of EC2"


@pytest.mark.ec2
def test_described_instances(ec2_described_instances):
    assert isinstance(ec2_described_instances, list), "No list item returned"
    assert ec2_described_instances != [], "The list is None, there was an error collecting the data"
    for instance in ec2_described_instances:
        assert isinstance(instance, dict), f"Object is not a dictionary"
