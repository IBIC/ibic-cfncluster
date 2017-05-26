# AWS-Estimator

There are two programs in this project, written in Python and R respectively, designed to come up with the cheapest way for you to run neuroimaging  projects on Amazon Web Services' Elastic Compute Cloud ("in the cloud").

Both do the same thing, but just go about it slightly different ways on the backend. You can use whichever you are more comfortable with.

Each takes (at minimum) two arguments and a switch: 

 + The length of time (in hours) you expect your job to take on the appropriate instance class (m4/c4 vs. g2).
 + The number of jobs you have).
 + Whether to use GPU instances or not.

Both programs rely on the same set of flags and are called identically.

Both programs use the environment variable `IBICCFNCLUSTERHOME` to locate a file with the number of VCPUs in each instance type (`instance_concurrency`). This file is located by default in `$IBICCFNCLUSTERHOME/lib/`.

## Python
(Trevor K. McAllister-Day)

**You will need to install the python package `boto3` if you do not have it.**
See `https://github.com/boto/boto3`.

Basic usage:

    ibic-get-spot-estimate [--gpu] --hours HOURS --num NUM

### Example Usage

    $ python/ibic-get-spot-estimate --hours 100 --num 9 

    instance     c4.large            
    region       ap-south-1b         
    total-$      8.3                 
    num-jobs     5                   
    exec-time    100                 
    $/hr         0.0166              
    #cores       2      

## R
(Tara Madhyastha)

Usage:

    ibic-get-spot-estimate  [--gpu] --hours HOURS --num NUM

The R version was originally written to download information about instance configuration from the web. However, this is long and time consuming (about 20 minutes, depending on how many configurations and regions you query). We changed it to use a configuration file.

+ `-d/--download`   Forces R to download data from the internet.

### Example Usage

    $ R/ibic-get-spot-estimate --hours 100 --num 9 

 

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

## Setting `IBICCFNCLUSTERHOME`

In order to run either the Python or the R script, the environment variable `IBICCFNCLUSTERHOME` needs to be set. 

You can set it at runtime with the command below, but this only works in that terminal for as long as you leave it open.

    export IBICCFNCLUSTERHOME=/path/to/aws-home

To have `IBICCFNCLUSTERHOME` persist across sessions, add the export line to your `.bashrc` file (or another file like `.bash_profile`.) This will make it so any session opened after that point will have `IBICCFNCLUSTERHOME` set.

To set it for the current session, source your `.bashrc`:

    source ~/.bashrc

Or, if you don't want to do it yourself, you can run the script `install.sh`, which will edit your `.bashrc` (or other file) for you.