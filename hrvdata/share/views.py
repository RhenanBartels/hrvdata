import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .forms import ShareForm
from upload.models import Tachogram
from .models import SharedFile

def files(request):
    template = 'shareindex.html'
    user = request.user
    #TODO: get all shared files of the current user and create a dict
    #with all user for each file
    shared_users = SharedFile.objects.filter(owner=user)
    #Dict with the shared filenames
    shared_filenames = {}
    for shared_obj in shared_users:
        shared_filenames.setdefault('filename', []).append(shared_obj.filename)
    #Create a dict with list of receivers for each file
    shared_relation = {}
    for shared_obj in shared_users:
        shared_relation.setdefault(shared_obj.filename, []).append(shared_obj.receiver)
    context = {'shared_relation': shared_relation,
            'shared_filenames': shared_filenames}
    return render(request, template, context)

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

#TODO: Check if data is an email and exists in the database.
#If not exists send a error msg over the form (red).
def delete(request):
    if request.is_ajax():
        file_name = request.POST['filename']
        #Remove the shared file
        SharedFile.objects.get(receiver=request.user.email, filename=file_name).delete()
        return HttpResponse('')

def delete_shared(request):
    if request.is_ajax():
        user = request.user
        email = request.POST['email']
        filename = request.POST['filename']
        #Delete shared file
        SharedFile.objects.get(owner=user, receiver=email, filename=filename).delete()
    return HttpResponse('')
