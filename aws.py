import boto3
from botocore.exceptions import ClientError, DataNotFoundError
import re

ec2 = boto3.client('ec2')
#response = ec2.describe_instances()
#print(response)

def create_ec2_instance(ami_id="", instance_type="", key_name="", security_group_ids=[], subnet_id="", instance_name="", public_ip=False, dry_run=True):
    ec2 = boto3.resource('ec2')
    try:
        instance = ec2.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=security_group_ids,
            #SubnetId=subnet_id,
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
            DryRun=dry_run,
            NetworkInterfaces=[
                {
                    'DeviceIndex': 0,
                    'SubnetId': subnet_id,
                    'Groups': security_group_ids,
                    'AssociatePublicIpAddress': public_ip
                }
            ]
        )[0]
    except ClientError as e:
        if e.response['Error'].get('Code') == 'DryRunOperation':
            print("\t\t\tDry run succeeded")
        else:
            if re.search("does not exist", e.response['Error'].get('Message')):
                print(f"\n\t\t\tDry run may or may not have succeeded due to not being able to get API Id's. \n\t\t\tPlease check output to make sure everything is good.")
            else:
                print(f"\t\t\tDry run failed, Reason: {e}")
            

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
            print("\t\t\tDry run succeeded")
            #print(e.response)
            return vpc_id
        else:
            if re.search("does not exist",e.response['Error'].get('Message')):
                print(f"\n\t\t\tDry run may or may not have succeeded due to not being able to get API Id's. \n\t\t\tPlease check output to make sure everything is good.")
                return vpc_id
            else:
                print(f"\t\t\tDry run failed, Reason: {e}")
                return vpc_id
          
            
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
        return response['Vpc']['VpcId']
        
    except ClientError as e:
        if e.response['Error'].get('Code') == 'DryRunOperation':
            print("\t\t\tDry run succeeded")
            #print(e.response)
            return vpc_name
        else:
            if re.search("does not exist", e.response['Error'].get('Message')):
                print(f"\n\t\t\tDry run may or may not have succeeded due to not being able to get API Id's. \n\t\t\tPlease check output to make sure everything is good.")
                return vpc_name
            else:
                print(f"\t\t\tDry run failed, Reason: {e}")
                return vpc_name
            
def terminate_instance(key_name):
    ec2 = boto3.resource('ec2')

    # Find instances with the specified key name
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [key_name]}])

    # Terminate each instance
    for instance in instances:
        print(instance)
        instance.terminate()
        print(f"Terminating instance with ID: {instance.id}")
    