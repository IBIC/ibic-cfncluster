# AWS-Estimator
## Python version
Trevor K. McAllister-Day

Tool for estimating execution time and cost on Amazon Web Services.

## Using `price.sh`

From Bash, access the estimator through `price.sh`:

    ./price.sh [-h] [-sSvgp] length num

### Required Arguments:

 * `length` - Estimate of job length, **in hours.**
 * `num` - Number of jobs

### Flags:

 * `-s/--show-all`      Show the price, etc. for all clusters evaluated.
 * `-S/--show-all-only` Show just the price, etc. for all clusters evaluated; better for grepping, etc. 
 * `-v/--verbose`       Be more verbose, also turns on `--show-all`
 * `-g/--gpus`          Evaluate GPU instances (for tractography programs only.)
 * `-p/--plaintext`     Show results in plain English, helpful if you aren't sure how to parse the regular output.
 

## Files

`price.sh` - Bash interface for underlying scripts, has the parser, etc.

`price_instances.py` - Contains the methods for pricing individual machine/region combinations, and for choosing the cheapest one given parameters.

`instance_concurrency` - Contains info about parallelizability per cores (m4/c4)and per GPU instances (g2).

## Tips

Use `sort -gk n,n` to sort results by the `n`th column. 

 * `-g`     Lexical sort numbers (i.e *1, 2, 10, 101*)
 * `-k n,n` Sort by column *n*.

## Example Usage

    $ ./price.sh 100 9 

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
