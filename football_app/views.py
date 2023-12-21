from django.shortcuts import render,redirect
from django.contrib import messages
from football_app.models import *


def display_log_reg(request):
    return render (request,'log_reg.html')

# Displaying Home Page after login or register and authenticating user existance:
def display_home(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context={
            'user_in':User.objects.get(id=request.session['id']),
            'allevents':Event.objects.all()
        }
        return render(request,'home.html',context)
    
## Registering a New Account:
def new_sign_up(request):
    ## Checking if there is any validation errors
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        ## Taking the password and hashing it directly:
        password = request.POST['inputpass']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user1 = User.new_user(first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        dob = request.POST['bdate'],
        email_address = request.POST['useremail'],
        password = pw_hash)
        
        request.session['id'] = user1.id
        request.session['username'] = user1.first_name
        
        return redirect('/success')
    
def new_sign_in(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=User.objects.filter(email_address=request.POST['useremail'])
            logged_user=user[0]
            request.session['id']=logged_user.id
            request.session['username'] = logged_user.first_name
        
            return redirect('/success')
    else:
        redirect('/')
        
    ## This is to logout and sign the user out from the account:
def destroy_session(request):
    request.session.flush()
    return redirect('/')

def add_new_event(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request,'add.html')
    
def create_event(request):
    if request.method =='POST':
        errors = Event.objects.event_basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/success')
        else: 
            user_id=request.session['id']
            event1=Event.new_event(title=request.POST['title'],
            desc=request.POST['desc'],
            year = request.POST['year'],
            link = request.POST['ylink'],
            uploaded_by=User.objects.get(id=user_id))
            
            this_user=User.objects.get(id=user_id)
            eventid=event1.id
            event1.user_that_fav.add(this_user)
            return redirect ('/success')
        
def show_event(request,evid):
    if 'id' not in request.session:
        return redirect('/')
    else:
        uploader = Event.objects.get(id=evid)
        context = {
            'oneevent':Event.one_event(evid),
            'oneuser':User.user_in_account(request.session['id'])
            }
        return render(request,'event_show_page.html',context)
    
def show_edit(request,evid):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
                'oneevent':Event.one_event(evid),
                'oneuser':User.user_in_account(request.session['id'])
            }
        return render(request,'event_edit_page.html',context)
