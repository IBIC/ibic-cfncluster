# Do float devision by default.
from __future__ import division, print_function

import boto3
import numpy as np
import sys
import math
import re
import itertools

from datetime import datetime, date, time, timedelta


instances = ['m4.large', 'm4.xlarge', 'c4.xlarge', 'c4.8xlarge',
                 'm4.large','m4.xlarge','m4.2xlarge','m4.4xlarge',
                    'm4.10xlarge',
                 'c4.large', 'c4.xlarge','c4.2xlarge','c4.4xlarge',
                     'c4.8xlarge' ]

gpu_instances = ['g2.2xlarge', 'g2.8xlarge']

regions = ['us-east-1']
# ['us-east-1', 'us-west-2', 'us-west-1' , 'eu-west-1'] #, 'eu-central-1',
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

# Get the number of cpus per instance from a text file
ncpus = {}

with open("instance_concurrency") as f:
    for line in f:
       # print(line)
       (key, val) = line.split(None)
       ncpus[key] = int(val)

def get_all_in_region(region, gpu):
    """Get the price of every instance in a single region."""

    if gpu:
        all_instances = gpu_instances
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

def get_all_regions(gpu):
    """Iterate over all given regions."""

    all_prices = np.empty([0, 3])

    for r in regions:
        mat = get_all_in_region(r, gpu)
        all_prices = np.append(all_prices, mat, axis=0)

    # print(*all_prices, sep='\n')
    return(all_prices)


def make_a_cluster(row, price, num, length):
    """Make a cluster based on how many jobs there are"""

    cores = ncpus[row[0]]
    machines = int(math.ceil(num / cores))

    # if re.match("^g", row[0]):
    #     length /= gpu_speed_up[program]
        # print("GPU speed up is " + str(gpu_speed_up[program]))

    if price is not None:
        total_cost = machines * length * float(price)
    else:
        total_cost = None

    return([row[0], row[2], total_cost, machines, length, price, cores])


def spaces(this_list, tnl=False):
    """Print the list spaces for each row.
    It isn't the prettiest, but it works for debug output"""

    list_s = [str(x) for x in this_list]

    # total price
    list_s[2] = format(float(list_s[2]), '.3f')
    # $/hr
    list_s[5] = format(float(list_s[5]), '.6f')

    print('\t'.join(list_s))

    if(tnl):
        print("")

def accumulate(array):
    """Get the average price of instances x AZs"""

    instances = list(set(array[:,0]))
    azones = list(set(array[:,2]))

    permute = np.array(list(itertools.product(*[instances, azones])))

    results = np.zeros([0, 3])

    for row in permute:
        subset = array[(array[:,0] == row[0]) & (array[:,2] == row[1])]
        vals_f = [float(x) for x in subset[:,1]]

        if len(vals_f) > 0:
            mean = sum(vals_f) / len(vals_f)
        else:
            mean = None

        results = np.append(results, [[row[0], mean, row[1]]], axis=0)

    return(results)

def get_best_cluster(num, length, gpu, showall=False, text=False,
    showbest=True, total=False):
    """Compare all possible clusters to get the cheapest one."""

    every = np.array(get_all_regions(gpu=gpu))

    iXaz = accumulate(every)

    if showall and showbest:
        spaces(header)

    maxprice = sys.maxint
    minprice = 0

    best = None

    for x in iXaz:
        mean_cost = x[1]

        if mean_cost is not None:
            price = make_a_cluster(x, mean_cost, num, length)

            if showall:
                spaces(price)

            if price[2] < maxprice:
                best = price
                maxprice = price[2]

    if showall and showbest:
        spaces(header, tnl=True)

    fmt = '{:<13}{:<20}'

    if showbest:
        for h,b in zip(header, best):
            print(fmt.format(str(h), str(b)))

    if text:
        print("You can run " + str(num) + \
            " jobs, taking " + str(round(best[6], 4)) + \
            " hours each on " + str(best[4]) + " " + best[0] + \
            "-class instances in the " + best[1] + " region. " + \
            " It will cost you $" + str(round(best[2], 5)) + ".")

    if total:
        print(best[2])
