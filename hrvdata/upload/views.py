from django.shortcuts import render, redirect

from .forms import FileForm
from .models import Tachogram

def index(request):
    template = "uploadindex.html"
    file_form = FileForm(request.POST or None)
    context = {'fileform': file_form}
    if request.method == "POST":
        user = request.user
        number_of_files = Tachogram.objects.filter(owner=user).count()
        ##Test if the file already exists
        if number_of_files < 5:
            file_form = FileForm(request.POST, request.FILES)
            if file_form.is_valid():
                data = file_form.cleaned_data
                file_name = prepare_filename(request.FILES['rri_data'].name)
                new_file = Tachogram(owner=user, filename=file_name,
                        rri=data['rri_data'])
                new_file.save()
                return redirect('/')
        else:
            template = 'upload_more_files.html'
            return render(request, template)
    return render(request, template, context)


def prepare_filename(file_name):
    return file_name.split(".txt")[0]
