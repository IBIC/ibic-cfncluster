#!/usr/bin/env python

# Do float division by default.
# from __future__ imports must be first
from __future__ import division, print_function


## IMPORT COMMANDS

import argparse
import boto3
import numpy as np
import sys
import math
import re

# import time functions
from datetime import datetime, date, time, timedelta

## SET UP FUNCTIONS

instances = ['m4.large', 'm4.xlarge', 'c4.xlarge', 'c4.8xlarge',
                 'm4.large','m4.xlarge','m4.2xlarge','m4.4xlarge',
                    'm4.10xlarge',
                 'c4.large', 'c4.xlarge','c4.2xlarge','c4.4xlarge',
                     'c4.8xlarge' ]

gpu_instances = ['g2.2xlarge', 'g2.8xlarge']

regions = ['us-east-1', 'us-west-2', 'us-west-1' , 'eu-west-1', 'eu-central-1',
           'ap-southeast-1', 'ap-northeast-1', 'ap-southeast-2',
           'ap-northeast-2', 'ap-south-1', 'sa-east-1']

# us-e1 N.Virginia; us-w2 Oregon; us-w1 N. California; eu-w1 Ireland;
# eu-c1 Frankfurt; ap-se1 Singapore; ap-ne1 tokyo, ap-se2 Sydney, ap-ne2 Seoul;
# ap-s1 Mumbai; sa-e1 Sao Paulo

header=["instance", "region", "total-$", "num-jobs", "exec-time", "$/hr",
    "#cores"]

five_days = timedelta(5)
now = datetime.now()
five_days_ago = now - five_days

ncpus = {}

with open("../lib/instance_concurrency") as f:
    # skip header line (for R)
    next(f)

    # read in data
    for line in f:
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
            #AvailabilityZone=region
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

    return(all_prices)


def make_a_cluster(row, num, length):
    """Make a cluster based on how many jobs there are"""

    cores = ncpus[row[0]]
    price = float(row[1])
    machines = int(math.ceil(num / cores))

    total_cost = machines * length * price

    return([row[0], row[2], total_cost, machines, length, price, cores])


def spaces(this_list, tnl=False):
    """Print the list spaces for each row.
    It isn't the prettiest, but it works for debug output"""

    list_s = [str(x) for x in this_list]

    print('\t'.join(list_s))

    if(tnl):
        print("")


def get_best_cluster(num, length, gpu, showall=False, text=False,
    showbest=True):
    """Compare all possible clusters to get the cheapest one."""

    every = get_all_regions(gpu=gpu)

    if showall and showbest:
        spaces(header)

    maxprice = sys.maxint
    minprice = 0
    for x in every:

        price = make_a_cluster(x, num, length)

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

## PARSE ARGUMENTS

parser = argparse.ArgumentParser(description="Determine the best value for a \
    given program based on execution time.")

# Putting the required flag arguments into their own group stops them from
## showing up under the confusing header "optional argumetnts"
required_named = parser.add_argument_group("required named arguments")

required_named.add_argument("-H", "--hours", type=int, required=True,
    help="Job execution time, on one brain in hours on a neuron-class " + \
    "machine (adrc, tpp, panuc), single-threaded. -H to not conflict with " + \
    "help.")
required_named.add_argument("-n", "--num", type=int, required=True,
    help="How many jobs you have.", default=1)

parser.add_argument("-s", "--show-all", action="store_true",
    help="Show info for all possible clusters.")
parser.add_argument("-S", "--show-all-only", action="store_true",
    help="Show info for all possibly clusters only (i.e. do not show best " + \
    "configuration")

parser.add_argument("-v", "--verbose", action="store_true",
    help="Be more verbose (turns on `show all\')")

parser.add_argument("-g", "--gpu", action="store_true",
    help="Don't calculate for GPU instances.")

parser.add_argument("-p", "--plaintext", action="store_true",
    help="Show results parsed into plain English.")

parser.add_argument("-t", "--total", action="store_true",
    help="Show the total cost for the cheapest configuration only.")

args = parser.parse_args()

if args.verbose:
    print(args)

# show all if -s or -S is set
if args.show_all or args.show_all_only or args.verbose:
    show_all = True
else:
    show_all = False

if args.total or args.show_all_only:
    show_best = False
else:
    show_best = True

## RUN CODE

get_best_cluster(args.num, args.hours,
    gpu = args.gpu,
    showall = show_all,
    text = args.plaintext,
    showbest = show_best)
