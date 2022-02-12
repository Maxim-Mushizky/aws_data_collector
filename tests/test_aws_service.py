from src.aws_service import Service
from src.data_handlers.data_containers import EC2Data
import pytest


@pytest.mark.parametrize('service_name', [
    # Would normally use a faker or string method to generate random str, but this to make a point
    'zxc',
    'cv',
    'asdad',
    'si2'
])
def test_none_existing_instances_not_created(service_name):
    with pytest.raises(NameError):
        Service(service_name)


@pytest.mark.ec2
def test_creation_of_ec2_object():
    ec2 = Service('ec2')
    try:
        ec2.populate_data()
    except Exception:
        pytest.fail(
            "A failure occurred during the populate stage, which means there's an issue with connected modules ")
    assert len(ec2.data) > 0, "Got an empty list, when expecting generated data"
    for data in ec2.data:
        assert isinstance(data, EC2Data), "The data doesn't belong to main container EC2Data class"
