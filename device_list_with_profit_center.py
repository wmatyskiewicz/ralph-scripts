#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph.discovery.models_device import Device

import csv

def dev_list():
    dev_list = [
    
    ]
    data = [
        ['Name', 'Venture', 'Symbol', 'Role', 'Department', 'Profit center']
    ]
    for hostname in dev_list:

        try:
            device = Device.objects.filter(name=hostname)
            for dev in device:
                data.append(
                    [
                        dev.name,
                        dev.venture.name,
                        dev.venture.symbol,
                        dev.role,
                        dev.venture.department.name if dev.venture.department else None,
                        dev.venture.profit_center.name if dev.venture.profit_center else None,
                    ]
                )
        except Device.DoesNotExist:
            data.append(
                [
                    hostname,
                    'Does Not Exist',
                    '',
                    '',
                    '',
                    '',
                ]
            )
    return data


def generate_csv(csv_format):
    c = csv.writer(open("MYFILE.csv", "wb"))
    for item in csv_format:
        c.writerow(item)

generate_csv(dev_list())
