# Do float devision by default.
from __future__ import division, print_function

import boto3
import numpy as np
import sys
import math
import re

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

# header for printing results
header=["instance", "region", "total-$", "num", "exec-time", "$/hr", "#cores"]

# Create five days ago datetime object.
five_days = timedelta(5)
now = datetime.now()
five_days_ago = now - five_days

# Experimentally determined speed up times.
gpu_speed_up = {"bedpostx": 161, "probtrackx": 14.9}

# Get the number of cpus per instance from a text file
ncpus = {}

with open("instance_concurrency") as f:
    for line in f:
       # print(line)
       (key, val) = line.split(None)
       ncpus[key] = int(val)

def get_all_in_region(region, gpu, program):
    if gpu:
        all_instances = instances + gpu_instances
    else:
        all_instances = instances

    client = boto3.client("ec2", region)
    response = client.describe_spot_price_history(
            InstanceTypes=all_instances,
            StartTime=five_days_ago,
            EndTime=now,
            ProductDescriptions=['Linux/UNIX'],
        )

    prices = np.empty([0, 3])

    for item in response["SpotPriceHistory"]:
        price = float(item["SpotPrice"])

        mat = np.array([[item["InstanceType"], price, 
            item["AvailabilityZone"]]])
        prices = np.append(prices, mat, axis=0)

    return(prices)

def get_all_regions(gpu, program):
    all_prices = np.empty([0, 3])
    
    for r in regions:
        mat = get_all_in_region(r, gpu, program)
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

def make_a_cluster(row, num, length, program):

    cores = ncpus[row[0]]
    price = float(row[1])
    machines = int(math.ceil(num / cores))


    if re.match("^g", row[0]):
        length /= gpu_speed_up[program]
        # print("GPU speed up is " + str(gpu_speed_up[program]))

    total_cost = machines * length * price

    return([row[0], row[2], total_cost, machines, length, price, cores])

# def best_price(program, length, num, quickest, cheapest, gpu=False):
#     """Find the best instance by comparing against previous best."""

#     print("AWS speed up for " + program + " is " + str(gpu_speed_up[program]) +
#           "x.")

#     # For comparison, so the first one is always smaller.
#     max_price = sys.maxint
#     max_time = sys.maxint

#     if gpu:
#         search_instances = instances + gpu_instances
#     else:
#         search_instances = instances

#     print("Pricing " + str(len(search_instances)) + " instances against " +
#           str(len(regions)) + " regions ...")

#     for r in regions:
#         for i in search_instances:
#             if i in gpu_instances:
#                 exec_time = length / gpu_speed_up[program]
#             else:
#                 exec_time = length 

#             cluster = make_a_cluster(price_instance(i, r), num, exec_time)

#             if cluster[4] < max_price:
#                 max_price = cluster[4]
#                 best_price = cluster

#             if cluster[5] < max_time:
#                 max_time = cluster[5]
#                 best_time = cluster

#     print("Format: machine, region, $/instance/hr, #instances, total$, " + 
#         "time(hr)")


    # Return appropriate things here

def spaces(this_list, tnl=False):
    '''Print the list spaces for each row.
    It isn't the prettiest, but it works for debug output'''
    width = 80 // len(this_list) 
    fmt = "{:<" + str(width) + "}"

    print(''.join([fmt.format(x) for x in this_list]))

    if(tnl):
        print("")

def get_best_cluster(num, length, gpu, program, showall=False, text=False,
    showbest=True):
    every = get_all_regions(gpu=gpu, program=program)

    if showall and showbest:
        spaces(header)

    maxprice = sys.maxint
    for x in every:
        price = make_a_cluster(x, num, length, program)

        if showall:
            spaces(price)

        if price[2] < maxprice:
            best = price
            maxprice = price[2]

    if showall and showbest:
        spaces(header, tnl=True)

    fmt = '{:<12}{:<20}'

    if showbest:
        for h,b in zip(header, best):
            print(fmt.format(str(h), str(b)))

    if text:
        print("You can run " + str(num) + \
            " jobs, taking " + str(round(best[6], 4)) + \
            " hours each on " + str(best[4]) + " " + best[0] + \
            "-class instances in the " + best[1] + " region. " + \
            " It will cost you $" + str(round(best[2], 5)) + ".")