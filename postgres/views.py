# Create your views here.

from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.context_processors import csrf

from postgres.forms import *
from postgres.models import *

def index(request):
    return render_to_response('postgres/index.html', context_instance=RequestContext(request))

def backup(request):
    c = {}
    c.update(csrf(request))
    state = ""
    c["backupForm"] = BackupForm()
    if request.POST:
        if request.POST["button"].lower() == "save":
            form = BackupForm(request.POST)
            if form.is_valid():            
                bkp = Backup()
                bkp.description = form.cleaned_data['description']
                bkp.user_id = request.user.id
                bkp.save()
                state = "Saved"
            else:
                state = str(form.errors) #"Invalid Data"
        elif request.POST["button"].lower() == "restore":
            print "restoring",Backup.objects.filter(id=request.POST["backups_id"])[0]
    c["state"] = state
    return render_to_response('postgres/backup.html', c, context_instance=RequestContext(request))


