# Terrafirma
This is essentially my take on IaC using YAML as the primary template.

Terrafirma is no where near production (nor dev really) ready. It can barely create resources at the moment with little ways of checking besides hard coded dry runs.

A basic example is like this:
```yaml
DEV: # Environment
  Variables:            # Will eventually allow environment wide variables here
    Provider: aws       # the cloud provider, as of this moment it's only AWS

  # VPC resource
  Vpc1:                 
    ResourceType: Vpc
    VpcName: test
    Cidr: 10.0.0.0/16

  # Subnet Resource
  Subnet1:
    ResourceType: Subnet
    VpcName: test
    Cidr: 10.0.0.0/24
    AZ: us-east-1a

  # EC2 Instance Resources
  TEST1:  #internal resource name
    ResourceType: Instance
    InstanceName: testing
    InstanceType: t2.micro
    ImageId: ami-058bd2d568351da34
    KeyName: dev
    SubnetId: Subnet1
    MinCount: 1
    MaxCount: 1

  TEST2:  #internal resource name
    ResourceType: Instance
    InstanceName: testing2
    InstanceType: t2.micro
    ImageId: ami-058bd2d568351da34
    KeyName: dev
    SubnetId: Subnet1
    MinCount: 1
    MaxCount: 1
```

If you haven't already, AWS Credentials will need to be stored in `~/.aws/config`. Then we'd run it with `python terrafirma.py tf.yaml`.



# Currently Terrafirma is under heavy development. There's currently little to no resource checking right now and little to no error feedback besides raw Python crash dumps and/or API responses. Please use this wisely right now.

