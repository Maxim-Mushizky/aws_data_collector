# AWS data storage project

## How to use

### Give credentials
use AWS configure to enter access key ID and secret access key

### Use code
Go to aws_service.py and select the EC2 service.
To get the requested data, use the code:<br>

```python
from aws_service import Service
# Create a EC2 instance
ec2 = Service('ec2') 
ec2.populate_data()
# data will now be stored in the ec2.data property 
print(ec2.data)
```  
