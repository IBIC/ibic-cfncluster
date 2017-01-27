# AWS-Estimator
## Python version
by Trevor K. McAllister-Day

Tool for estimating execution time and cost on Amazon Web Services' Elastic Compute Cloud (EC2).

## Using `price.py`

From your terminal, access the estimator through `price.py`:

    python ./price.py [-h] [-sSvgp] length num

*You will need to install the python package* **boto3** *if you do not have it. See https://github.com/boto/boto3.*

### Required Arguments

 * `length`     Number of hours you expect your job to take (on average) on the appropriate instance.
 * `num`        How many jobs (brains) you have to execute.

### Flags

 * `-s/--show-all`      Show the price, etc. for all clusters evaluated.
 * `-S/--show-all-only` Show just the price, etc. for all clusters evaluated; better for grepping, etc. 
 * `-v/--verbose`       Be more verbose, also turns on `--show-all`
 * `-g/--gpus`          Evaluate GPU instances (we recommend this for compute-intensive pipelines, such as tractography, only.)
 * `-p/--plaintext`     Show results in plain English, helpful if you aren't sure how to parse the regular output.
 
## Files

`price.py` - Main Python script for estimating time and cost on AWS EC2.

`price_instances.py` - Contains the functions/methods for pricing individual machine/region combinations, and for choosing the cheapest one given parameters; called on by price.py.

`instance_concurrency` - Contains list of instance types and the number of vCPUs deployed for each instance.

## Tips

Use `sort -gk n,n` to sort results by the `n`th column. 

 * `-g`     Lexical sort numbers (i.e *1, 2, 10, 101*)
 * `-k n,n` Sort by column *n*.

## Example Usage

    $ python ./price.py 100 9 

    instance    m4.large            
    region      us-east-1e          
    total-$     7.1                 
    num         5                   
    exec-time   100                 
    $/hr        0.0142              
    #cores      2   

    $ ./price.sh -S 100 9 
    
    m4.2xlarge us-east-1e 13.66      2          100        0.0683     8          
    m4.10xlargeus-east-1c 35.42      1          100        0.3542     40         
    m4.large   us-east-1a 7.75       5          100        0.0155     2         
    ... 
