import json

import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from upload.models import Tachogram, Settings
from share.models import SharedFile
from analysis.models import Comment
from .forms import TachogramSettingsForm, TimeVaryingSettingsForm

import hrv
from hrvtools.hrv import TimeDomain, TimeVarying, FrequencyDomain

#TODO: use new hrv module intalled with pip. Remove hrvtools library
#TODO: Make the comments different from shared files.
def index(request, filename):
    #Instanciate tachogram settings form
    tachogram_settings_form = TachogramSettingsForm()
    time_varying_settings_form = TimeVaryingSettingsForm()
    user = request.user
    rri_file = Tachogram.objects.get(owner=user, filename=filename)
    #Get the parameters in the database
    settings = Settings.objects.get(signal=rri_file)
    rri = get_file_information(rri_file)
    time_domain= TimeDomain(rri)
    frequency_domain = FrequencyDomain(rri)
    #TODO: Use the information from the database to calculate the indices
    segment = 256
    overlap = 128
    frequency_domain.calculate(segment, overlap)
    time_domain.calculate()
    #TODO: create a function to create the results context

    #Load comments for this file
    comments = Comment.objects.filter(signal=rri_file)

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
            "filename": filename,
            "comments": comments,
            "tachogramsettingsform": tachogram_settings_form,
            "timevaryingsettingsform": time_varying_settings_form}
    if request.is_ajax():
        segment_size = settings.tv_segment_size
        overlap_size = settings.tv_overlap_size
        time_varying = TimeVarying(rri, segment_size, overlap_size)
        time_varying.calculate()
        rri = time_domain.rri
        rri_time = time_varying.rri_time
        rri_result = zip(rri_time, rri)
        rmssdi = time_varying.rmssd
        segment_interval = time_varying.segment_interval
        rmssdi_result = zip(segment_interval, rmssdi)
        vlf_psd, lf_psd, hf_psd = split_psd_classes(frequency_domain.fxx, frequency_domain.pxx)
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
    #Get the settings in the database
    settings = Settings.objects.get(signal=rri_file)
    segment_size = settings.tv_segment_size
    overlap_size = settings.tv_overlap_size
    rri = get_file_information(rri_file)
    time_varying = TimeVarying(rri, segment_size, overlap_size)
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

def settings(request, filename):
    if request.is_ajax():
        #Get the RRi
        user = request.user
        rri_file = Tachogram.objects.get(owner=user, filename=filename)
        rri = get_file_information(rri_file)
        method = request.POST['method']
        #TODO: Create function to do everything for each method. Instead of
        #letting the code here directly.
        if method == 'timevarying':
            segment_size = int(request.POST['segmentsize'])
            overlap_size = int(request.POST['overlapsize'])
            error_msg = validate_timevarying_parameters(rri, segment_size,
                    overlap_size)
            time_varying = hrv.time_varying(rri, segment_size, overlap_size)
            #Save the parameters in the databse
            settings = Settings.objects.get(signal=rri_file)
            settings.tv_segment_size = segment_size
            settings.tv_overlap_size = overlap_size
            settings.save()
            results = {'time_varying_index':
                    zip(time_varying[0], time_varying[1]), 'time_varying_name':
                    'rmssd'}
        return HttpResponse(json.dumps(results),
                content_type='application/json')

def shared(request, filename):
    user = request.user
    owner = SharedFile.objects.get(receiver=user.email,
            filename=filename).owner
    rri_file = Tachogram.objects.get(owner=owner, filename=filename)
    comments = Comment.objects.filter(signal=rri_file)
    rri = get_file_information(rri_file)
    time_domain = hrv.time_domain(rri)
    frequency_domain = hrv.frequency_domain(rri)
    results = {'rmssd': round(time_domain[0], 2),
            'sdnn': round(time_domain[1], 2),
            'pnn50':round(time_domain[2], 2),
            'mrri':round(time_domain[3], 2),
            'mhr': round(time_domain[4], 2),
            "totalpower": round(frequency_domain[1][0], 2),
            "vlf": round(frequency_domain[1][1], 2),
            "lf": round(frequency_domain[1][2],2),
            "hf":round(frequency_domain[1][3], 2),
            "lfhf": round(frequency_domain[1][4], 2),
            "lfnu": round(frequency_domain[1][5], 2),
            "hfnu": round(frequency_domain[1][6], 2),
            "filename": filename,
            "comments": comments}
    if request.is_ajax():
        time_rri = hrv._create_time_array(rri)
        rri_result = zip(time_rri, rri)
        time_varying = hrv.time_varying(rri)
        rmssdi_result = zip(time_varying[0], time_varying[1])
        fxx, pxx = frequency_domain[0]
        psd = zip(fxx, pxx)
        vlf_psd, lf_psd, hf_psd = split_psd_classes(fxx, pxx)
        results = {'rri': rri_result, "rmssdi": rmssdi_result,
                "vlfpsd": vlf_psd, "lfpsd": lf_psd, "hfpsd": hf_psd,
                "psd": psd, "time_varying_index": "rmssd"}
        return HttpResponse(json.dumps(results), content_type="application/json")
    return render(request, "index.html", results)

def change_tv_index_shared():
    pass

#TODO: make a query with all comments of the current user and pass as context
#to enable edition and deletion
def shared_comment(request, filename):
    if request.is_ajax():
        text = request.POST["text"]
        user = request.user
        owner = SharedFile.objects.get(receiver=user.email,
                filename=filename).owner
        rri_file = Tachogram.objects.get(owner=owner, filename=filename)
        save_comment(rri_file, text, user)
        comment_context = {"user": user.username}
        return HttpResponse(json.dumps(comment_context),
            content_type="application/json")

def comment(request, filename):
    if request.is_ajax():
        text = request.POST["text"]
        user = request.user
        rri_file = Tachogram.objects.get(owner=user, filename=filename)
        save_comment(rri_file, text, user)
        comment_context = {"user": user.username}
        return HttpResponse(json.dumps(comment_context),
            content_type="application/json")

def save_comment(rri_file, text, user):
    new_comment = Comment()
    new_comment.author = user
    new_comment.signal = rri_file
    new_comment.text = text
    new_comment.save()

def get_file_information(f):
    #Check if it is possible to read as a text file.
    try:
        rri = [float(value.strip()) for value in
                signal.readlines() if value.strip()]
    except:
        import re
        for chunk in f.rri.chunks():
            file_content = chunk
        rri = [float(value.strip()) for value in
                re.findall("\d{3,4}\\r\\n", file_content)]
        #Remove empty values and zeros.
        rri = [rri for rri in rri if rri]
    return rri

#TODO: acceot as arguments the frequency boundaries and put the default values
def split_psd_classes(fxx, pxx, vlf_range=(0.003, 0.05),
        lf_range=(0.04, 0.15), hf_range=(0.15, 0.4)):
    #Make sure that the PSD bands are adjacents
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

def validate_timevarying_parameters(rri, segment_size, overlap_size):
    if overlap_size >= segment_size:
        return 'Overlap size can not be bigger than Segment size'
