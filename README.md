# AWS-Estimator

There are two programs in this project, written in Python and R respectively, designed to come up with the cheapest way for you to run neuroimaging  projects on Amazon Web Services' Elastic Compute Cloud ("in the cloud").

Both do fundamentally the same thing, but just go about it slightly different ways on the backend. You can use whichever you are more comfortable with.

Each takes (at minimum) two arguments and a switch: 

 + The length of time (in hours) you expect your job to take on the appropriate instance class (m4/c4 vs. g2).
 + The number of jobs (brains) you have.
 + Whether to use GPU instances or not.

More information about each program can be found in their respective READMEs, but basic usage is also documented here.

## Python
(Trevor K. McAllister-Day)

Basic usage:

    ./price.py [--gpu] --hours HOURS --num NUM

`price.py` also has options for modifying the output: `--show-all`, `--show-all-only`, `--verbose`, and `--plaintext`.

## R
(Tara Madhyastha)

Usage:

    ./get-spot-estimate [--gpu] --hours HOURS --num NUM