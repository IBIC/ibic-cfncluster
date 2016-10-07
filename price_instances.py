# Do float devision by default.
from __future__ import division, print_function

import boto3
import numpy as np
import sys
import math

from datetime import datetime, date, time, timedelta


instances = ['m4.large', 'm4.xlarge', 'c4.xlarge', 'c4.8xlarge'
             #            'm3.medium','m3.large','m3.xlarge','m3.2xlarge',
             #            'm4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge',
             #            'r3.large','r3.xlarge','r3.2xlarge','r3.4xlarge','r3.8xlarge',
             #            'x1.4xlarge','x1.8xlarge','x1.16xlarge','x1.32xlarge',
             #            'i2.xlarge','i2.2xlarge','i2.4xlarge','i2.8xlarge',
             #            'c3.large','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge',
             #            'c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge',
             #            'cc1.4xlarge',
             #            'g2.2xlarge','g2.8xlarge',
             #            'd2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge']
             ]

gpu_instances = ['g2.2xlarge', 'g2.8xlarge']

regions = ['us-east-1', 'us-west-2', 'us-west-1' , 'eu-west-1'] #, 'eu-central-1',
           #'ap-southeast-1', 'ap-northeast-1', 'ap-southeast-2',
           #'ap-northeast-2', 'ap-south-1', 'sa-east-1']

# us-e1 N.Virginia; us-w2 Oregon; us-w1 N. California; eu-w1 Ireland;
# eu-c1 Frankfurt; ap-se1 Singapore; ap-ne1 tokyo, ap-se2 Sydney, ap-ne2 Seoul;
# ap-s1 Mumbai; sa-e1 Sao Paulo

# Create five days ago datetime object.
five_days = timedelta(5)
now = datetime.now()
five_days_ago = now - five_days

# Experimentally determined speed up times.
gpu_speed_up = {"bedpostx": 161, "probtrackx": 14.9}

# Numer of cpus per instance
ncpus = {"t1.micro": 1, "t2.micro": 1, "t2.small": 1, "t2.medium": 2,
         "t2.large": 2, "m1.small": 1, "m1.medium": 1, "m1.large": 2, 
         "m1.xlarge": 4,"m2.xlarge": 2, "m2.2xlarge": 4, "m2.4xlarge": 8, 
         "m3.medium": 1,"m3.large": 1, "m3.xlarge": 2, "m3.2xlarge": 4, 
         "m4.large": 1, "m4.xlarge": 2, "m4.2xlarge": 4, "m4.4xlarge": 8, 
         "m4.10xlarge": 20, "c1.medium": 2, "c1.xlarge": 8, "cc2.8xlarge": 16, 
         "cg1.4xlarge": 8, "cr1.8xlarge": 16, "c3.large": 1, "c3.xlarge": 2, 
         "c3.2xlarge": 4, "c3.4xlarge": 8, "c3.8xlarge": 16, "c4.large": 1, 
         "c4.xlarge": 2, "c4.2xlarge": 4, "c4.4xlarge": 8, "c4.8xlarge": 18, 
         "hi1.4xlarge": 8, "hs1.8xlarge": 8, "g2.2xlarge": 4, "x1.32xlarge": 64,
         "r3.large": 1, "r3.xlarge": 2, "r3.2xlarge": 4, "r3.4xlarge": 8, 
         "r3.8xlarge": 16, "i2.xlarge": 2, "i2.2xlarge": 4, "i2.4xlarge": 8, 
         "i2.8xlarge": 16, "d2.xlarge": 2, "d2.2xlarge": 4, "d2.4xlarge": 8, 
         "d2.8xlarge": 18,
         'g2.2xlarge': 1, 'g2.8xlarge': 4  
         # Not actual cpus, but gpu concurrency = 4
         }

def get_all_in_region(region):
    client = boto3.client("ec2", region)
    response = client.describe_spot_price_history(
            InstanceTypes=instances,
            StartTime=five_days_ago,
            EndTime=now,
            ProductDescriptions=['Linux/UNIX'],
        )

    prices = np.empty([0, 3])

    for item in response["SpotPriceHistory"]:
        mat = np.array([[item["InstanceType"], item["SpotPrice"], 
            item["AvailabilityZone"]]])
        prices = np.append(prices, mat, axis=0)

    return(prices)

def get_all_regions():
    all_prices = np.empty([0, 3])
    
    for r in regions:
        mat = get_all_in_region(r)
        all_prices = np.append(all_prices, mat, axis=0)

    return(all_prices)


# def price_instance(instancename, region):
#     """Return the mean price for an instance in a region over the last
#     five days"""



#     client = boto3.client("ec2", region)
#     response = client.describe_spot_price_history(
#         InstanceTypes=[instancename],
#         StartTime=five_days_ago,
#         EndTime=now,
#         ProductDescriptions=['Linux/UNIX'],
#     )
#     prices = [float(x['SpotPrice']) for x in response['SpotPriceHistory']]

#     if (len(prices) > 0):
#         price = np.mean(prices)
#     else:
#         price = sys.maxint

#     return([instancename, region, price])

def make_a_cluster(row, num, length):

    cores = ncpus[row[0]]
    machines = math.ceil(num / cores)
    price = row[1]

    print(row)
    total_cost = machines * length * price

    return([row[0], row[2], price])

def best_price(program, length, num, quick, cheapest, gpu=False):
    """Find the best instance by comparing against previous best."""

    print("AWS speed up for " + program + " is " + str(gpu_speed_up[program]) +
          "x.")

    # For comparison, so the first one is always smaller.
    max_price = sys.maxint
    max_time = sys.maxint

    if gpu:
        search_instances = instances + gpu_instances
    else:
        search_instances = instances

    print("Pricing " + str(len(search_instances)) + " instances against " +
          str(len(regions)) + " regions ...")

    for r in regions:
        for i in search_instances:
            if i in gpu_instances:
                exec_time = length / gpu_speed_up[program]
            else:
                exec_time = length 

            cluster = make_a_cluster(price_instance(i, r), num, exec_time)

            if cluster[4] < max_price:
                max_price = cluster[4]
                best_price = cluster

            if cluster[5] < max_time:
                max_time = cluster[5]
                best_time = cluster

    print("Format: machine, region, $/instance/hr, #instances, total$, " + 
        "time(hr)")


    # Return appropriate things here

every = get_all_regions()

[ make_a_cluster(x, 10, 100) for x in every ]

