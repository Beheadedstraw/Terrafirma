# Terrafirma
This is essentially my take on IaC using YAML as the primary template.

Terrafirma is no where near production (nor dev really) ready. It can barely create/destroy resources at the moment with no state management (yet!). 

A basic example named `tf.yaml`:
```yaml
DEV: # Environment
  Variables:            # Will eventually allow environment wide variables here
    Provider: aws       # the cloud provider, as of this moment it's only AWS
    ImageId: ami-058bd2d568351da34

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
    ImageId: $DEV.Variables.ImageId
    KeyName: dev
    SubnetId: Subnet1
    MinCount: 1
    MaxCount: 1

  TEST2:  #internal resource name
    ResourceType: Instance
    InstanceName: testing2
    InstanceType: t2.micro
    ImageId: $DEV.Variables.ImageId
    KeyName: dev
    SubnetId: Subnet1
    MinCount: 1
    MaxCount: 1
```

If you haven't already, AWS Credentials will need to be stored in `~/.aws/config`. Then we'd run it with `python terrafirma.py tf.yaml create`. By default it will always run a dryrun (aka basic testing while not modifying the live environment) and will require `nodry` on the end of the command to push to said live environment.



# Currently Terrafirma is under heavy development. There's currently little to no resource checking right now and little to no error feedback besides raw Python crash dumps and/or API responses. Please use this wisely right now.

