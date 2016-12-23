# AWS-Estimator
## R version
Tara Madhyastha

Tool for estimating execution time and cost on Amazon Web Services.

## Using `get_spot_estimate`

`get_spot_estimate` is a Bash script, so it can be called directly from the command line with the following arguments:

    ./get_spot_estimate [-h] [--gpu] --hours [HOURS] --num [NUM]

### Required Arguments

 + `--hours HOURS`      Number of hours you expect your job to take (on average) on the appropriate instance.
 + `--num NUM`          How many jobs (brains) you have to execute.

### Flags

 + `--gpu`              Evaluate GPU instances? 

## Example Usage 

    $ ./get_spot_estimate --hours 100 --num 9 

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

(`get_spot_estimate` will output messages related to pulling information from the Amazon API.)