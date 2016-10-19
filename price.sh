#!/usr/bin/env python

import argparse
from price_instances import get_best_cluster # best_price

parser = argparse.ArgumentParser(description="Determine the best value for a \
    given program based on execution time.")

# parser.add_argument("name", help="What to name this cluster.")
parser.add_argument("length", type=int, help="Job execution time, on one " + \
    "brain in hours on a neuron-class machine (adrc, tpp, panuc), " + \
    "single-threaded")
parser.add_argument("num", type=int, help="How many jobs you have.", default=1)
# parser.add_argument("size", type=int, 
#     help="Estimate how large the volume needs to be, in GB.")

parser.add_argument("-s", "--show-all", action="store_true", 
    help="Show info for all possible clusters.")

parser.add_argument("-S", "--show-all-only", action="store_true",
    help="Show info for all possibly clusters only (i.e. do not show best " + \
    "configuration")

parser.add_argument("-v", "--verbose", action="store_true",
    help="Be more verbose (turns on \`show all\')")

parser.add_argument("-n", "--no-gpus", action="store_true",
    help="Don't calculate for GPU instances.")

parser.add_argument("-p", "--plaintext", action="store_true",
    help="Show results parsed into plain English.")

group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("-F", "--freesurfer", action="store_true", 
    help="Estimate for freesurfer.")
group.add_argument("-B", "--bedpostx", action="store_true",
    help="Estimate for bedpostx.")
group.add_argument("-P", "--probtrackx", action="store_true",
    help="Estimate for probtrackx.")
group.add_argument("-N", "--neurosim", action="store_true",
    help="Estimate for neurosim.")

# output=parser.add_mutually_exclusive_group(required=True)
# output.add_argument("-Q", "--quickest", action="store_true", 
#     help="Get the quickest cluster configuration.")
# output.add_argument("-C", "--cheapest", action="store_true",
#     help="Get the cheapest cluster configuration.")
# output.add_argument("-A", "--all", action="store_true",
#     help="Get all configurations.")

args = parser.parse_args()

if args.verbose:
    print(args)
    args.show_all = True

# if args.all:
#     args.quickest = True
#     args.cheapest = True

if args.freesurfer:
    program = "freesurfer"
elif args.bedpostx:
    program = "bedpostx"
elif args.probtrackx:
    program = "probtrackx"
elif args.neurosim:
    program = "neurosim"

# Set gpu status
if args.no_gpus:
    # no gpus if no-gpus flag set
    gpu = False
elif args.bedpostx or args.probtrackx:
    # if flag not set, and using *x program, gpus
    gpu = True
else:
    # freesurfer/neurosim: don't use gpu 
    gpu = False

# print args if verbose is on
if args.verbose:
    print(args)

# show all if -s or -S is set
if args.show_all or args.show_all_only:
    showall=True
else:
    showall=False


# print(best_price(program, args.length, args.num, quick=args.quickest,
    # cheapest=args.cheapest, gpu=gpu))

get_best_cluster(args.num, args.length, 
    gpu = gpu,
    program = program,
    showall = showall,
    text = args.plaintext,
    showbest = not args.show_all_only)