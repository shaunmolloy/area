#!/usr/bin/env python
"""
Get details for a house area using a postcode.
author: Shaun Molloy <shaunmolloy@gmail.com>
"""
import os
import sys
import csv
import helpers


def land_registry(postcode):
    """
    Get tenure: Freehold or Leasehold.

    :param postcode
    """
    # Download complete csv file
    url = 'http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv'
    filename = os.path.basename(url)
    helpers.download_file(filename, url)
    found = False

    # Parse csv file
    for line in open(filename):
        if postcode in line:
            found = True
            reader = csv.reader([line])
            columns = list(*reader)

            pos_price = 2-1
            pos_date = 3-1
            pos_type = 5-1
            pos_tenure = 7-1

            print("price: %s" % columns[pos_price] )
            print("sold: %s" % columns[pos_date] )
            print("type: %s" % ("semi-detached" if columns[pos_type] == 'S' else "detached") )
            print("tenure: %s" % ("freehold" if columns[pos_tenure] == 'F' else "leasehold") )

            break

    if not found:
        print("Error: Postcode not found")
        sys.exit()


if not len(sys.argv) > 1:
    # TODO add more detailed help message
    print("Missing arguments")
    sys.exit()

# With postcode, apply trim and convert to uppercase
postcode = sys.argv[1].strip().upper()

# TODO validate postcode
if not len(postcode) > 0:
    print("Missing postcode")
    sys.exit()

print("Postcode: %s" % postcode)

land_registry(postcode)
