from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['fname']) < 3:
            errors["fname"] = "User First Name should be at least 6 characters"
        if len(postData['lname']) < 3:
            errors["lname"] = "User Last Name should be at least 6 characters"
            
        if postData['bdate'] == "":
            errors['bdate'] = "Please Enter a Valid Date!"
        else:
            userbirthdate = datetime.strptime(postData['bdate'],'%Y-%m-%d')
            if datetime.today() < userbirthdate:
                errors["bdate"] = "User's Birthday must be in the past!"
            elif ((datetime.today().year)-userbirthdate.year)<15:
                errors['bdate'] = "You are young to sign up here!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['useremail']):      
            errors['useremail'] = "Invalid email address!"
        if len(User.objects.filter(email_address = postData['useremail'])) > 0:
            errors["useremail"] = "Email address exist!"
            
        if len(postData['inputpass']) < 8 :
            errors['inputpass'] = "Password is Weak, Choose Another Please!"
        if postData['inputpass'] != postData['confirminputpass']:
            errors['confirminputpass'] = "Password does not match!"
        return errors
    
    def login_validator(self, postData):
        errors ={}
        logged_user=User.objects.filter(email_address=postData['useremail'])
        if logged_user:
            user=logged_user[0]
        else:
            errors['useremail']='Email Not Found In DataBase. Please register.'
            return errors
        if bcrypt.checkpw(postData['inputpass'].encode(), user.password.encode()):
            return errors
        else:
            errors['inputpass']='Password does not match Email.Try Again! :).'
            return errors

class EventManager(models.Manager):
    def event_basic_validator(self,postData):
        errors = {}
        if len(postData['title']) < 5:
            errors['title']="Please :) Add a Title!."
        if len(postData['desc'])<10:
            errors['desc']="Description Must Be More Than 10 Characters."
        if postData['year'] > '2023' :
            errors['year']="Please Enter a Valid Year"
        if len(postData['ylink']) < 10:
            errors['ylink']="Invalid Link"
        return errors
    
    
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    dob = models.DateField()
    email_address = models.EmailField()
    password = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    ## Defining the function that will create the user in the database:
    def new_user(first_name,last_name,dob,email_address,password):
        return User.objects.create(first_name=first_name,last_name=last_name,dob=dob,email_address=email_address,password=password)
    def user_in_account(id):
        return User.objects.get(id=id)
    
class Event(models.Model):
    title = models.CharField(max_length=45)
    desc = models.TextField()
    year = models.IntegerField()
    link = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="uploded_events",on_delete=models.CASCADE)
    user_that_fav = models.ManyToManyField(User, related_name="fav_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
    
    def new_event(title,desc,year,link,uploaded_by):
        return Event.objects.create(title=title, desc=desc,year=year,link=link,uploaded_by=uploaded_by)
    def one_event(id):
        return Event.objects.get(id=id)
    
    def update_one(id,title,desc,year,link):
        update1 =Event.objects.get(id=int(id))
        update1.title=title
        update1.desc=desc
        update1.year=year
        update1.link=link
        update1.save()
        
    def delete_event(id):
        event1 = Event.objects.filter(id=int(id))
        event1.delete()
        
    def fav_add_one(userid,evid):
        user1 = User.objects.get(id=int(userid))
        event1 = Event.objects.get(id=int(evid))
        event1.user_that_fav.add(user1)
        
    def unfav_rem_one(userid,evid):
        user1 = User.objects.get(id=int(userid))
        event1 = Event.objects.get(id=int(evid))
        event1.user_that_fav.remove(user1)
    
class Comment(models.Model):
    comment_entry = models.TextField()
    user = models.ForeignKey(User,related_name="user_comments",on_delete=models.CASCADE)
    event = models.ForeignKey(Event,related_name="event_comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def new_cmnt(comment_entry,user,event):
        Comment.objects.create(comment_entry=comment_entry,user=user,event=event)
        
    def delete_cmnt(id):
        cmnt1 = Comment.objects.get(id=int(id))
        cmnt1.delete()