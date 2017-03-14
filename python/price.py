#!/usr/bin/env python

import argparse
from price_instances import get_best_cluster # best_price

parser = argparse.ArgumentParser(description="Determine the best value for a \
    given program based on execution time.")

# Putting the required flag arguments into their own group stops them from
## showing up under the confusing header "optional argumetnts"
required_named = parser.add_argument_group("required named arguments")

required_named.add_argument("-H", "--hours", type=int, required=True,
    help="Job execution time, on one brain in hours on a neuron-class " + \
    "machine (adrc, tpp, panuc), single-threaded. -H to not conflict with " + \
    "help.")
required_named.add_argument("-n", "--num", type=int, required=True,
    help="How many jobs you have.", default=1)

parser.add_argument("-s", "--show-all", action="store_true",
    help="Show info for all possible clusters.")
parser.add_argument("-S", "--show-all-only", action="store_true",
    help="Show info for all possibly clusters only (i.e. do not show best " + \
    "configuration")

parser.add_argument("-v", "--verbose", action="store_true",
    help="Be more verbose (turns on `show all\')")

parser.add_argument("-g", "--gpu", action="store_true",
    help="Don't calculate for GPU instances.")

parser.add_argument("-p", "--plaintext", action="store_true",
    help="Show results parsed into plain English.")

parser.add_argument("-t", "--total", action="store_true",
    help="Show the total cost for the cheapest configuration only.")

args = parser.parse_args()

if args.verbose:
    print(args)

# show all if -s or -S is set
if args.show_all or args.show_all_only or args.verbose:
    show_all = True
else:
    show_all = False

if args.total or args.show_all_only:
    show_best = False
else:
    show_best = True

get_best_cluster(args.num, args.hours,
    gpu = args.gpu,
    showall = show_all,
    text = args.plaintext,
    showbest = show_best)

# ,
#     total = args.total)