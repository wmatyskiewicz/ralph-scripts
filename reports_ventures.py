#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, datetime, tempfile, smtplib, csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ralph.settings")

from django.db import models as db
from ralph.ui.views.reports import ReportVentures
from ralph.business.models import Venture, VentureExtraCostType

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders


def generate_temp_csv(csv_format):
    filename = tempfile.mktemp(".csv")
    f = open(filename, "wb")
    writer = csv.writer(f, delimiter=b';', quotechar=b'"')
    for row in csv_format:
    	unicode_row = [x.encode('utf-8') for x in row]
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



start = datetime.date.today() - datetime.timedelta(days=30)
end = datetime.date.today()

extra_types = list(
    VentureExtraCostType.objects.annotate(
        cost_count=db.Count('ventureextracost')
    ).filter(cost_count__gt=0).order_by('name')
)

data = ReportVentures()._get_venture_data(
    start=start,
    end=end,
    ventures= Venture.objects.all()[0:10],
    extra_types=extra_types,
)

format_csv = ReportVentures().export_csv(data, extra_types)
temp_csv = generate_temp_csv(format_csv)

send_email(
    you='user@domain',
    text = "In attachment there is a file with report",
    csv=temp_csv,
)
