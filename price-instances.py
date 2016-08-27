import boto3
from datetime import datetime, date, time, timedelta
import numpy as np
import sys

instances = ['m3.medium','m3.large','m3.xlarge','m3.2xlarge',
             'm4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge',
#            'r3.large','r3.xlarge','r3.2xlarge','r3.4xlarge','r3.8xlarge',
#            'x1.4xlarge','x1.8xlarge','x1.16xlarge','x1.32xlarge',
#            'i2.xlarge','i2.2xlarge','i2.4xlarge','i2.8xlarge',
             'c3.large','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge',
             'c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge', ]
#            'cc1.4xlarge',
#            'g2.2xlarge','g2.8xlarge',
#             'd2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge']

regions = ['us-east-1', 'us-west-2', 'us-west-1',
           'eu-west-1', 'eu-central-1',
           'ap-southeast-1', 'ap-northeast-1', 'ap-southeast-2', 'ap-northeast-2', 'ap-south-1',
           'sa-east-1']

# N. Virginia, Oregon, N. California
# Ireland, Frankfurt
# Singapore, Tokyo, Sydney, Seoul, Mumbai
# Sao Paulo

# Price over the last five days
five_days = timedelta(5)
now = datetime.now()
five_days_ago = now - five_days

# Return the mean price for an instance in a region over the last five days
def price_instance(instancename, region):
    client = boto3.client("ec2", region)
    response = client.describe_spot_price_history(
        InstanceTypes =[instancename],
        StartTime=five_days_ago,
        EndTime=now,
        ProductDescriptions = ['Linux/UNIX'],
    )
    prices = [ float(x['SpotPrice']) for x in response['SpotPriceHistory'] ]

    return(np.mean(prices))

print("Pricing all instances against all regions ...")

# Find the best instance by comparing against previous best.
max_price = sys.maxint
for r in regions:
    for i in instances:
        price = price_instance(i, r)
        stats = [i, r, price]
        if price < max_price:
            max_price = price
            best_value = stats

print("Best value:")
print(best_value)
