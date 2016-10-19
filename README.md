# AWS-Estimator
Tool for estimating execution time and cost on Amazon Web Services.

## Using AWS-estimator

From Bash, access the estimator through `price.sh`:

    ./price.sh [-h] [-sSvnp] (-F | -B | -P | -N) length num

### Required Arguments:

 * `(-F | -B | -P | -N)` - Programs that can be estimated: **F**reesurfer, **b**edpostx, **p**robtrackx, **n**eurosim.
 * `length` - Length of a normal job, **in hours.**
 * `num` - Number of jobs

### Flags:

 * `-s/--show-all`      Show the price, etc. for all clusters evaluated.
 * `-S/--show-all-only` Show just the price, etc. for all clusters evaluated; better for grepping, etc. 
 * `-v/--verbose`       Be more verbose, also turns on `--show-all`
 * `-n/--no-gpus`       Do not evaluate GPU instances (for `*x` programs only.)
 * `-p/--plaintext`     Show results in plain English, helpful if you aren't sure how to parse the regular output.
 

## Files

`price.sh` - Bash interface for underlying scripts, has the parser, etc.

`price_instances.py` - Contains the methods for pricing individual machine/region combinations, and for choosing the cheapest one given parameters.

`instance_concurrency` - Contains info about parallelizability per cores (!`g2.*`) and per GPU instances.