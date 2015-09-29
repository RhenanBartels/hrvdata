import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .forms import ShareForm
from upload.models import Tachogram
from .models import SharedFile

def index(request):
    form = ShareForm(request.POST or None)
    if request.is_ajax():
        if form.is_valid():
            useremail = form.clean_usermail()
            #Check if there is a user if this email
            try:
                user_exist = User.objects.get(email=useremail)
            except ObjectDoesNotExist:
                user_exist = None
            if user_exist:
                #TODO: Check if this file is already shared with one user.
                #TODO: Refoctor this view to make the if-else logic cleaner
                # Check if the user is not sharing a file with himself.
                if not useremail == request.user.email:
                    file_name = request.POST['filename']
                    new_share = SharedFile(owner=request.user, receiver=useremail,
                            filename=file_name)
                    new_share.save()
                    return HttpResponse(json.dumps({'log': 'Success'}),
                            content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'log': 'sameuser'}),
                            content_type='application/json')
            else:
                return HttpResponse(json.dumps({'log': 'notuser'}),
                        content_type='application/json')
        else:
            return HttpResponse(json.dumps({'log': 'notvalid'}),
                    content_type='application/json')

def delete(request):
    if request.is_ajax():
        file_name = request.POST['filename']
        #Remove the shared file
        SharedFile.objects.get(receiver=request.user.email, filename=file_name).delete()
        return HttpResponse('')


