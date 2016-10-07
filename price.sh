#!/usr/bin/env python

import argparse
from price_instances import best_price

parser = argparse.ArgumentParser(description="Determine the best value for a \
    given program based on execution time.")

parser.add_argument("name", help="What to name this cluster.")
parser.add_argument("length", type=int, help="Job execution time, on one " + \
    "brain in hours on a neuron-class machine (adrc, tpp, panuc), " + \
    "single-threaded")
parser.add_argument("num", type=int, help="How many jobs you have.", default=1)
# parser.add_argument("size", type=int, 
#     help="Estimate how large the volume needs to be, in GB.")

group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("-F", "--freesurfer", action="store_true", 
    help="Estimate for freesurfer.")
group.add_argument("-B", "--bedpostx", action="store_true",
    help="Estimate for bedpostx.")
group.add_argument("-P", "--probtrackx", action="store_true",
    help="Estimate for probtrackx.")
group.add_argument("-N", "--neurosim", action="store_true",
    help="Estimate for neurosim.")

output=parser.add_mutually_exclusive_group(required=True)
output.add_argument("-Q", "--quickest", action="store_true", 
    help="Get the quickest cluster configuration.")
output.add_argument("-C", "--cheapest", action="store_true",
    help="Get the cheapest cluster configuration.")
output.add_argument("-A", "--all", action="store_true",
    help="Get all configurations.")

args = parser.parse_args()

if args.all:
    args.quickest = True
    args.cheapest = True

if args.freesurfer:
	program="freesurfer"
elif args.bedpostx:
	program="bedpostx"
elif args.probtrackx:
	program="probtrackx"
elif args.neurosim:
    program="neurosim"

if args.bedpostx or args.probtrackx:
    gpu = True

print(best_price(program, args.length, args.num, quick=args.quickest,
    cheapest=args.cheapest, gpu=gpu))