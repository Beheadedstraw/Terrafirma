#!/usr/bin/python

import oyaml as yaml
from aws import *
import json

DRYRUN=False
#with open(sys.argv[1], "r") as file:
'''
Terrafirma yaml files are formatted like so:

Environment:
    Variables:
        foo1: bar
        foo2: bar
        
    internal_resource_id:
        ResourceType: blah
        attr: blah
        
Internal resource id's are not utilized as the actual resource name for more programmatic purposes.
'''

with open("tf.yaml", "r") as file:
    y = yaml.safe_load(file)
RESOURCES = {}
for env in y:
    print(f"Environment: {env}")
    for resources in y.items():
        attributes = resources[1].items()   #Pull the environment dicts
        for a in resources:                 #Start going through the resources
            if a[0] == "Variables":
                pass
            else:
                if a[1]['ResourceType'] == "Vpc":
                    print(f"""
                    ResourceInternalName: {a[0]}
                        ResourceType: {a[1]['ResourceType']}
                            VpcName: {a[1]['VpcName']}
                            Cidr: {a[1]['Cidr']}
                    """)
                    vpc_id = create_vpc(a[1]['VpcName'], a[1]['Cidr'],dry_run=DRYRUN)
                    RESOURCES["vpc"] = {a[1]['VpcName']: vpc_id}
                    print(f"{RESOURCES}")
                    
                elif a[1]['ResourceType'] == "Subnet":
                    print(f"""
                    ResourceInternalName: {a[0]}
                        ResourceType: {a[1]['ResourceType']}
                            VpcId: {RESOURCES["vpc"][a[1]['VpcName']]}
                            Cidr: {a[1]['Cidr']}
                            AZ: {a[1]['AZ']}
                    """)
                    RESOURCES['subnet'] = {a[0]:create_subnet(RESOURCES["vpc"][a[1]['VpcName']], a[1]['Cidr'], a[1]['AZ'], a[0], dry_run=DRYRUN)}
                    print(RESOURCES)
                elif a[1]['ResourceType'] == "Instance":
                    if "SecGroupIds" not in a[1]:
                        SecGroupIds = []
                    print(f"""
                        ResourceInternalName: {a[0]}
                            ResourceType: {a[1]['ResourceType']}
                                InstanceName: {a[1]['InstanceName']}
                                InstanceType: {a[1]['InstanceType']}
                                ImageId: {a[1]['ImageId']}
                                KeyName: {a[1]['KeyName']}
                                SecGroupIds: {SecGroupIds}
                                SubnetId: {a[1]['SubnetId']}
                                MinCount: {a[1]['MinCount']}
                                MaxCount: {a[1]['MaxCount']}
                        """)
                    create_ec2_instance(a[1]['ImageId'], a[1]['InstanceType'], a[1]['KeyName'], SecGroupIds, RESOURCES['subnet'][a[1]['SubnetId']], a[1]['InstanceName'], dry_run=DRYRUN)

#if y['START']:
#    START(y)


 