#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get details for a house area using a postcode.
author: Shaun Molloy <shaunmolloy@gmail.com>
"""
import csv
import datetime
from tabulate import tabulate
from helpers import *


def land_registry(postcode, number=None):
    """
    Get tenure: Freehold or Leasehold.

    :param postcode
    :param number
    """
    # Download complete csv file
    url = 'http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv'
    filename = os.path.basename(url)
    download_file(filename, url)

    # dict object for keys
    history = {}
    sold = {}
    types = {
        'S': "Semi-Detached",
        'D': "Detached",
        'T': "Terraced",
        'F': "Flats",
        'O': "Other",
    }

    # Parse csv file
    lines = find_in_file(postcode, filename)

    if lines is not None:
        for line in csv.reader(lines):
            pos_price = 2-1
            pos_date = 3-1
            pos_type = 5-1
            pos_new = 6-1
            pos_tenure = 7-1
            pos_addr1 = 8-1
            pos_addr2 = 10-1

            price = '£{:,.0f}'.format(int(line[pos_price]))
            date = datetime.datetime.strptime(line[pos_date], '%Y-%m-%d 00:00')
            date = datetime.date.strftime(date, "%Y-%m-%d")

            if number is not None and number == line[pos_addr1]:
                # [date] = {...}
                history[date] = {
                    "street": line[pos_addr2].title(),
                    "price": price,
                    "new": ("Yes" if line[pos_new] == 'Y' else "No"),
                    "type": types[line[pos_type] ],
                    "tenure": ("Freehold" if line[pos_tenure] == 'F' else "Leasehold"),
                }

            # [date] = '...'
            sold[date] = price

        if number is not None:
            recent_history = sorted(history.items(), reverse=True)
            data = []

            for i in recent_history:
                row = [
                    i[0],
                    number,
                    i[1]['street'],
                    i[1]['price'],
                    i[1]['new'],
                    i[1]['type'],
                    i[1]['tenure'],
                ]
                data.append(row)

            heading("Sale History")
            print(tabulate(data, headers=['Date', 'Number', 'Street', 'Price', 'New', 'Type', 'Tenure']))

        recently_sold = sorted(sold.items(), reverse=True)
        count = 0
        data = []

        for j in recently_sold:
            count += 1
            if count > 2:
                break

            row = [
                j[0],
                j[1],
            ]
            data.append(row)

        heading("Recently Sold")
        print(tabulate(data, headers=['Date', 'Price']))

    else:
        die("Error: Postcode not found")


if not len(sys.argv) > 1:
    # TODO add more detailed help message
    die("Missing arguments")

# With postcode, apply trim and convert to uppercase
postcode = sys.argv[1].strip().upper()
number = None

clear()

# TODO validate postcode
if not len(postcode) > 0:
    die("Missing postcode")

if len(sys.argv) > 2:
    number = sys.argv[2].strip()
    print(tabulate([ [number, postcode] ], headers=['Number', 'Postcode']))
else:
    print(tabulate([ [postcode] ], headers=['Postcode']))

land_registry(postcode, number)
