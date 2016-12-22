# AWS-Estimator
## Python version

Tool for estimating execution time and cost on Amazon Web Services.

## Using AWS-estimator

From Bash, access the estimator through `price.sh`:

    ./price.sh [-h] [-sSvgp] length num

### Required Arguments:

 * `length` - Length of a normal job, **in hours.**
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

`instance_concurrency` - Contains info about parallelizability per cores 
(!`g2.*`) and per GPU instances.

## Tips

Use `sort -gk n,n` to sort results by the `n`th column. 

 * `-g`     Lexical sort numbers (i.e *1, 2, 10, 101*)
 * `-k n,n` Sort by column *n*.