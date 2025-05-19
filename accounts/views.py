from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from items.models import Item
from .models import Detail
from django.core.mail import send_mail
from datetime import date
import datetime
from datetime import datetime,timedelta
from django.utils import timezone  # Ensure this is correct


# Create your views here.
def login(request):
    if request.method == 'POST':
        uname = request.POST.get('un','')
        pass1 = request.POST.get('pa','')
        user = auth.authenticate(username=uname,password=pass1)

        if user == None:
            messages.info(request,"invalid username/password")
            return redirect('login')
        else:
            auth.login(request,user)
            return redirect("home")
            
    else:
        return render(request,'login.html')

"""
def register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        name = request.POST['name']
        mail = request.POST['email']
        p1 = request.POST['p1']
        p2 = request.POST['p2']

        contact = request.POST['contact']
        if p1 == p2:
            if User.objects.filter(email=mail).exists():
                messages.info(request,"Already an User with this Email")
                return redirect('register')
            elif User.objects.filter(username=name).exists():
                messages.info(request,"Already an User with this Username")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=fname,last_name=lname,email=mail,password=p1,username=name)
                user.save()
                obj = Detail(username=name,contact=contact)
                obj.save()
                subject = "Online Bidding"  
                msg     = "Congratulations you are registered successfully."
                to      = mail  
                res     = send_mail(subject, msg, "kishorepandiri2244@gmail.com", [to])
                if res == 1:
                    return redirect('/')
                else:
                    messages.info(request,"Some thing is wrong")
                    return redirect('register')
        else:
            messages.info(request,"Password does not match")
            return redirect('register')
    else:
        return render(request,'register.html')
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib.auth.models import User
from .models import Detail

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        name = request.POST['name']
        mail = request.POST['email']
        p1 = request.POST['p1']
        p2 = request.POST['p2']
        contact = request.POST['contact']

        if p1 == p2:
            if User.objects.filter(email=mail).exists():
                messages.info(request, "Already a User with this Email")
                return redirect('register')
            elif User.objects.filter(username=name).exists():
                messages.info(request, "Already a User with this Username")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=fname, last_name=lname, email=mail, password=p1, username=name)
                user.save()
                obj = Detail(username=name, contact=contact)
                obj.save()
                subject = "Online Bidding"
                msg = "Congratulations you are registered successfully."
                to = mail
                try:
                    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
                    if res == 1:
                        return redirect('/')
                    else:
                        messages.info(request, "Something went wrong")
                        return redirect('register')
                except BadHeaderError:
                    messages.info(request, "Invalid header found.")
                    return redirect('register')
                except Exception as e:
                    messages.info(request, f"An error occurred: {str(e)}")
                    return redirect('register')
        else:
            messages.info(request, "Passwords do not match")
            return redirect('register')
    else:
        return render(request, 'register.html')
    
    
"""
@login_required(login_url='login')
def sendMailTowinners(request):
    today = date.today()
    yesterday = today - datetime.timedelta(days=1) 
    item = Item.objects.filter(start_date=yesterday).filter(sold="sold").filter(sendwinmail="unsended")
    for i in item :
        # print("1")
        try:
            # print("2")
            winnerid = i.highest_bidder
            # print(winnerid)
            user_obj = User.objects.get(id=winnerid)
            winnermail = user_obj.email


            winuser = user_obj.username
            # wincon=""            
            #-----------------------------------------------------------
            obj = Detail.objects.get(username=winuser)
            wincon = obj.contact
            # print(wincon)
            
            itemmail = i.ownermail
            itemUserobj = User.objects.get(email=itemmail)
            itemuser = itemUserobj.username

            obj2 = Detail.objects.get(username=itemuser)
            itemcon = obj2.contact
            # print(itemcon)
            # print(winnermail)
            #-------------------------------------------------------------
            #To winner
            #send ownwer contact
            subject = "Online Bidding"  
            msg     = "Congratulations you are winner of item"+i.name+"'s, Seller Email-id is "+i.ownermail+"  contact him for further informations. phone no = "+itemcon+" Thank You :)"
            to      = winnermail  
            res     = send_mail(subject, msg, "kishorepandiri2244@gmail.com", [to])
            if res ==1:
                print ("mail sended to winner")
            else:
                print("something wrong for sending mail to winner")
            
            #To owner
            #send winner contact
            subject = "Online Bidding"  
            msg     = "Congratulations your item "+i.name+"'s higgest bidder's email id is "+winnermail+" ,  contact him for further informations. phone no = "+wincon +" Thank You :)"
            to      = i.ownermail  
            res     = send_mail(subject, msg, "kishorepandiri2244@gmail.com", [to])
            if res ==1:
                print ("mail sended to seller")
            else:
                print("something wrong for sending mail to seller")
            i.sendwinmail="sended"
            i.save()
        except:
            pass

"""
"""

@login_required(login_url='login')
def sendMailTowinners(request):
    #now = datetime.now()  # Get the current time
    local_time = timezone.localtime(timezone.now())
    now = local_time   # Get the current time
    items = Item.objects.filter(end_date__lt=now, sold="sold", sendwinmail="unsended")  # Get items that have ended

    for item in items:
        try:
            winnerid = item.highest_bidder
            user_obj = User.objects.get(id=winnerid)
            winnermail = user_obj.email
            winuser = user_obj.username
            print(winnerid)
            
            # Get winner's contact details
            winner_detail = Detail.objects.get(username=winuser)
            wincon = winner_detail.contact
            
            # Get owner's contact details
            itemmail = item.ownermail
            owner_user = User.objects.get(email=itemmail)
            owner_username = owner_user.username
            owner_detail = Detail.objects.get(username=owner_username)
            itemcon = owner_detail.contact
            
            # To winner
            subject = "Online Bidding"
            msg = f"Congratulations, you are the winner of item {item.name}. Seller Email-id is {item.ownermail}. Contact him for further information. Phone no = {itemcon}. Thank You :)"
            res = send_mail(subject, msg, "kishorepandiri2244@gmail.com", [winnermail])
            if res == 1:
                print("Mail sent to winner")
            else:
                print("Something went wrong while sending mail to winner")
            
            # To owner
            subject = "Online Bidding"
            msg = f"Congratulations, your item {item.name}'s highest bidder's email id is {winnermail}. Contact him for further information. Phone no = {wincon}. Thank You :)"
            res = send_mail(subject, msg, "kishorepandiri2244@gmail.com", [item.ownermail])
            if res == 1:
                print("Mail sent to seller")
            else:
                print("Something went wrong while sending mail to seller")
            
            # Mark the email as sent
            item.sendwinmail = "sended"
            item.save()
        except Exception as e:
            print(f"Error sending mail: {e}") """

import logging

# Set up logging
logger = logging.getLogger(__name__)

@login_required(login_url='login')
def sendMailTowinners(request):
    now = timezone.now()  # Get the current time
    items = Item.objects.filter(end_date__lt=now, sold="sold", sendwinmail="unsended")  # Get items that have ended

    for item in items:
        try:
            winnerid = item.highest_bidder
            user_obj = User.objects.get(id=winnerid)
            winnermail = user_obj.email
            winuser = user_obj.username
            
            # Get winner's contact details
            winner_detail = Detail.objects.get(username=winuser)
            wincon = winner_detail.contact
            
            # Get owner's contact details
            itemmail = item.ownermail
            owner_user = User.objects.get(email=itemmail)
            owner_username = owner_user.username
            owner_detail = Detail.objects.get(username=owner_username)
            itemcon = owner_detail.contact
            
            # To winner
            winner_subject = "Online Bidding"
            winner_msg = (
                f"Congratulations, you are the winner of item {item.name}. "
                f"Seller Email-id is {item.ownermail}. Contact him for further information. "
                f"Phone no = {itemcon}. Thank You :)"
            )
            winner_res = send_mail(winner_subject, winner_msg, "kishorepandiri2244@gmail.com", [winnermail])
            if winner_res > 0:
                print("Mail sent to winner")
            else:
                print("Something went wrong while sending mail to winner")
            
            # To owner
            owner_subject = "Online Bidding"
            owner_msg = (
                f"Congratulations, your item {item.name}'s highest bidder's email id is {winnermail}. "
                f"Contact him for further information. Phone no = {wincon}. Thank You :)"
            )
            owner_res = send_mail(owner_subject, owner_msg, "kishorepandiri2244@gmail.com", [item.ownermail])
            if owner_res > 0:
                print("Mail sent to seller")
            else:
                print("Something went wrong while sending mail to seller")
            
            # Mark the email as sent
            item.sendwinmail = "sended"
            item.save()
        except Exception as e:
            logger.error(f"Error sending mail for item {item.id}: {e}")
"""

@login_required(login_url='login')
def pastConfigurations(request):
    # cuser =request.user
    # cmail = cuser.email
    # item = Item.objects.filter(ownermail=cmail)
    item = Item.objects.all()
    for i in item:
        try:
            hb = i.highest_bidder
            if hb is not None:
                i.sold="sold"
                i.save()
            else:
                i.sold="unsold"
                i.save()
        except:
            pass
    # print("hy")

@login_required(login_url='login')
def home(request):
    items = Item.objects.all()
    today = date.today()
    yesterday = today - datetime.timedelta(days=1) 
    # print(today)
    # print(yesterday)    
    for i in items:
        # print (i.start_date)
        if(today > i.start_date):
            i.status = "past"
            # print("past")
        if(today < i.start_date):
            i.status="future"
            # print("future")
        if(today == i.start_date):
            i.status="live"
            # print("live")
        i.save()
        # print("-------")
    pastConfigurations(request)
    sendMailTowinners(request)
    items = Item.objects.filter(status="live")
    return render(request,"home.html",{'items':items})
"""
@login_required(login_url='login')
def pastConfigurations(request):
    items = Item.objects.all()
    for item in items:
        try:
            if item.highest_bidder is not None:
                item.sold = "sold"
            else:
                item.sold = "unsold"
            item.save()
        except Exception as e:
            print(f"Error updating item status: {e}")

@login_required(login_url='login')
def home(request):
    items = Item.objects.all() 
    from django.utils import timezone

    local_time = timezone.localtime(timezone.now())
    now = local_time   # Get the current time

    for item in items:
        # Check if end_date is None
        if item.end_date is None:
            # Handle the case where end_date is None
            item.status = "future"  # or set it to a default status
            item.save()
            continue  # Skip to the next item

        # Now we can safely compare
        if now < item.start_date:  # Check if the auction has ended
            item.status = "future"
        elif item.start_date < now <= item.end_date:
            item.status = "live"
       # elif now > item.end_date :
            #item.status = "past"
        else:
            item.status = "past"
        item.save()

    pastConfigurations(request)
    sendMailTowinners(request)
    items = Item.objects.filter(status="live")
    return render(request, "home.html", {'items':items})

    
def logout(request):
    auth.logout(request)
    return redirect("login") 

def ilogout(request):
    auth.logout(request)
    return redirect("login") 

@login_required(login_url='login')
def myprofile(request):
    bidder = request.user
    # item_obj = Item.objects.get(highest_bidder=bidder.id)
    details = bidder   
    cuname = details.username
    # print(cuname)
    # ,"item_obj":item_obj
    obj = Detail.objects.filter(username=cuname)
    contact=""
    for i in obj:
        contact = i.contact
    return render(request,"myprofile.html",{"details":details,"contact":contact})

@login_required(login_url='login')
def log(request):
    cuser =request.user
    cmail = cuser.email
    cid = cuser.id
    item_obj = Item.objects.filter(highest_bidder=cid)

    biddeditem = item_obj
    # item = Item.objects.filter(ownermail=cmail)
    pitem = Item.objects.filter(ownermail=cmail).filter(status="past") 
    litem = Item.objects.filter(ownermail=cmail).filter(status="live") 
    fitem = Item.objects.filter(ownermail=cmail).filter(status="future") 
    return render(request,"log.html",{'pitem':pitem,'litem':litem,'fitem':fitem,"biddeditem":biddeditem})

@login_required(login_url='login')
def future(request):
    items = Item.objects.filter(status="future")
    return render(request,"future.html",{"items":items})
