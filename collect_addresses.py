#!/usr/bin/env python3
#Rishabh Pandey, rp36723

import argparse
import csv
import subprocess
import sys

#command line arguments for multiple files/binary utilized
parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
parser.add_argument("--runs", type=int, default=100)
parser.add_argument("--config-name", required=True)
parser.add_argument("--output-csv", required=True)
args = parser.parse_args()

with open(args.output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    #header to parse in entropy calculation
    writer.writerow(["run_id","config_name","binary_name","region","address_hex","address_int"])

    for run_id in range(args.runs):
        #binaries are run using subproccesses
        #capture stdout/error if there is any
        proc = subprocess.run([args.binary],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)

        #parse address lines from stdout
        #empty/incorrect lines are skipped
        for line in proc.stdout.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            
            #convert hex address to int + csv write
            region, addr_hex = parts
            addr_int = int(addr_hex, 16)
            writer.writerow([run_id,args.config_name,args.binary,region,addr_hex,addr_int])

        # if (run_id + 1) % 100 == 0:
        #     print(f"[+] Completed {run_id + 1} / {args.runs} runs", file=sys.stderr)