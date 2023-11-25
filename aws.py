import boto3
from botocore.exceptions import ClientError, DataNotFoundError

ec2 = boto3.client('ec2')
#response = ec2.describe_instances()
#print(response)

def create_ec2_instance(ami_id="", instance_type="", key_name="", security_group_ids=[], subnet_id="", instance_name="", dry_run=True):
    ec2 = boto3.resource('ec2')
    try:
        instance = ec2.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=security_group_ids,
            SubnetId=subnet_id,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ], 
            DryRun=dry_run
        )[0]
    except ClientError as e:
        if e.response['Error'].get('Code') == 'DryRunOperation':
            print("Dry run succeeded")
        else:
            print(f"Dry run failed, Reason: {e}")
            

def create_subnet(vpc_id, cidr_block, availability_zone, subnet_name, dry_run=True):
    ec2 = boto3.resource('ec2')
    try:
        response = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block,
            AvailabilityZone=availability_zone,
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': subnet_name
                        }
                    ]
                }
            ], 
            DryRun=dry_run
        )
        print(response.id)
        return response.id
    except ClientError as e:
        if e.response['Error'].get('Code') == 'DryRunOperation':
            print("Dry run succeeded")
            print(e.response)
            return vpc_id
        else:
            print(f"Dry run failed, Reason: {e}")
          
            
def create_vpc(vpc_name, cidr_block, dry_run=True):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_vpc(
            CidrBlock=cidr_block, 
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': vpc_name
                        }
                    ]
                }
            ],
            DryRun=dry_run)
        print(response['Vpc']['VpcId'])
        
    except ClientError as e:
        if e.response['Error'].get('Code') == 'DryRunOperation':
            print("Dry run succeeded")
            print(e.response)
            return vpc_name
        else:
            print(f"Dry run failed, Reason: {e}")
    