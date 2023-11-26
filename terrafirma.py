#!/usr/bin/python

import oyaml as yaml
from aws import *
import json
import sys
import copy

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
#with open("tf.yaml", "r") as file:
with open(sys.argv[1], "r") as file:
    y = yaml.safe_load(file)


def process_variables(a):
    b = copy.deepcopy(a)
    for i, v in b[1].items():
        #print(f"\n\nResource items in for loop for variable conversion: {i}")
        if str(v)[0] == '$':
            # We strip the dollar sign and split the variable by ENV.VARIABLES.ITEM.
            #                                                    y[var[1]].y[var[2]].y[var[3]]
            var = v[1:].split('.') 
            a[1][i] = y[var[0]][var[1]][var[2]]
            #print(f"Value of variable {i} is {a[1][i]}")


def create_aws(y):
    for env in y:
        try:
            print(f"Environment: {env}")
            RESOURCES["vpc"] = {}
            RESOURCES["subnet"] = {}
            for resources in y.items():
                attributes = resources[1].items()   #Pull the environment dicts
                for a in attributes:                 #Start going through the resources
                    if a[0] == "Variables":
                        pass
                    else:
                        #print(a[1])
                        if a[1]['ResourceType'] == "Vpc":
                            #replace variables with actual values in the dictionary
                            process_variables(a)
                            
                            print(f"""
                            ResourceInternalName: {a[0]}
                                ResourceType: {a[1]['ResourceType']}
                                    VpcName: {a[1]['VpcName']}
                                    Cidr: {a[1]['Cidr']}
                            """)
                            vpc_id = create_vpc(a[1]['VpcName'], a[1]['Cidr'],dry_run=DRYRUN)
                            RESOURCES["vpc"] = {a[1]['VpcName']: vpc_id}
                            print(f"RESOURCES ARE NOW: {RESOURCES}")
                            print("-"*100)
                            
                        elif a[1]['ResourceType'] == "Subnet":
                            #replace variables with actual values in the dictionary
                            process_variables(a)
                            
                            print(f"""
                            ResourceInternalName: {a[0]}
                                ResourceType: {a[1]['ResourceType']}
                                    VpcId: {RESOURCES["vpc"][a[1]['VpcName']]}
                                    Cidr: {a[1]['Cidr']}
                                    AZ: {a[1]['AZ']}
                            """)
                            RESOURCES['subnet'] = {a[0]:create_subnet(RESOURCES["vpc"][a[1]['VpcName']], a[1]['Cidr'], a[1]['AZ'], a[0], dry_run=DRYRUN)}
                            #print(RESOURCES)
                            print("-"*100)
                            
                        elif a[1]['ResourceType'] == "Instance":
                            #replace variables with actual values in the dictionary
                            process_variables(a)
                                    
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
                            create_ec2_instance(a[1]['ImageId'], a[1]['InstanceType'], a[1]['KeyName'], SecGroupIds, RESOURCES['subnet'][a[1]['SubnetId']], a[1]['InstanceName'], a[1]['PublicIp'], dry_run=DRYRUN)
                            print("-"*100)
        except Exception as e:
            print(e)
            
def destroy_aws(y):
    for env in y:
        try:
            print(f"Environment: {env}")
            for resources in y.items():
                attributes = resources[1].items()   #Pull the environment dicts
                for a in attributes:                 #Start going through the resources
                    if a[0] == "Variables":
                        pass
                    else:
                        #print(a[1])
                        if a[1]['ResourceType'] == "Instance":
                            terminate_instance(a[1]['InstanceName'])
        except Exception as e:
            print(e)
            

#set it to true just in case this borks for now.         
DRYRUN=True 
RESOURCES = {}

#check if were setting nodry, which means this will deploy to a live env                            
if sys.argv.__len__() > 2:      
    if sys.argv[2] == "create":
        if sys.argv[3] == "nodry":
            DRYRUN=False
            print("!"*100)
            print("!!!!!!!!!!!!!!----       nodry is set - Deploying to live environment!           ----!!!!!!!!!!!!!!!")
            print("!"*100)
            create_aws(y)
        else:
            DRYRUN=True
            print("#"*100)
            print("############----                 nodry is NOT set - Doing a dry run.               ----#############")
            print("############----         API ID's will be replaced with the resource name          ----#############")
            print("#"*100)
            create_aws(y)
        
    elif sys.argv[2] == "destroy":
        confirm = input("""
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                !!!!!!     THERE IS NO DRYRUN FOR DESTROYING AWS CLUSTERS.  !!!!!!
                !!!!!!     THIS WILL ENTIRELY REMOVE THE DEFINED RESOURCES. !!!!!!
                !!!!!!     ARE YOU SURE YOU WANT TO CONTINUE?               !!!!!!
                !!!!!!     (enter 'YES_DESTROY_IT' to continue)             !!!!!!
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nConfirm:""")
        if confirm == "YES_DESTROY_IT":
            DRYRUN=False
            print("#"*100)
            print("############----                 nodry is NOT set - Doing a dry run.               ----#############")
            print("############----         API ID's will be replaced with the resource name          ----#############")
            print("#"*100)
            destroy_aws(y)
        else:
            print("Exiting...")
            sys.exit()


    
print(f"\n\nAPI RESOURCES DEFINED: {RESOURCES}")
                    
                    


#if y['START']:
#    START(y)


 