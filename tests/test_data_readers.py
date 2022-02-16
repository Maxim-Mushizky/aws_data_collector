import pytest
from src.data_readers import EC2DataReader
from src.data_handlers.data_containers import EC2Data


@pytest.mark.ec2
def test_reading_process():
    ec2 = EC2DataReader()
    try:
        ec2.populate_data()
    except Exception as e:
        pytest.fail(
            f"A failure occurred during the populate stage, which means there's an issue with connected modules. "
            f"Details: {type(e)}:{e}  ")
    assert len(ec2.data) > 0, "Got an empty list, when expecting generated data"
    for data in ec2.data:
        assert isinstance(data, EC2Data), "The data doesn't belong to main container EC2Data class"
