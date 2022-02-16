# AWS data storage project

## How to use

### Give credentials
use AWS configure to enter access key ID and secret access key

### Use code
Go to data_readers.py and utilize the EC2DataReader.
To get the requested data, use the code:<br>

```python
from data_readers import EC2DataReader
ec2 = EC2DataReader() # Create a EC2 instance either empty or pass multiple token with the credentials keyword
ec2.populate_data() # populate the dataclasses with all available data
# data will now be stored in the ec2.data property 
print(ec2.data)
```  
