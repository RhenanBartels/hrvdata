import json

import numpy as np

from django.shortcuts import render
from django.http import HttpResponse

from upload.models import Tachogram

from hrvtools.hrv import TimeDomain, TimeVarying, FrequencyDomain
#TODO: use new hrv module intalled with pip. Remove hrvtools library
def index(request, filename):
    user = request.user
    rri_file = Tachogram.objects.get(owner=user, filename=filename)
    rri = get_file_information(rri_file.rri)
    time_domain= TimeDomain(rri)
    frequency_domain = FrequencyDomain(rri)
    segment = 256
    overlap = 128
    frequency_domain.calculate(segment, overlap)
    time_domain.calculate()
    results = {'rmssd': round(time_domain.rmssd, 2),
            'sdnn': round(time_domain.sdnn, 2),
            'pnn50':round(time_domain.pnn50, 2),
            'mrri':round(time_domain.rri_mean, 2),
            'mhr': round(time_domain.hr_mean, 2),
            "totalpower": round(frequency_domain.total_power, 2),
            "vlf": round(frequency_domain.vlf, 2),
            "lf": round(frequency_domain.lf,2),
            "hf":round(frequency_domain.hf, 2),
            "lfhf": round(frequency_domain.lfhf, 2),
            "lfnu": round(frequency_domain.lfnu, 2),
            "hfnu": round(frequency_domain.hfnu, 2),
            "filename": filename}
    if request.is_ajax():
        time_varying = TimeVarying(rri, 30, 0)
        time_varying.calculate()
        rri = time_domain.rri
        rri_time = time_varying.rri_time
        rri_result = zip(rri_time, rri)
        rmssdi = time_varying.rmssd
        segment_interval = time_varying.segment_interval
        rmssdi_result = zip(segment_interval, rmssdi)
        vlf_psd, lf_psd, hf_psd = split_psd_classes(frequency_domain)
        psd = zip(frequency_domain.fxx, frequency_domain.pxx)
        results = {'rri': rri_result, "rmssdi": rmssdi_result,
                "vlfpsd": vlf_psd, "lfpsd": lf_psd, "hfpsd": hf_psd,
                "psd": psd, "time_varying_index": "rmssd"}
        return HttpResponse(json.dumps(results), content_type="application/json")
    else:
        return render(request, "index.html", results)

def change_tv_index(request, filename, indexname):
    user = request.user
    rri_file = Tachogram.objects.get(owner=user, filename=filename)
    rri = get_file_information(rri_file.rri)
    time_varying = TimeVarying(rri, 30, 0)
    time_varying.calculate()
    if indexname == "rmssdi_li":
        time_varying_index = time_varying.rmssd
        time_varying_name = "rmssd"
    elif indexname == "sdnni_li":
        time_varying_index = time_varying.sdnn
        time_varying_name = "sdnn"
    elif indexname == "pnn50i_li":
        time_varying_index = time_varying.pnn50
        time_varying_name = "pnn50"
    elif indexname == "mrrii_li":
        time_varying_index = time_varying.rri_mean
        time_varying_name = "mrrii"
    elif indexname == "mhri_li":
        time_varying_index = time_varying.hr_mean
        time_varying_name = "mhri"

    segment_interval = time_varying.segment_interval
    results = {'time_varying_index': zip(segment_interval, time_varying_index),
            'time_varying_name': time_varying_name}
    return HttpResponse(json.dumps(results),
        content_type="application/json")

def get_file_information(f):
    for chunk in f.chunks():
        rri = chunk
    rri = rri.split("\r\n")
    rri = [float(rri) for rri in rri if rri]
    return  rri

def split_psd_classes(freq_domain):
    fxx, pxx = freq_domain.fxx, freq_domain.pxx
    vlf_range = freq_domain.vlf_range
    lf_range = freq_domain.lf_range
    hf_range = freq_domain.hf_range
    freq_res = fxx[1] - fxx[0]
    fxx_vlf = fxx[np.where(np.logical_and(fxx >= (vlf_range[0] - freq_res),
        fxx <= vlf_range[1]))]
    pxx_vlf = pxx[np.where(np.logical_and(fxx >= (vlf_range[0] - freq_res),
        fxx <= vlf_range[1]))]
    fxx_lf = fxx[np.where(np.logical_and(fxx >= lf_range[0],
        fxx <= lf_range[1]))]
    pxx_lf = pxx[np.where(np.logical_and(fxx >= lf_range[0],
        fxx <= lf_range[1]))]
    fxx_hf = fxx[np.where(np.logical_and(fxx >= (hf_range[0] - freq_res),
        fxx <= (hf_range[1] + freq_res)))]
    pxx_hf = pxx[np.where(np.logical_and(fxx >= (hf_range[0] - freq_res),
        fxx <= (hf_range[1] + freq_res)))]

    return [zip(fxx_vlf, pxx_vlf), zip(fxx_lf, pxx_lf), zip(fxx_hf, pxx_hf)]

