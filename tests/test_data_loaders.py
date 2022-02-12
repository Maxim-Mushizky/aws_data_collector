import pytest
from src.data_handlers.data_loaders import EC2DataLoader
import src.data_handlers.data_containers as dc


@pytest.mark.ec2
def test_creation_of_ec2_loader(ec2_data_loader):
    assert ec2_data_loader is not None, "ec2_data given to test is empty"
    assert isinstance(ec2_data_loader, EC2DataLoader), "Type returned should be a EC2DataLoader"
    assert isinstance(ec2_data_loader.described_instances, list), "The described instances are not in list format"
    assert len(ec2_data_loader.described_instances) > 0, "Empty list was given and no test can continue"


@pytest.mark.ec2
def test_populate_instances_container(ec2_data_loader_populated):
    print("hold")
    assert len(ec2_data_loader_populated.instances_data) > 1, "The list shouldn't be empty"
    for instance in ec2_data_loader_populated.instances_data:
        assert isinstance(instance, dc.EC2Data), f"The instance {instance} is not an object of EC2Data"
        assert isinstance(instance.ids, dc.Ids), f"The instance {instance} is not an object of Ids"
        assert isinstance(instance.times, dc.Times), f"The instance {instance} is not an object of Times"
        assert isinstance(instance.security_groups,
                          dc.SecurityGroups), f"The instance {instance} is not an object of SecurityGroups"
        assert isinstance(instance.specs, dc.Specs), f"The instance {instance} is not an object of Specs"
        assert isinstance(instance.platform_details,
                          dc.PlatformDetails), f"The instance {instance} is not an object of PlatformDetails"
