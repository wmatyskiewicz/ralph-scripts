#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, csv, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ralph.settings")

from bob.csvutil import make_csv_response
from ralph.discovery.models_device import Device
from ralph.ui.views import reports


data = []
all_devices = Device.objects.exclude(sn__isnull=True).exclude(sn__exact='')

for device in all_devices:
    data.append(
        reports.ReportDevicePricesPerVenture().device_details(
            device, exclude=['software']
        )
    )
    sys.stdout.write('.')

csv_format = reports.ReportDevicePricesPerVenture().get_csv_data(data)

file = open("/tmp/reports.csv", 'wb')
writer = csv.writer(file, delimiter=b';', quotechar=b'"')

row = []
for field in csv_format:
    writer.writerow(field)
file.close()
