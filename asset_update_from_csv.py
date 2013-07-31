#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import csv

from ralph_assets.models_assets import Asset

def csv_to_dicts(filename):
    with open(filename, 'rU') as file:
        reader = csv.reader(file)
        data = []
        for i, row in enumerate(reader):
            if i == 0:
                fields = row[0].split(';')
            else:
                field = {}
                for key, item in enumerate(row[0].split(';')):
                    field[fields[key]] = item
                data.append(field)
    return data, fields


def asset_update(filename):
    csv_data, db_fields = csv_to_dicts(filename)
    for item in csv_data:
        try:
            asset = Asset.objects.get(id=item.get('id'))
        except Asset.DoesNotExist:
            print(item.get('id'))
            continue
        for field in db_fields:
            old_value = getattr(asset, field)
            new_value = item.get(field)
            if not old_value == new_value:
                setattr(asset, field, new_value)
                print(asset.id, field, old_value, new_value)
        asset.save()
