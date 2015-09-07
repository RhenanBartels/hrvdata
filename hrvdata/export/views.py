import csv
import json
import os
import tempfile

from django.shortcuts import render
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from upload.models import Tachogram

from analysis.hrvtools.hrv import TimeDomain, TimeVarying, FrequencyDomain

def index(request, filename):
    user = request.user
    rri_obj = Tachogram.objects.get(owner=user, filename=filename)
    rri = get_file_information(rri_obj.rri)
    reponse = create_csv_document(rri, filename)
    export_file = zip(range(len(rri)), rri)
    return reponse

#    return HttpResponse(json.dumps(export_file),
#        content_type="application/json")

def get_file_information(f):
    for chunk in f.chunks():
        rri = chunk
    rri = rri.split("\r\n")
    rri = [float(rri) for rri in rri if rri]
    return  rri

def create_csv_document(rri, filename):
    time_domain = TimeDomain(rri)
    time_domain.calculate()
    time_varying = TimeVarying(rri, 30, 0)
    time_varying.calculate()
    frequency_domain = FrequencyDomain(rri)
    frequency_domain.calculate(256, 128)

# Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.\
            format(filename)

    writer = csv.writer(response)
    writer.writerow(["Time Domain"])
    writer.writerow(["RMSSD (ms)", "%.2f" % time_domain.rmssd])
    writer.writerow(["SDNN (ms)", "%.2f" % time_domain.sdnn])
    writer.writerow(["pNN50 (%)", "%.2f" % time_domain.pnn50])
    writer.writerow(["Mean RRi (ms)", "%.2f" % time_domain.rri_mean])
    writer.writerow(["Mean HR (bpm)", "%.2f" % time_domain.hr_mean])
    writer.writerow(["Frequency Domain"])
    writer.writerow(["Total Power (ms^2)", "%.2f" % frequency_domain.total_power])
    writer.writerow(["VLF (ms^2)", "%.2f" % frequency_domain.vlf])
    writer.writerow(["LF (ms^2)", "%.2f" % frequency_domain.lf])
    writer.writerow(["HF (ms^2)", "%.2f" % frequency_domain.hf])
    writer.writerow(["LF/HF", "%.2f" % frequency_domain.lfhf])
    writer.writerow(["LFn.u", "%.2f" % frequency_domain.lfnu])
    writer.writerow(["HFn.u", "%.2f" % frequency_domain.hfnu])
    writer.writerow(["Time Varying"])
    #Browse through Time Varying re
    rmssdi = list(time_varying.rmssd)
    rmssdi.insert(0, "RMSSDi (ms)")
    sdnni = list(time_varying.sdnn)
    sdnni.insert(0, "SDNNi (ms)")
    pnn50i = list(time_varying.pnn50)
    pnn50i.insert(0, "pNN50i (%)")
    rri_meani = list(time_varying.rri_mean)
    rri_meani.insert(0, "Mean RRii (ms)")
    hr_meani = list(time_varying.hr_mean)
    hr_meani.insert(0, "Mean HRi (bpm)")
    writer.writerows([rmssdi])
    writer.writerows([sdnni])
    writer.writerows([pnn50i])
    writer.writerows([rri_meani])
    writer.writerows([hr_meani])
    return response

