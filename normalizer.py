#!/usr/bin/env python
import argparse
import csv
from datetime import datetime, timedelta

from dateutil.parser import parse as dateparse
from dateutil import tz

PACIFIC = tz.gettz('America/Los_Angeles')
EASTERN = tz.gettz('America/New_York')

def convert_timestamp(datestamp):
    parsed = dateparse(datestamp)
    as_gmt = parsed.replace(tzinfo=PACIFIC)
    as_pacific = as_gmt.astimezone(tz=EASTERN)
    # Outputs as RFC 3339 date
    return as_pacific.isoformat()

def verify_zipcode(zip):
    # All zip codes are 5 digits.  If less, assume 0 as a prefix
    return zip.zfill(5)

def parse_name(name):
    return name.upper()

def parse_address(address):
    if isinstance(address, str):
        return str(address)
    else:
        return address.decode()

def parse_duration(duration):
    # HH:MM:SS.MS format
    seconds = 0
    try:
        t = datetime.strptime(duration, '%H:%M:%S.%f')
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
        seconds = delta.total_seconds()
    except ValueError:
        # Invalid duration format
        pass
    return seconds

def parse_notes(notes):
    return

def input_data(input_file):
    rows = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        rows = list(csv.DictReader(csvfile))
        for row in rows:
            row['Timestamp'] = convert_timestamp(row['Timestamp'])
            row['ZIP'] = verify_zipcode(row['ZIP'])
            row['FullName'] = parse_name(row['FullName'])
            row['Address'] = parse_address(row['Address'])
            row['FooDuration'] = parse_duration(row['FooDuration'])
            row['BarDuration'] = parse_duration(row['BarDuration'])
            row['TotalDuration'] = row['BarDuration'] + row['FooDuration']

    return rows

def output_data(data, output_file):
    with open(output_file, "w", encoding='utf-8') as f:
        fieldnames = ['Timestamp','ZIP','FullName','Address','FooDuration','BarDuration','TotalDuration','Notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_file', required=True, help="name of the input file")
    parser.add_argument('-o', '--output_file', required=True, help="name of the file to store results")
    args, argv = parser.parse_known_args()
    input_file = args.input_file
    output_file = args.output_file

    data = input_data(input_file)
    output_data(data, output_file)

