#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, csv, smtplib, tempfile, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ralph.settings")

from bob.csvutil import make_csv_response
from ralph.discovery.models_device import Device
from ralph.ui.views.reports import ReportDevicePricesPerVenture

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders


def devices_as_csv():
    data = []
    all_devices = Device.objects.exclude(sn__isnull=True).exclude(sn__exact='')[0:10]
    for device in all_devices:
        data.append(
            ReportDevicePricesPerVenture().device_details(
                device, exclude=['software']
            )
        )
    return data


def generate_temp_csv(csv_format):
    filename = tempfile.mktemp(".csv")
    f = open(filename, "wb")
    writer = csv.writer(f, delimiter=b';', quotechar=b'"')
    for row in csv_format:
        writer.writerow(row)
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


# Using

data = devices_as_csv()
csv_format = ReportDevicePricesPerVenture().get_csv_data(data)
temp_csv = generate_temp_csv(csv_format)

send_email(
    you='user@host',
	text = "In attachment there is a file with report",
	csv=temp_csv,
)
