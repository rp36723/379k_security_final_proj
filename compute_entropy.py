#!/usr/bin/env python3
#Rishabh Pandey rp36723

import argparse
import csv
import math
from collections import defaultdict, Counter
from pathlib import Path

#command line file(s) input with bucket size and output CSV
#4096 is default bucket size as page size in Linux is 4kb
parser = argparse.ArgumentParser()
parser.add_argument("csv_files", nargs="+")
parser.add_argument("--bucket-size", type=int, default=4096)
parser.add_argument("--output-summary", default="entropy_summary.csv")
args = parser.parse_args()

#addresses grouped by memory region and filename
#reads the input file(s)
data = defaultdict(list)
for csv_path in args.csv_files:
    p = Path(csv_path)
    #print(f"[+] Reading {p}")
    with p.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            config_name = row["config_name"]
            region = row["region"]
            addr_int = int(row["address_int"])
            data[(config_name, region)].append(addr_int)

#entropy calculate for each group and bucket
records = []
for (config_name, region), addrs in sorted(data.items()):
    #addresses of buckets
    buckets = [addr // args.bucket_size for addr in addrs]
    counter = Counter(buckets)

    #compute Shannon Entropy in bits
    counts = counter.values()
    total = sum(counts)
    
    if total == 0:
        H = 0.0
    else:
        H = 0.0
        for c in counts:
            if c == 0:
                continue
            p = c / total
            H -= p * math.log2(p)

    #pull Shannon entropy value alongside potential max
    num_samples = len(addrs)
    num_buckets = len(counter)
    max_entropy = math.log2(num_buckets) if num_buckets > 0 else 0.0

    #print(f"Config={config_name:15s} Region={region:12s} "f"samples={num_samples:6d} buckets={num_buckets:5d} " f"H={H:6.3f} bits (max possible {max_entropy:6.3f} bits)")
    records.append({"config_name": config_name,"region": region,"num_samples": num_samples,"num_buckets": num_buckets,"entropy_bits": H,"max_entropy_bits": max_entropy})

#summary file
with open(args.output_summary, "w", newline="") as f:
    fieldnames = ["config_name","region","num_samples","num_buckets","entropy_bits","max_entropy_bits"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for rec in records:
        writer.writerow(rec)