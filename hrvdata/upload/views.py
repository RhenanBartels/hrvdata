from django.shortcuts import render, redirect

from .forms import FileForm
from .models import Tachogram

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
            if number_of_files < 5:
                file_name = prepare_filename(request.FILES['rri_data'].name)
                #Check if file already exists
                if _file_exists(user, file_name):
                    #TODO: Make a template for more files and for already existing file
                    template = 'upload_more_files.html'
                    return render(request, template)
                data = file_form.cleaned_data
                new_file = Tachogram(owner=user, filename=file_name,
                        rri=data['rri_data'])
                new_file.save()
                return redirect('/')
            else:
                template = 'upload_more_files.html'
                return render(request, template)
        else:
            context = {'fileform': file_form}
            return render(request, template, context)
    return render(request, template, context)


def prepare_filename(file_name):
    return file_name.split(".txt")[0]

def _file_exists(user, filename):
    return Tachogram.objects.filter(owner=user, filename=filename).exists()
