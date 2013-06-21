#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph.discovery.models_device import Device

import os, datetime, tempfile, smtplib, csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders


def dev_list():
    dev_list = [

    ]
    data = []
    for hostname in dev_list:
        device = Device.objects.get(name=hostname)
        name = device.name
        venture = device.venture.name
        symbol = device.venture.symbol
        role = device.role
        department = None
        if device.venture.department:
            department = device.venture.department.name
        profit_center = None
        if device.venture.profit_center:
            profit_center = device.venture.profit_center.name
        data.append(
            {
                name,
                venture,
                symbol,
                role,
                department,
                profit_center,
            }
        )
    return data


def generate_temp_csv(csv_format):
    filename = tempfile.mktemp(".csv")
    f = open(filename, "wb")
    writer = csv.writer(f, delimiter=b';', quotechar=b'"')
    for row in csv_format:
        unicode_row = [x for x in row]
        # unicode_row = [x.encode('utf-8') for x in row]
        writer.writerow(unicode_row)
    f.close()
    return f


def send_email(you, me='ralph@local', subject='Reports', text='', csv=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    msg.attach(MIMEText(text, 'plain'))
    if csv is not None:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(csv.name,"r").read())
        Encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename="%s"' % os.path.basename(csv.name)
        )
        msg.attach(part)
    send = smtplib.SMTP('localhost')
    send.sendmail(me, you, msg.as_string())
    send.quit()


format_csv = dev_list()
temp_csv = generate_temp_csv(format_csv)

send_email(
    you='wojciech.matyskiewic@ext.allegro.pl',
    text="In attachment there is a file with report",
    csv=temp_csv,
)
