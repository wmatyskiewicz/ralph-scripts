# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime


from ralph.util import plugin, api_pricing
from ralph_pricing.plugins import shares
from ralph_pricing.models import Device


def update_history_share():
    today = datetime.date.today()
    end = datetime.date(2013, 3, 30)  # XXX Make it configurable!
    for share in api_pricing.get_shares():
        date = today
        device, created = Device.objects.get_or_create(device_id=share['storage_device_id'])
        while date > end:
            shares.update_usage(
                device=device,
                venture=None,
                usage_name=share['model'],
                date=date,
                value=share['size'],
            )
            date -= datetime.timedelta(days=1)
