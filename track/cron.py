from .models import *
from django.http import HttpResponse
import datetime
from datetime import timedelta
from django.shortcuts import render, redirect
from django.db.models import Q

# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def bulk_status():
    sample = Bulk_Order.objects.filter(status1="Accept").exclude(gre_date=None)
    for sam in sample:
        gre = Griege_Status.objects.get(bulk=sam)
        pri = Bulk_Printed.objects.get(bulk=sam)
        che = Fabric_Cheking.objects.get(bulk=sam)
        dis = Dispatch_Detail.objects.get(bulk=sam)
        if gre.g_date:
            if sam.gre_date > gre.g_date:
                sam.time_status = "On Time"
                sam.save()
            else:
                sample.time_status = "Delayed"
                sam.save()
        else:
            if sam.gre_date > datetime.date.today():
                sam.time_status = "On Time"
                sam.save()
            else:
                sam.time_status = "Delayed"
                sam.save()
            
        if pri.pr_date:
            if sam.print_date > pri.pr_date:
                sam.time_status = "On Time"
                sam.save()
            else:
                sam.time_status = "Delayed"
                sam.save()
        else:
            if gre.g_date:
                if sam.print_date > datetime.date.today():
                    sam.time_status = "On Time"
                    sam.save()
                else:
                    sam.time_status = "Delayed"
                    sam.save()
                
        if che.f_date:
            if sam.checking_date > che.f_date:
                sam.time_status = "On Time"
                sam.save()
            else:
                sam.time_status = "Delayed"
                sam.save()
        else:
            if pri.pr_date:
                if sam.checking_date > datetime.date.today():
                    sam.time_status = "On Time"
                    sam.save()
                else:
                    sam.time_status = "Delayed"
                    sam.save()
        
        if dis.d_date:
            if sam.dispatch_date > dis.d_date:
                sam.time_status = "On Time"
                sam.save()
            else:
                sam.time_status = "Delayed"
                sam.save()
        else:
            if che.f_date:
                if sam.dispatch_date > datetime.date.today():
                    sam.time_status = "On Time"
                    sam.save()
                else:
                    sam.time_status = "Delayed"
                    sam.save()

def sampling_status():
    sample = Sampling.objects.all()
    for sample in sample:
        if sample.count == 0:
            f_date = sample.sent_on
            if f_date:
                if f_date <= sample.first:
                    sample.time_status = "On Time"
                else:
                    sample.time_status = "Delay"
            else:
                if datetime.date.today() <= sample.first:
                    sample.time_status = "On Time"
                else:
                    sample.time_status = "Delay"
            
        if sample.count == 1:
            f_date = sample.sent_on
            if f_date <= sample.second or datetime.date.today() <= sample.second:
                sample.time_status = "On Time"
            else:
                sample.time_status = "Delay"
        
        if sample.count == 2:
            f_date = sample.sent_on
            if f_date <= sample.third or datetime.date.today() <= sample.third:
                sample.time_status = "On Time"
            else:
                sample.time_status = "Delay"
        sample.save()
        
def Send_Mail_daily_sample():
    tod = datetime.date.today()
    #yes = tod - timedelta(days=1)
    #sample = Courier_Detail.objects.filter(buyer=None)
    data = Search_for_date.objects.all()
    buyer = Buyer.objects.all()
    for i in buyer:
        to = i.user.email
        to1 = i.additional_email
        to2 = to1.split(",")
        to2.append(to)
        from_email = settings.EMAIL_HOST_USER
        sub = "Dispatch Detail"
        msg = EmailMultiAlternatives(sub, '', from_email, to2)
        delv = Courier_Detail.objects.filter(Q(c_date=tod) & Q(buyer=i))
        d ={'name': i.user.username, 'title': 'Dispatch Detail', 'del': len(delv), 'prod': delv, 'task': 'Dispatch_Rem', 'date': tod}
        html = get_template('email.html').render(d)
        msg.attach_alternative(html, 'text/html')
        if len(delv) > 0 :
            msg.send()
    

def Send_Mail_daily_approval():
    buyer = Buyer.objects.all()
    for i in buyer:
        to = i.user.email
        to1 = i.additional_email
        to2 = to1.split(",")
        to2.append(to)
        from_email = settings.EMAIL_HOST_USER
        sub = "Pending Approval Detail"
        msg = EmailMultiAlternatives(sub, '', from_email, to2)
        delv = Sampling.objects.filter(c_status__icontains ="approval", buyer=i)
        d ={'name': i.user.username, 'title': 'Pending Approval Detail', 'del': len(delv), 'prod': delv, 'task': 'Approval_Rem'}
        html = get_template('email.html').render(d)
        msg.attach_alternative(html, 'text/html')
        if len(delv) > 0 :
            msg.send()
            
def Send_Mail_Pending_Griege():
    buyer= Supplier.objects.all()
    for i in buyer:
        to = i.user.email
        to1 = i.additional_email
        to2=[]
        if to1 and ("," in to1):
            to2 = to1.split(",")
        to2.append(to)
        from_email = settings.EMAIL_HOST_USER
        sub = "Pending Greige Detail"
        msg = EmailMultiAlternatives(sub, '', from_email, to2)
        date1 = datetime.date.today()
        delv = Griege_Status.objects.filter(bulk__gre_date__lte = date1,bulk__sup=i)
        d ={'name': i.user.username, 'title': 'Pending Greige Detail', 'del': delv.count(), 'prod': delv, 'task': 'Pending Greige'}
        html = get_template('email.html').render(d)
        msg.attach_alternative(html, 'text/html')
        if len(delv) > 0 :
            msg.send()

def Send_Mail_Latest_Dispatch():
    buyer= Buyer.objects.all()
    for i in buyer:
        delv = Bulk_Order.objects.filter(buy=i,status1="Accept")
        to = i.user.email
        to1 = i.additional_email
        to2=[]
        if to1 and ("," in to1):
            to2 = to1.split(",")
        to2.append(to)
        from_email = settings.EMAIL_HOST_USER
        sub = "Latest Dispatch Detail"
        msg = EmailMultiAlternatives(sub, '', from_email, to2)
        date1 = datetime.date.today() - timedelta(days=1)
        delv = Bulk_Order.objects.filter(buy=i)
        d ={'name': i.user.username, 'title': 'Latest Dispatch Detail', 'del': delv.count(), 'prod': delv, 'task': 'Latest Dispatch','date1':date1}
        html = get_template('email.html').render(d)
        msg.attach_alternative(html, 'text/html')
        if len(delv) > 0 :
            msg.send()
            
    buyer1= GMT_Vendor.objects.all()
    for i in buyer1:
        delv = Bulk_Order.objects.filter(gmt_vendor=i.user.username,status1="Accept")
        to = i.user.email
        to2=[]
        to2.append(to)
        from_email = settings.EMAIL_HOST_USER
        sub = "Latest Dispatch Detail"
        msg = EmailMultiAlternatives(sub, '', from_email, to2)
        date1 = datetime.date.today() - timedelta(days=1)
        delv = Bulk_Order.objects.filter(buy=i)
        d ={'name': i.user.username, 'title': 'Latest Dispatch Detail', 'del': delv.count(), 'prod': delv, 'task': 'Latest Dispatch','date1':date1}
        html = get_template('email.html').render(d)
        msg.attach_alternative(html, 'text/html')
        if len(delv) > 0 :
            msg.send()
            
            
def DevelopementTime():
    nexmo = Sampling.objects.all()
    for i in nexmo:
        # i.time_in_develop = 0
        # i.time_in_approve = 0
        # i.save()
        cour = Courier_Detail.objects.filter(sample = i)
        if cour:
            count = 0
            latest = None
            for j in cour:
                if i.count == count:
                    d1 = j.rep_date
                    d2 = j.sent_on
                    d4 = d1 - d2
                    d3 = i.time_in_develop
                    i.time_in_develop = int(d3) + int(d4.days)
                    i.save()
                    break
                else:
                    if count == 0:
                        d1 = i.dos
                        d2 = j.sent_on
                        d4 = d2 - d1
                        d3 = i.time_in_develop
                        i.time_in_develop = int(d3) + int(d4.days)
                        i.save()
                        latest = j
                    else:
                        if latest.rep_date:
                            d1 = latest.rep_date
                            d2 = j.sent_on
                            d4 = d2 - d1
                            d3 = i.time_in_develop
                            i.time_in_develop = int(d3) + int(d4.days)
                            i.save()
                            latest = j
                        else:
                            d1 = datetime.date.today()
                            d2 = j.sent_on
                            d4 = d2 - d1
                            d3 = i.time_in_develop
                            i.time_in_develop = int(d3) + int(d4.days)
                            i.save()
                            latest = j
                count+=1
                
        else:
            d1 = i.dos
            if d1:
                d2 = datetime.date.today()
                d4 = d2 - d1
                d3 = i.time_in_develop
                i.time_in_develop = int(d3) + int(d4.days)
                i.save()
    
            
            
            
            

