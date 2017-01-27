import csv

from price_instances import price_instance
from datetime import datetime, date, time, timedelta

instances = ['m3.medium','m3.large','m3.xlarge','m3.2xlarge',
                 'm4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge',
                 'r3.large','r3.xlarge','r3.2xlarge','r3.4xlarge','r3.8xlarge',
                 #'x1.4xlarge','x1.8xlarge','x1.16xlarge','x1.32xlarge',
                 'i2.xlarge','i2.2xlarge','i2.4xlarge','i2.8xlarge',
                 'c3.large','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge',
                 'c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge',
                 #'cc1.4xlarge',
                 'g2.2xlarge','g2.8xlarge',
                 'd2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge'
                 ]


gpu_instances = ['g2.2xlarge', 'g2.8xlarge']

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

# Experimentally determined speed up times.
speed_up = {"freesurfer": 1.3, "bedpostx": 161, "probtrackx": 14.9,
            "neurosim": 1}

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
         'g2.2xlarge': 1, 'g2.8xlarge': 1  
         # Not actual cpus, but no gpu concurrency
         }

with open("prices.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    for i in instances + gpu_instances:
        print(i)
        writer.writerow([i, str(price_instance(i, "us-west-2")), ncpus[i]])

print("Done!")