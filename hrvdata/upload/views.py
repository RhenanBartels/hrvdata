from django.shortcuts import render, redirect

from .forms import FileForm, read_rri_from_django
from .models import Tachogram, Settings

import hrv
#TODO: check type of uploaded and save it to database. When clicked in filelist
#will be easier to open file.
def index(request):
    template = "uploadindex.html"
    file_form = FileForm(request.POST or None)
    context = {'fileform': file_form}
    if request.method == "POST":
        user = request.user
        file_form = FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            #For beta version each user can only uplod 5 files,
            number_of_files = Tachogram.objects.filter(owner=user).count()
            if number_of_files < 10:
                file_name = prepare_filename(request.FILES['rri_data'].name)
                #Check if file already exists
                if _file_exists(user, file_name):
                    file_form.add_error("rri_data", "You have already uploaded a file with this name.")
                    context = {'fileform': file_form}
                    return render(request, template, context)
                data = file_form.cleaned_data
                new_file = Tachogram(owner=user, filename=file_name,
                        rri=data['rri_data'])
                new_file.save()
                #Save the default value for settings
                save_signal_settings(request.FILES['rri_data'], new_file)
                return redirect('/')
            else:
                file_form.add_error("rri_data", "You have already uploaded 10 files.")
                context = {'fileform': file_form}
                return render(request, template, context)
        else:
            context = {'fileform': file_form}
            return render(request, template, context)
    return render(request, template, context)


def prepare_filename(file_name):
    return file_name.split(".txt")[0] if file_name.endswith(".txt") else \
            file_name.split(".hrm")[0]

def _file_exists(user, filename):
    return Tachogram.objects.filter(owner=user, filename=filename).exists()

def save_signal_settings(signal, signal_db_object):
    """
    Persists the initial values for the settings for the uploaded signal
    """
    #TODO: set overlap size of sp and tf to zero. ForeignKey is wrong. Fix it
    #Return to the bof.
    signal.seek(0)
    rri = read_rri_from_django(signal)
    rri_time = hrv._create_time_array(rri)
    #Save as the maximum length for this signal.
    time_length = rri_time[-1]
    #Check if the signal has at least 30 seconds for time varying analysis
    tv_segment_size = 0 if rri_time[-1] < 30 else 30
    #Check if the signal has at least 256 points for spectral analysis
    resamp_freq = 4 #Default for 4Hz
    rri_time_interp = hrv._create_time_interp_array(rri, resamp_freq)
    sp_seg_size = 0 if len(rri_time_interp) < 256 else 256
    #Check if the signal has at least 256 points for time frequency analysis
    tf_seg_size = 0 if len(rri_time_interp) < 512 else 512
    tf_overlap_size = 0 if len(rri_time_interp) < 512 else 512
    new_settings = Settings(signal=signal_db_object, end_signal=time_length,
            tv_segment_size=tv_segment_size, sp_segment_size=sp_seg_size,
            tf_segment_size=tf_seg_size)
    new_settings.save()
