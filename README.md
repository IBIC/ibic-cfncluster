# AWS-Estimator

There are two programs in this project, written in Python and R respectively, designed to come up with the cheapest way for you to run neuroimaging  projects on Amazon Web Services ("in the cloud").

Both do fundamentally the same thing, but just go about it slightly different ways on the backend. You can use whichever you are more comfortable with.

Each takes two arguments: 

 + The length of time (in hours) it takes to complete a pipeline on a single 
 brain, on a neuron-class machine or equivalent.
 + The number of jobs (brains) you have.

More information about each program can be found in their respective READMEs, but basic usage is also documented here.

## Python
(Trevor K. McAllister-Day)

Basic usage:

    ./price.sh [--no-gpus] <hours> <N>

`price.sh` also has options for modifying the output: `--show-all`, `--show-all-only`, `--verbose`, and `--plaintext`.

## R
(Tara Madhyastha)

Usage:

    ./get-spot-estimate [--gpu] --hours H --num N