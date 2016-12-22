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


args = parser.parse_args()

if args.verbose:
    print(args)

# Use GPUs is no_gpus flag is not set
search_gpus = not args.no_gpus

# show all if -s or -S is set
if args.show_all or args.show_all_only or args.verbose:
    show_all=True
else:
    show_all=False

get_best_cluster(args.num, args.length,
    gpu = search_gpus,
    showall = show_all,
    text = args.plaintext,
    showbest = not args.show_all_only)