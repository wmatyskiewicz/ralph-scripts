#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ralph.settings")

from django.conf import settings
from ralph.discovery.models_device import Device, DeviceType

DEVICE = {
    'model_name': 'xxxx',
    'position': '12',
    'rack': '14',
    'dc': 'test-dc'
}

def t1_update_devices_remarks():
    devices = Device.objects.all()[:100]
    for device in devices:
        device.remarks = 'test_remarks %s' % time.time()
        device.save()

def t2_create_devices():
    count = 0
    while (count < 99):
        Device.create(
            sn='test-%s' % time.time(),
            barcode='test-%s' % time.time(),
            model_name=DEVICE['model_name'],
            model_type=DeviceType.unknown,
            rack=DEVICE['rack'],
            position=DEVICE['position'],
            dc=DEVICE['dc'],
        )
        count = count + 1

# Run tests
t1_start = time.time()
t1_update_devices_remarks()
t1 = time.time()-t1_start

t2_start = time.time()
t2_create_devices()
t2 = time.time()-t2_start

print('Performance tests (Auto CI is %s)' % settings.AUTOCI)
print('Update devices remarks: %s seconds.' % t1)
print('Create devices: %s seconds.' % t2)

