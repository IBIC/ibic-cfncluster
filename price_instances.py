import boto3
from datetime import datetime, date, time, timedelta
import numpy as np
import sys

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

regions = ['us-east-1', 'us-west-2', 'us-west-1', 'eu-west-1', 'eu-central-1',
           'ap-southeast-1', 'ap-northeast-1', 'ap-southeast-2', 
           'ap-northeast-2', 'ap-south-1', 'sa-east-1']

# us-e1 N.Virginia; us-w2 Oregon; us-w1 N. California; eu-w1 Ireland; 
# eu-c1 Frankfurt; ap-se1 Singapore; ap-ne1 tokyo, ap-se2 Sydney, ap-ne2 Seoul;
# ap-s1 Mumbai; sa-e1 Sao Paulo

# Create five days ago datetime object.
five_days = timedelta(5)
now = datetime.now()
five_days_ago = now - five_days

def price_instance(instancename, region):
    """Return the mean price for an instance in a region over the last
    five days"""
    
    client = boto3.client("ec2", region)
    response = client.describe_spot_price_history(
        InstanceTypes =[instancename],
        StartTime=five_days_ago,
        EndTime=now,
        ProductDescriptions = ['Linux/UNIX'],
    )
    prices = [ float(x['SpotPrice']) for x in response['SpotPriceHistory'] ]

    return(np.mean(prices))


def best_price(program):
    """Find the best instance by comparing against previous best."""

    default_time=-1
    if program=="freesurfer":
       default_time=10
    elif program=="bedpostx":
       default_time=5
    elif program=="probtrackx":
       default_time=7
    elif program=="neurosim":
      default_time=11

    max_price = sys.maxint

    print("Pricing all instances against all regions ...")
    for r in regions:
        for i in instances:
            price = price_instance(i, r)
            stats = [i, r, price]
            if price < max_price:
                max_price = price
                best_value = stats

    return(best_value)

#print("Price on this machine:")
#print(args.length/default_time * args.num * args.length)