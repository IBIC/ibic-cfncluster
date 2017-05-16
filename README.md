# AWS-Estimator

There are two programs in this project, written in Python and R respectively, designed to come up with the cheapest way for you to run neuroimaging  projects on Amazon Web Services' Elastic Compute Cloud ("in the cloud").

Both do the same thing, but just go about it slightly different ways on the backend. You can use whichever you are more comfortable with.

Each takes (at minimum) two arguments and a switch: 

 + The length of time (in hours) you expect your job to take on the appropriate instance class (m4/c4 vs. g2).
 + The number of jobs you have).
 + Whether to use GPU instances or not.

Both programs rely on the same set of flags and are called identically.

Both programs use the environment variable `IBICCFNCLUSTERLIB` to locate a file with the number of VCPUs in each instance type (`instance_concurrency`). If unspecified, this file will be located in `../lib`.

## Python
(Trevor K. McAllister-Day)

**You will need to install the python package `boto3` if you do not have it.**
See `https://github.com/boto/boto3`.

Basic usage:

    ibic-get-spot-estimate [--gpu] --hours HOURS --num NUM

### Example Usage

    $ cd python
    $ python/ibic-get-spot-estimate --hours 100 --num 9 

    instance    m4.large            
    region      us-east-1e          
    total-$     7.1                 
    num         5                   
    exec-time   100                 
    $/hr        0.0142              
    #cores      2   

## R

Usage:

    R/ibic-get-spot-estimate  [--gpu] --hours HOURS --num NUM

The R version was originally written to download information about instance configuration from the web. However, this is long and time consuming (about 20 minutes, depending on how many configurations and regions you query). We changed it to use a configuration file.

+ `-d/--download`   Forces R to download data from the internet.

### Example Usage

    $ R/ibic-get-spot-estimate --hours 100 --num 9 

       instancetype     region      price vcpu ninstances totalprice
    1    c4.2xlarge us-east-1a 0.06995468    8          2 0.13990937
    2    c4.2xlarge us-east-1b 0.07025850    8          2 0.14051700
    ...
    43    m4.xlarge us-east-1c 0.02970014    4          3 0.08910042
    44    m4.xlarge us-east-1e 0.02835648    4          3 0.08506944
    Minimum cost per instance is instancetype m4.large at price $ 0.01491771 /hr
    Maximum cost per instance is instancetype m4.16xlarge at price $ 0.5103859 /hr
    Minimum total cost estimate $ 0.07458855 ( 5 ) instances
    Maximum total cost estimate $ 0.5103859 ( 1 ) instances

## Common Flags

Both short and long flags are available for both programs.

### Required Arguments

 + `-H/--hours HOURS`      Number of hours you expect your job to take (on average) on the appropriate instance. Capital "H" to avoid conflict with default `-h` help flag.
 + `-n/--num NUM`     How many jobs (brains) you have to execute.

### Optional flags

 + `-g/--gpu`       Get cost estimates for GPU-enabled instances.
 + `-t/--total`     Display the total cost for the cheapest configuration only.

### Other flags

 + `-v/--verbose`   Be more verbose.
 + `-h/--help`      Display respective help menus.
