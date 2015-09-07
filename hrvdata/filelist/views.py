from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from upload.models import Tachogram

@login_required
def index(request):
    user = request.user
    data = Tachogram.objects.filter(owner=user)
    context = {'data': data}
    return render(request, "filelistindex.html", context)

