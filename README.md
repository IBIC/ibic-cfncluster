# AWS-Estimator
Tool for estimating execution time and cost on Amazon Web Services.

## Using AWS-estimator

From Bash, access the estimator through `price.sh`:

    price.sh [-h] (-F | -B | -P | -N) name length num size

 * `(-F | -B | -P | -N)` - Programs that can be estimated: **F**reesurfer, **b**edpostx, **p**robtrackx, **n**eurosim.
 * `name` - Identifier for cluster.
 * `length` - Length of a normal job, **in hours.**
 * `num` - Number of jobs
 * `size` - How much space needs to be reserved, both in uploaded files and created files, **in GB.**

## Files


`price.sh` - Bash interface for underlying scripts, has the parser, etc.

`price_instances.py` - Contains the methods for pricing individual machine/region combinations, and for choosing the cheapest one given parameters.