from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from upload.models import Tachogram

@login_required
def index(request):
    user = request.user
    data = Tachogram.objects.filter(owner=user)
    context = {'data': data}
    return render(request, "filelistindex.html", context)

@login_required
def delete(request):
    user = request.user
    if request.is_ajax():
        filename = request.POST['filename']
        #Delete the selected file.
        Tachogram.objects.get(owner=user, filename=filename).delete()
        return HttpResponse('')



