from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from django.contrib import messages
from django.http import HttpResponse
from .models import *
import datetime
from django.contrib.auth.decorators import login_required
from .decorators import *
from datetime import timedelta
from .forms import *
from django.db.models import Q
to = datetime.date.today()
yes = to - timedelta(days=1)
from django.db.models import Sum,Max
import calendar
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from .utils import *


def Send_Mail(to, name, title, task):
    from_email = settings.EMAIL_HOST_USER
    sub = "Reminder"
    msg = EmailMultiAlternatives(sub, '', from_email, to)
    user = User.objects.get(username=name)
    sup = ""
    if task == "pending_app":
        to = datetime.date.today()
        yes = to - timedelta(days=0)
        delv = Courier_Detail.objects.filter(rep_date=yes)
        d ={'name': name, 'title': title, 'del': len(delv), 'prod': delv, 'task': task, 'date': yes}
        html = get_template('email.html').render(d)
    elif "Dispatch_Rem" in task:
        to = datetime.date.today()
        li1 = task.split('.')
        task = li1[0]
        yes = to - timedelta(days=int(li1[1]))
        buy = Buyer.objects.get(user=user)
        sample = Sampling.objects.filter(buyer=buy).first()
        delv = Courier_Detail.objects.filter(sent_on=yes)
        d ={'name': name, 'title': title, 'del': len(delv), 'prod': delv, 'task': task, 'date': yes}
        html = get_template('email.html').render(d)
    elif "Bulk Dispatched Detail" in task:
        to = datetime.date.today()
        li1 = task.split('.')
        task = li1[0]
        yes = to - timedelta(days=int(li1[1]))
        buy = Supplier.objects.get(user=user)
        delv = Dispatch_Detail.objects.filter(supplier=buy,d_date=yes)
        d ={'name': name, 'title': title, 'del': len(delv), 'prod': delv, 'task': task, 'date': yes}
        html = get_template('email.html').render(d)
    elif task == "Approval_Rem":
        buy = Buyer.objects.get(user=user)
        delv = Sampling.objects.filter(c_status="Under 1st Submit Approval", buyer=buy) | Sampling.objects.filter(c_status="Under 2nd Submit Approval", buyer=buy) | Sampling.objects.filter(buyer=buy,c_status="Under 3rd Submit Approval")| Sampling.objects.filter(buyer=buy,c_status="Under 4th Submit Approval")| Sampling.objects.filter(buyer=buy,c_status="Under 5th Submit Approval")
        d ={'name': name, 'title': title, 'del': len(delv), 'prod': delv, 'task': task}
        html = get_template('email.html').render(d)
    else:
        sup = Supplier.objects.get(user=user)
        delv = Sampling.objects.filter(del_date=None, supplier=sup).exclude(technique = "Adhoc")
        d ={'name': name, 'title': title, 'del': len(delv), 'prod': delv, 'task': task}
        html = get_template('email.html').render(d)
    msg.attach_alternative(html, 'text/html')
    if len(delv) > 0:
        msg.send()


def Home(request):
    error = ""
    try:
        error = get_group(request.user.id)
    except:
        pass
    d = {'error':error}
    return render(request, 'carousel.html',d)


def get_group(user):
    user1 = User.objects.get(id=user)
    try:
        rm = RM.objects.get(user=user1)
        if rm:
            return "pat4"
    except:
        try:
            rm = Buyer.objects.get(user=user1)
            if rm:
                return "pat"
        except:
            try:
                rm = Supplier.objects.get(user=user1)
                if rm:
                    return "pat2"
            except:
                try:
                    rm = GMT_Vendor.objects.get(user=user1)
                    if rm:
                        return "pat3"
                except:
                    return "pat5"

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM','Supplier'])
def Admin_Home(request):
    error = get_group(request.user.id)
    error = get_group(request.user.id)
    terror = ""
    season = Season.objects.all()
    buyer = Buyer.objects.all()
    sampling_summary = sampling_summary_fn(request)
    bulk_summary =bulk_summary_fn(request)
    d ={
         'sampling_summary':sampling_summary,
        'bulk_summary':bulk_summary,
        'season': season,
        'buyer': buyer,
         'terror': terror,
         'error': error,
         }
    return render(request, 'admin_home.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def User_Home(request):
    error = get_group(request.user.id)
    terror = ""
    season = Season.objects.all()
    buyer = Buyer.objects.get(id = request.user.id)
    sampling_summary = sampling_summary_fn(request)
    bulk_summary =bulk_summary_fn(request)
    d ={
         'sampling_summary':sampling_summary,
        'bulk_summary':bulk_summary,
        'season': season,
        'buyer': buyer,
        'terror': terror,
         'error': error,
         }
    return render(request, 'buyer_home.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Supplier_Home(request):
    error = get_group(request.user.id)
    terror = ""
    season = Season.objects.all()
    buyer = Buyer.objects.all()
    sampling_summary = sampling_summary_fn(request)
    bulk_summary =bulk_summary_fn(request)
    d ={
         'sampling_summary':sampling_summary,
        'bulk_summary':bulk_summary,
        'season': season,
        'buyer': buyer,
         'terror': terror,
         'error': error,
         }
    return render(request, 'supplier_home.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['GMT'])
def GMT_Home(request):
    error = get_group(request.user.id)
    ur_sample = 0
    ud_sample = 0
    a_sample = 0
    ua_sample = 0
    t_sample = 0
    t_qty = 0
    d_qty = 0
    p_qty = 0
    u_qty = 0
    o_qty = 0
    de_qty = 0
    t_opt = 0
    d_opt = 0
    p_opt = 0
    u_opt = 0
    o_opt = 0
    de_opt = 0
    terror = ""
    season = Season.objects.all()
    buyer = Buyer.objects.all()
    if request.method == "POST":
        try:
            b = request.POST['buy']
            br = Buyer.objects.get(id=b)
            for i in Bulk_Order.objects.filter(buy=br):
                q = i.qunt.split('.')
                t_qty += int(q[0])
                t_opt += 1
            for i in Dispatch_Detail.objects.filter(bulk=Bulk_Order.objects.filter(buy=br).first()):
                d_qty += int(i.bulk.qunt)
                d_opt += 1
            for i in Sampling.objects.filter(c_status="Under Redevelopment", buyer=br):
                ur_sample += 1
            for i in Sampling.objects.filter(c_status="Under Development", buyer=br) | Sampling.objects.filter(
                    c_status="Under 1st Submittion", buyer=br):
                ud_sample += 1
            for i in Sampling.objects.filter(c_status="Under Digital Approval", buyer=br) | Sampling.objects.filter(
                    c_status="Under 1st Submit Approval", buyer=br) | Sampling.objects.filter(
                c_status="Under 2nd Table Approval", buyer=br) | Sampling.objects.filter(
                c_status="Under 3rd Table Approval", buyer=br) | Sampling.objects.filter(
                c_status="Under 4th Table Approval", buyer=br) | Sampling.objects.filter(
                c_status="Under 5th Table Approval", buyer=br):
                ua_sample += 1
            for i in Sampling.objects.filter(status1="Complete", buyer=br):
                a_sample += 1
            for i in Sampling.objects.filter(buyer=br):
                t_sample += 1
            terror = "Buyer : ({})".format(br.user.username)
        except:
            pass
        try:
            b = request.POST['sea']
            br = Season.objects.get(id=b)
            for i in Bulk_Order.objects.filter(season=br):
                q = i.qunt.split('.')
                t_qty += int(q[0])
                t_opt += 1
            for i in Dispatch_Detail.objects.filter(bulk=Bulk_Order.objects.filter(season=br).first()):
                d_qty += int(i.bulk.qunt)
                d_opt += 1
            for i in Sampling.objects.filter(c_status="Under Redevelopment", season=br):
                ur_sample += 1
            for i in Sampling.objects.filter(c_status="Under Development", season=br) | Sampling.objects.filter(
                    c_status="Under 1st Submittion", season=br):
                ud_sample += 1
            for i in Sampling.objects.filter(c_status="Under Digital Approval", season=br) | Sampling.objects.filter(
                    c_status="Under Digital Approval", season=br):
                ua_sample += 1
            for i in Sampling.objects.filter(status1="Complete", season=br):
                a_sample += 1
            for i in Sampling.objects.filter(season=br):
                t_sample += 1
            terror = "Season : ({})".format(br.name)
        except:
            pass
    d ={'error':error,'t_sample': t_sample,
         'ur_sample': ur_sample,
         'ud_sample': ud_sample,
         'a_sample': a_sample,
         'ua_sample': ua_sample,
         'season': season,
         'buyer': buyer,
         'd_opt': d_opt,
         't_opt': t_opt,
         'd_qty': d_qty,
         'terror': terror,
         'error': error,
         't_qty': t_qty
         }
    return render(request, 'gmt_home.html', d)


def About(request):
    
    return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['name']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        try:
            if not user.is_staff:
                try:
                    sign = Buyer.objects.get(user=user)
                except:
                    pass
                if sign:
                    login(request, user)
                    error = "pat1"
                else:
                    stat = Status.objects.get(status="Accept")
                    pure = False
                    try:
                        pure = Supplier.objects.get(status=stat, user=user)
                    except:
                        pass
                    if pure:
                        login(request, user)
                        error = "pat2"
                    else:
                        stat = Status.objects.get(status="Accept")
                        pure = False
                        try:
                            pure = GMT_Vendor.objects.get(status=stat, user=user)
                        except:
                            pass
                        if pure:
                            login(request, user)
                            error = "pat3"
                        else:

                            pure = False
                            try:
                                pure = RM.objects.get(user=user)
                            except:
                                pass
                            if pure:
                                login(request, user)
                                return redirect('admin_home')
                                error = "pat4"
                            else:
                                error = "notmember"
            elif user:
                login(request, user)
                error = "admin"
            else:
                error = "not"
        except:
            error = "not"
    d ={'error': error}
    return render(request, 'login.html', d)


def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['name']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error = "pat"
        else:
            error = "not"
    d ={'error':error,'error': error}
    return render(request, 'admin_login.html', d)


def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        u = request.POST['name']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        com = request.POST['company']
        type = request.POST['type']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f)
        if type == "Buyer":
            buy = Buyer.objects.create(company=com, user=user, contact=con, address=add)
            SummaryBuyer.objects.create(buyer=buy)
        elif type == "Supplier":
            stat = Status.objects.get(status='pending')
            sup = Supplier.objects.create(company=com, user=user, contact=con, address=add, status=stat)
            SummarySupplier.objects.create(supplier=sup)
        else:
            stat = Status.objects.get(status='pending')
            GMT_Vendor.objects.create(company=com, user=user, contact=con, address=add, status=stat)
        error = "create"
    d ={'error': error}
    return render(request, 'signup.html', d)


def Logout(request):
    error = get_group(request.user.id)
    logout(request)
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Register_RM(request):
    error = get_group(request.user.id)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['name']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f, last_name=l)
        RM.objects.create(user=user, contact=con, address=add)
        terror = True
    d ={'error':error, 'terror': terror}
    return render(request, 'add_rm.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_RM(request, pid):
    buy = RM.objects.get(id=pid)
    terror = False
    error = get_group(request.user.id)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['name']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['address']
        amail = request.POST['aemail']
        buy.user.first_name = f
        buy.user.last_name = l
        buy.user.email = e
        buy.contact = con
        buy.address = add
        buy.additional_email = amail
        buy.save()
        buy.user.save()
        terror = True
    d ={'error':error,'terror': terror, 'error': error, 'buy': buy}
    return render(request, 'edit_rm.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_rm(request, pid):
    buy = Buyer.objects.get(id=pid)
    buy.delete()
    return redirect('view_rm')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def View_RM(request):
    error = get_group(request.user.id)
    buy = RM.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_rm.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Register_Buyer(request):
    error = get_group(request.user.id)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        u = request.POST['name']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        com = request.POST['company']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f)
        buy = Buyer.objects.create(company=com, user=user, contact=con, address=add)
        SummaryBuyer.objects.create(buyer=buy)
        terror = True
    d ={'error':error,'terror': terror}
    return render(request, 'add_buyer.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Register_Supplier(request):
    error = get_group(request.user.id)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        u = request.POST['name']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        com = request.POST['company']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f)
        sup = Supplier.objects.create(company=com, user=user, contact=con, address=add)
        SummarySupplier.objects.create(supplier=sup)
        terror = True
    d ={'error':error,'terror': terror}
    return render(request, 'add_supplier.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Add_Season(request):
    error = get_group(request.user.id)
    terror = False
    if request.method == 'POST':
        u = request.POST['name']
        de = request.POST['desc']
        Season.objects.create(name=u, desc=de)
        terror = True
    d ={'error':error,'terror': terror}
    return render(request, 'add_season.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Add_Drop(request):
    error = get_group(request.user.id)
    terror = False
    if request.method == 'POST':
        u = request.POST['name']
        de = request.POST['desc']
        Drop.objects.create(name=u, desc=de)
        terror = True
    d ={'error':error,'terror': terror}
    return render(request, 'add_drop.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Add_Product(request):
    error = get_group(request.user.id)
    terror = False
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['count']
        co = request.POST['construct']
        g = request.POST['gsm']
        w = request.POST['weave']
        wi = request.POST['width']
        mq = request.POST['moq']
        sr = request.POST['sr']
        pr = request.POST['pr']
        dpr = request.POST['dpr']
        lt = request.POST['leadtime']
        de = request.POST['desc']
        Product.objects.create(printed_rate=pr, digital_rate=dpr, solid_rate=sr, name=n, desc=de, count=c,
                               construction=co, gsm=g, weave=w, width=wi, moq=mq, leadtime=lt)
        terror = True
    d ={'error':error,'terror': terror}
    return render(request, 'add_item.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Add_Sampling(request):
    error = get_group(request.user.id)
    do = datetime.date.today()
    form = SamplingForm()
    try:
        if request.method == 'POST':
            ex = request.FILES['file1']
            df = pd.read_excel(ex)
            cou = df.shape[0]
            i = 0
            while cou:
                cou -= 1
                drop1 = Drop.objects.get(name=str(df['Drop'][i]))
                sea1 = Season.objects.get(name=str(df['Season'][i]))
                user2 = User.objects.get(username=df['Buyer'][i])
                user1 = User.objects.get(username=df['Supplier'][i])
                buy1 = Buyer.objects.get(user=user2)
                sup1 = Supplier.objects.get(user=user1)
                prod1 = Product.objects.get(name=str(df['Quality'][i]))
                tech = df['Technique'][i]
                
                sample = Sampling.objects.create(
                        count=0,dos=do, design_name=df['Design'][i], color_name=df['Color'][i], buyer=buy1,supplier=sup1, drop=drop1, season=sea1, product=prod1, technique=df['Technique'][i],rm = RM.objects.get(user=request.user))
                if tech == "Adhoc":
                    sample.doe = do
                    sample.c_status = "Approved"
                    sample.status = "Complete"
                    sample.save()
                    bulk = Bulk_Order.objects.create(status1="pending", c_status="Order Not Started", sample=sample,buy=sample.buyer, season=sample.season, sup=sample.supplier)
                    Griege_Status.objects.create(bulk=bulk)
                    Bulk_Printed.objects.create(bulk=bulk)
                    FirstBulk.objects.create(bulk=bulk)
                    FPT_Status.objects.create(bulk=bulk)
                    Fabric_Cheking.objects.create(bulk=bulk)
                    Dispatch_Detail.objects.create(bulk=bulk,season=bulk.season,supplier=bulk.sup,buyer=bulk.buy,drop=bulk.drop)
                    Payment_Status.objects.create(bulk=bulk)
                i += 1
            messages.success(request, 'Data Saved Successfully')
            return redirect("all_sampling")
    except:
        try:
            if request.method == 'POST':
                form = SamplingForm(request.POST,request.FILES)
                tech = request.POST['technique']
                if tech:
                    if form.is_valid():
                        user1 = RM.objects.get(user=request.user)
                        user_rm = form.save()
                        user_rm.rm = user1
                        user_rm.save()
                        if tech == "Adhoc":
                            user_rm.doe = do
                            user_rm.c_status = "Approved"
                            user_rm.status = "Complete"
                            user_rm.save()
                            bulk = Bulk_Order.objects.create(status1="pending", c_status="Order Not Started", sample=user_rm,buy=user_rm.buyer, season=user_rm.season, sup=user_rm.supplier)
                            Griege_Status.objects.create(bulk=bulk)
                            Bulk_Printed.objects.create(bulk=bulk)
                            FirstBulk.objects.create(bulk=bulk)
                            FPT_Status.objects.create(bulk=bulk)
                            Fabric_Cheking.objects.create(bulk=bulk)
                            Dispatch_Detail.objects.create(bulk=bulk,season=bulk.season,supplier=bulk.sup,buyer=bulk.buy,drop=bulk.drop)
                            Payment_Status.objects.create(bulk=bulk)
                        messages.success(request, 'Data Saved Successfully')
                        return redirect("all_sampling")
                else:
                    messages.success(request, 'Check Your Data')
        except:
            messages.success(request, 'Invalid User')
    d = {'form': form,'error':error}
    return render(request, 'add_sampling.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Sampling(request,id):
    error = get_group(request.user.id)
    sam = Sampling.objects.get(id=id)
    buy = Courier_Detail.objects.filter(sample=sam)
    if request.method == 'POST':
        c = request.POST['current']
        t = request.POST['doe']
        s = request.POST['c_status']
        sam.status = c
        sam.doe = t
        sam.c_status = s
        sam.save()
        messages.success(request, 'Data Updated Successfully')
        return redirect("view_sampling_uncomplete")
    d = {'sam': sam,'buy':buy,'error':error}
    return render(request, 'update_sampling.html', d)



#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin', 'RM'])
#def Add_Sampling(request):
#    error = get_group(request.user.id)
#    terror = False
#    error2 = False
#    do = datetime.date.today()
#    form = SamplingForm()
#    if request.method == 'POST':
#        try:
#            n = request.POST['name']
#           se = request.POST['sea']
#            co = request.POST['color']
#            d = request.POST['drop']
#            s = request.POST['sup']
#            b = request.POST['buy']
#            p = request.POST['prod']
#            te = request.POST['tech']
#            do1 = request.POST['s_date']
#            f = request.FILES['file']
#            sea1 = Season.objects.get(name=se)
#            user1 = User.objects.get(username=s)
#            user2 = User.objects.get(username=b)
#            sup1 = Supplier.objects.get(user=user1)
#            buy1 = Buyer.objects.get(user=user2)
#            drop1 = Drop.objects.get(name=d)
#            prod1 = Product.objects.get(name=p)
#            if te == "Rotary" and te == "Digital":
#                sample = Sampling.objects.create(count=0, c_status="Under Digital Development",
#                                                 c_table="Digital Strike",
#                                                 dos=do, image=f, product=prod1, design_name=n, color_name=co,
#                                                buyer=buy1,
#                                                 supplier=sup1, drop=drop1, season=sea1, technique=te)
#            return redirect('view_sampling')
#            else:
#                sample = Sampling.objects.create(count=0, c_status="Under 1st Submittion", c_table="1st Submit",
#                                                 dos=do, image=f, product=prod1, design_name=n, color_name=co,
#                                                 buyer=buy1,
#                                                 supplier=sup1, drop=drop1, season=sea1, technique=te)
#                return redirect('view_sampling')
#        except:
#            pass
#        try:
#            ex = request.FILES['file1']
#            df = pd.read_excel(ex)
#            cou = df.shape[0]
#            i = 0
#            while cou:
#                cou -= 1
#                drop1 = Drop.objects.get(name=str(df['DROP'][i]))
#                sea1 = Season.objects.get(name=str(df['SEASON'][i]))
#
#                user2 = User.objects.get(username=df['BUYER'][i])
#                user1 = User.objects.get(username=str(df['SUPPLIER'][i]))
#                buy1 = Buyer.objects.get(user=user2)
#                sup1 = Supplier.objects.get(user=user1)
#                prod1 = Product.objects.get(name=str(df['PRODUCT'][i]))
#                sample = Sampling.objects.create(
#                    count=0, c_status="Under Digital Development", c_table="Digital Strike",
#                    dos=do, design_name=df['DESIGN NAME'][i], color_name=df['COLOR NAME'][i], buyer=buy1,
#                    supplier=sup1, drop=drop1, season=sea1, product=prod1, technique=df['TECHNIQUE'][i])
#                i += 1
#                return redirect('view_sampling')
#            terror = True
#        except:
#            pass
#
#    d ={'error':error,'terror': terror, 'form': form}
#    return render(request, 'add_sampling.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def Add_Sampling_Buyer(request):
    error = get_group(request.user.id)
    form = SamplingForm()
    try:
        if request.method == 'POST':
            ex = request.FILES['file1']
            df = pd.read_excel(ex)
            cou = df.shape[0]
            i = 0
            while cou:
                cou -= 1
                drop1 = Drop.objects.get(name=str(df['Drop'][i]))
                sea1 = Season.objects.get(name=str(df['Season'][i]))
                user1 = User.objects.get(username=str(df['Supplier'][i]))
                buy1 = Buyer.objects.get(user=request.user)
                sup1 = Supplier.objects.get(user=user1)
                prod1 = Product.objects.get(name__icontains=str(df['Quality'][i]))
                tech = df['Technique'][i]
                
                sample = Sampling.objects.create(
                        count=0,dos=datetime.date.today(), design_name=df['Design'][i], color_name=df['Color'][i], buyer=buy1,supplier=sup1, drop=drop1, season=sea1, product=prod1, technique=df['Technique'][i])
                i += 1
            messages.success(request, 'Data Saved Successfully')
            return redirect("sample_buyer")
    except:
        if request.method == 'POST':
            form = SamplingForm(request.POST,request.FILES)
            if form.is_valid():
                sample = form.save()
                sample.buyer = Buyer.objects.get(user=request.user)
                sample.save()
                messages.success(request, 'Data Saved Successfully')
                return redirect("sample_buyer")
    d = {'form': form,'error':error}
    return render(request, 'add_sampling_buyer.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Buyer(request, pid):
    error = get_group(request.user.id)
    buy = Buyer.objects.get(id=pid)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['name']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['address']
        amail = request.POST['aemail']
        try:
            im = request.FILES['image']
            buy.image = im
            buy.save()
        except:
            pass
        buy.user.first_name = f
        buy.user.last_name = l
        buy.user.email = e
        buy.user.username = u
        buy.contact = con
        buy.address = add
        buy.additional_email = amail
        buy.save()
        buy.user.save()
        terror = True
    d ={'error':error,'terror': terror, 'buy': buy}
    return render(request, 'edit_buyer.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Supplier(request, pid):
    error = get_group(request.user.id)
    buy = Supplier.objects.get(id=pid)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['name']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['address']
        amail = request.POST['aemail']
        try:
            im = request.FILES['image']
            buy.image = im
            buy.save()
        except:
            pass
        buy.user.first_name = f
        buy.user.last_name = l
        buy.user.email = e
        buy.contact = con
        buy.address = add
        buy.additional_email = amail
        buy.save()
        buy.user.save()
        terror = True
    d ={'terror':terror,'error': error, 'buy': buy}
    return render(request, 'edit_supplier.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Bulk_Admin(request, pid):
    error = get_group(request.user.id)
    sam = Bulk_Order.objects.get(id=pid)
    try:
        dis = Dispatch_Detail.objects.get(bulk=sam)
    except:
        dis = Dispatch_Detail.objects.create(bulk = sam,season=sam.season,drop=sam.drop,buyer=sam.buy,supplier=sam.sup)
    gmt = GMT_Vendor.objects.all()
    season = Season.objects.all()
    drop = Drop.objects.all()
    terror = False
    do = datetime.date.today()
    bpm_error = ""
    if request.method == 'POST':
        try:
            s = request.POST['style']
            t = request.POST['tech']
            q = request.POST['qunt']
            r = request.POST['rate']
            v = request.POST['value']
            de = request.POST['del']
            mo = request.POST['mon']
            se = request.POST['season']
            dr = request.POST['drop']
            wi = request.POST['width']
            i1 = datetime.datetime.fromisoformat(de).month
            i2 = datetime.datetime.fromisoformat(de).year
            i3 = datetime.datetime.fromisoformat(de).day
            
            a_bpm = int(mo)
            if i1 > a_bpm:
                day1 = 30*(a_bpm+12) + 15
                day2 = 30*i1+i3
                if (day1-day2)>=45:
                    bpm_error = "BPM OK"
                else:
                    bpm_error = "BPM NOT OK"
            else:
                day1 = 30*(a_bpm) + 15
                day2 = (30*i1)+i3
                if (day1-day2)>=45:
                    bpm_error = "BPM OK"
                else:
                    bpm_error = "BPM NOT OK"
            if de:
                sam.del_date = de
                d2 = datetime.datetime.fromisoformat(de).month
                d3 = datetime.datetime.fromisoformat(de).year
                d1 = datetime.datetime.fromisoformat(de).day
                d1 = d1 + 5
                if d1 > 30:
                    d2 = d2 + 1
                    d1 = d1 - 30
                    if d2 > 12:
                        d2 = d2 - 12
                        d3 = d3 + 1
                sam.dupl_del_date = str(d1) + "/" + str(d2) + "/" + str(d3)
                sam.save()
            else:
                pass
            g = request.POST['gmt']
            sam.dos = do
            sam.save()
            sam.dos = do
            sam.save()
            sam1 = Bulk_Order.objects.get(id=pid)
            t1 = sam1.dos
            i1 = datetime.datetime.fromisoformat(de)
            t2 = datetime.date(i1.year, i1.month, i1.day)
            total_day = (t2-t1).days
            gre = total_day * (10 / 100)
            print1 = total_day * (77 / 100)
            check = total_day * (90 / 100)
            dispatch = total_day * (100 / 100)
            sam.gre_date = t1 + timedelta(days=gre)
            sam.print_date =  t1 + timedelta(days=print1)
            sam.checking_date =  t1 + timedelta(days=check)
            sam.dispatch_date =  t1 + timedelta(days=dispatch)
            sam.bpm = calendar.month_name[int(mo)]
            sam.bpmstatus = bpm_error
            sam.time_status = "On Time"
            sam.style = s
            sam.dos = do
            sam.print_tech = t
            sam.qunt = q
            sam.rate = r
            sam.season = Season.objects.get(name=se)
            sam.drop = Drop.objects.get(name=dr)
            sam.width = wi
            sam.value = v
            sam.gmt_vendor = g
            dis.gmt = GMT_Vendor.objects.get(user=User.objects.get(username=g))
            dis.save()
            sam.status1 = "Accept"
            sam.save()
            if not sam.pid:
                sam.pid = sam.id
                sam.save()
            terror = True
        except:
            pass
        try:
            mas = request.FILES['mass']
            df = pd.read_excel(mas)
            cou = df.shape[0]
            i = 0
            while cou:
                cou -= 1
                sam1 = Bulk_Order.objects.get(id=int(df['#'][i]))
                s = str(df['Style'][i])
                se = str(df['Season'][i])
                dr = str(df['Drop'][i])
                wi = str(df['Width'][i])
                t = str(df['Print_Tech'][i])
                q = str(df['Quantity'][i])
                r = str(df['Rate'][i])
                v = int(q) * int(r)
                de = str(df['Delivery'][i])[:10]
                g = str(df['GMT Vendor'][i])
                co = str(df['Copy'][i])
                i1 = datetime.datetime.fromisoformat(de).month
                i2 = datetime.datetime.fromisoformat(de).year
                i3 = datetime.datetime.fromisoformat(de).day
                mo = str(df['BPM No.'][i])
                a_bpm = int(mo)
                if i1 > a_bpm:
                    day1 = 30*(a_bpm+12) + 15
                    day2 = 30*i1+i3
                    if (day1-day2)>=45:
                        bpm_error = "BPM OK"
                    else:
                        bpm_error = "BPM NOT OK"
                else:
                    day1 = 30*(a_bpm) + 15
                    day2 = 30*i1+i3
                    if (day1-day2)>=45:
                        bpm_error = "BPM OK"
                    else:
                        bpm_error = "BPM NOT OK"
                if co == "Y" or co == "y":
                    copy = Bulk_Order.objects.create(pid=sam1.pid, season=Season.objects.get(name=se),drop = Drop.objects.get(name=dr),time_status=sam1.time_status, c_status="Order Not Started",buy=sam1.buy, sup=sam1.sup, sample=sam1.sample, dos=datetime.date.today(),del_date=de,gmt_vendor=sam1.gmt_vendor)
                    Griege_Status.objects.create(bulk=copy)
                    Bulk_Printed.objects.create(bulk=copy)
                    FirstBulk.objects.create(bulk=copy)
                    FPT_Status.objects.create(bulk=copy)
                    Fabric_Cheking.objects.create(bulk=copy)
                    Dispatch_Detail.objects.create(bulk=copy,season=copy.season,drop=copy.drop,buyer=copy.buy,supplier=copy.sup,gmt=GMT_Vendor.objects.get(user=User.objects.get(username=copy.gmt_vendor)))
                    Payment_Status.objects.create(bulk=copy)
            
                    t1 = sam1.dos
                    i1 = datetime.datetime.fromisoformat(de)
                    t2 = datetime.date(i1.year, i1.month, i1.day)
                    total_day = (t2-t1).days
                    gre = total_day * (10 / 100)
                    print1 = total_day * (77 / 100)
                    check = total_day * (90 / 100)
                    dispatch = total_day * (100 / 100)
                    copy.gre_date = t1 + timedelta(days=gre)
                    copy.print_date =  t1 + timedelta(days=print1)
                    copy.checking_date =  t1 + timedelta(days=check)
                    copy.dispatch_date =  t1 + timedelta(days=dispatch)
                    copy.bpmstatus = bpm_error
                    copy.time_status = "On Time"
                    copy.save()
                    if de:
                        copy.del_date = de
                        copy.save()
            
                    else:
                        pass
                    d2 = datetime.datetime.fromisoformat(de).month
                    d3 = datetime.datetime.fromisoformat(de).year
                    d1 = datetime.datetime.fromisoformat(de).day
                    d1 = d1 + 5
                    if d1 > 30:
                        d2 = d2 + 1
                        d1 = d1 - 30
                        if d2 > 12:
                            d2 = d2 - 12
                            d3 = d3 + 1
                    copy.dupl_del_date = str(d1) + "/" + str(d2) + "/" + str(d3)
                    copy.style = s
                    copy.dos = do
                    copy.print_tech = t
                    copy.qunt = q
                    copy.rate = r
                    copy.value = str(v)
                    copy.bpm = calendar.month_name[int(mo)]
                    copy.width = wi
                    copy.gmt_vendor = g
                    copy.status1 = "Accept"
                    copy.save()
                else:   
                    if de:
                        sam1.del_date = de
                        d2 = datetime.datetime.fromisoformat(de).month
                        d3 = datetime.datetime.fromisoformat(de).year
                        d1 = datetime.datetime.fromisoformat(de).day
                        d1 = d1 + 5
                        if d1 > 30:
                            d2 = d2 + 1
                            d1 = d1 - 30
                            if d2 > 12:
                                d2 = d2 - 12
                                d3 = d3 + 1
                        sam1.dupl_del_date = str(d1) + "/" + str(d2) + "/" + str(d3)
                        sam1.save()
                    else:
                        pass
                    sam1.dos = do
                    sam1.save()
                    t1 = do
                    i1 = datetime.datetime.fromisoformat(de)
                    t2 = datetime.date(i1.year, i1.month, i1.day)
                    total_day = (t2-t1).days
                    gre = total_day * (10 / 100)
                    print1 = total_day * (77 / 100)
                    check = total_day * (90 / 100)
                    dispatch = total_day * (100 / 100)
                    sam1.gre_date = t1 + timedelta(days=gre)
                    sam1.print_date =  t1 + timedelta(days=print1)
                    sam1.checking_date =  t1 + timedelta(days=check)
                    sam1.dispatch_date =  t1 + timedelta(days=dispatch)
                    sam1.bpm = calendar.month_name[int(mo)]
                    sam1.bpmstatus = bpm_error
                    sam1.time_status = "On Time"
                    sam1.style = s
                    sam1.dos = do
                    sam1.print_tech = t
                    sam1.qunt = q
                    sam1.rate = r
                    sam1.season = Season.objects.get(name=se)
                    sam1.drop = Drop.objects.get(name=dr)
                    sam1.width = wi
                    sam1.value = str(v)
                    sam1.gmt_vendor = g
                    sam1.status1 = "Accept"
                    sam1.save()
                    if not sam1.pid:
                        sam1.pid = sam1.id
                        sam1.save()
                i += 1
            terror = True
        except:
            pass
    d ={'error':error,'terror': terror, 'pro': sam, 'gmt': gmt,'season':season,'drop':drop}
    return render(request, 'update_bulk_admin.html', d)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Bulk_Order(request, pid):
    error = get_group(request.user.id)
    sam = Bulk_Order.objects.get(id=pid)
    gmt = GMT_Vendor.objects.all()
    terror = False
    bpm_error = ""
    bpm_mon = str(sam.bpm)[:3]
    bpm_id = datetime.datetime.strptime(bpm_mon,"%b").month
    if request.method == 'POST':
        s = request.POST['style']
        dos1 = request.POST['dos']
        if dos1:
            sam.dos = dos1
            sam.save()
        t = request.POST['tech']
        q = request.POST['qunt']
        r = request.POST['rate']
        v = int(q) * int(r)
        de = request.POST['del']
        if de:
            sam.del_date = de
            sam.save()
        mo = request.POST['mon']
        se = request.POST['season']
        dr = request.POST['drop']
        wi = request.POST['width']
        i1 = 0
        i2 = 0
        i3 = 0
        if de:
            i1 = datetime.datetime.fromisoformat(de).month
            i2 = datetime.datetime.fromisoformat(de).year
            i3 = datetime.datetime.fromisoformat(de).day
        else:
            i1 = int(sam.del_date.month)
            i2 = int(sam.del_date.year)
            i3 = int(sam.del_date.day)
        a_bpm = int(mo)
        if i1 > a_bpm:
            day1 = 30*(a_bpm+12) + 15
            day2 = 30*i1+i3
            if (day1-day2)>=45:
                bpm_error = "BPM OK"
            else:
                bpm_error = "BPM NOT OK"
        else:
            day1 = 30*(a_bpm) + 15
            day2 = 30*i1+i3
            if (day1-day2)>=45:
                bpm_error = "BPM OK"
            else:
                bpm_error = "BPM NOT OK"
        if de:
            sam.del_date = de
            d2 = datetime.datetime.fromisoformat(de).month
            d3 = datetime.datetime.fromisoformat(de).year
            d1 = datetime.datetime.fromisoformat(de).day
            d1 = d1 + 5
            if d1 > 30:
                d2 = d2 + 1
                d1 = d1 - 30
                if d2 > 12:
                    d2 = d2 - 12
                    d3 = d3 + 1
            sam.dupl_del_date = str(d1) + "/" + str(d2) + "/" + str(d3)
            sam.save()
        else:
            pass
        g = request.POST['gmt']
        sam1 = Bulk_Order.objects.get(id=pid)
        t1 = sam1.dos
        t2 = sam1.del_date
        if de:
            i1 = datetime.datetime.fromisoformat(de)
            t2 = datetime.date(i1.year, i1.month, i1.day)
        total_day = int(str(t2 - t1)[:-14])
        gre = total_day * (10 / 100)
        print1 = total_day * (77 / 100)
        check = total_day * (90 / 100)
        dispatch = total_day * (100 / 100)
        sam.gre_date = t1 + timedelta(days=gre)
        sam.print_date =  t1 + timedelta(days=print1)
        sam.checking_date =  t1 + timedelta(days=check)
        sam.dispatch_date =  t1 + timedelta(days=dispatch)
        sam.bpm = calendar.month_name[int(mo)]
        sam.bpmstatus = bpm_error
        sam.time_status = "On Time"
        sam.style = s
        sam.print_tech = t
        sam.qunt = q
        sam.rate = r
        sam.width = wi
        sam.value = v
        sam.gmt_vendor = g
        sam.status1 = "Accept"
        sam.save()
        if not sam.pid:
            sam.pid = sam.id
            sam.save()
        terror = True
    d ={'error':error,'terror': terror, 'pro': sam, 'gmt': gmt,'bulk':sam,'bpm_id':bpm_id}
    return render(request, 'update_bulk_order.html', d)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Copies_Of_Bulk(request, pid):
    error = get_group(request.user.id)
    sam1 = Bulk_Order.objects.get(id=pid)
    gmt = GMT_Vendor.objects.all()
    season = Season.objects.all()
    drop = Drop.objects.all()
    terror = False
    do = datetime.date.today()
    sam = ""
    bpm_error = ""
    if request.method == 'POST':
        s = request.POST['style']
        t = request.POST['tech']
        q = request.POST['qunt']
        r = request.POST['rate']
        v = request.POST['value']
        d = request.POST['del']
        mo = request.POST['mon']
        se = request.POST['season']
        dr = request.POST['drop']
        wi = request.POST['width']
        g = request.POST['gmt']
        sam = Bulk_Order.objects.create(gmt_vendor=g,pid=sam1.pid, time_status=sam1.time_status, c_status="Order Not Started",buy=sam1.buy, sup=sam1.sup, sample=sam1.sample, dos=datetime.date.today(),del_date=d)
        Griege_Status.objects.create(bulk=sam)
        Bulk_Printed.objects.create(bulk=sam)
        FirstBulk.objects.create(bulk=sam)
        FPT_Status.objects.create(bulk=sam)
        Fabric_Cheking.objects.create(bulk=sam)
        Dispatch_Detail.objects.create(bulk=sam,season=sam.season,drop=sam.drop,buyer=sam.buy,supplier=sam.sup,gmt=GMT_Vendor.objects.get(user=User.objects.get(username=sam.gmt_vendor)))
        Payment_Status.objects.create(bulk=sam)

        i1 = datetime.datetime.fromisoformat(d).month
        i2 = datetime.datetime.fromisoformat(d).year
        i3 = datetime.datetime.fromisoformat(d).day
        a_bpm = int(mo)
        if i1 > a_bpm:
            day1 = 30*(a_bpm+12) + 15
            day2 = 30*i1+i3
            if (day1-day2)>=45:
                bpm_error = "BPM OK"
            else:
                bpm_error = "BPM NOT OK"
        else:
            day1 = 30*(a_bpm) + 15
            day2 = 30*i1+i3
            if (day1-day2)>=45:
                bpm_error = "BPM OK"
            else:
                bpm_error = "BPM NOT OK"
        sam.dos = do
        sam.save()
        t1 = sam.dos
        i1 = datetime.datetime.fromisoformat(d)
        t2 = datetime.date(i1.year, i1.month, i1.day)
        total_day = int(str(t2 - t1)[:-14])
        gre = total_day * (10 / 100)
        print1 = total_day * (77 / 100)
        check = total_day * (90 / 100)
        dispatch = total_day * (100 / 100)
        sam.gre_date = t1 + timedelta(days=gre)
        sam.print_date =  t1 + timedelta(days=print1)
        sam.checking_date =  t1 + timedelta(days=check)
        sam.dispatch_date =  t1 + timedelta(days=dispatch)
        sam.bpmstatus = bpm_error
        sam.time_status = "On Time"
        sam.save()
        if d:
            sam.del_date = d
            sam.save()

        else:
            pass
        g = request.POST['gmt']
        d2 = datetime.datetime.fromisoformat(d).month
        d3 = datetime.datetime.fromisoformat(d).year
        d1 = datetime.datetime.fromisoformat(d).day
        d1 = d1 + 5
        if d1 > 30:
            d2 = d2 + 1
            d1 = d1 - 30
            if d2 > 12:
                d2 = d2 - 12
                d3 = d3 + 1
        sam.dupl_del_date = str(d1) + "/" + str(d2) + "/" + str(d3)
        sam.save()
        sam.style = s
        sam.dos = do
        sam.print_tech = t
        sam.qunt = q
        sam.rate = r
        sam.value = v
        sam.bpm = calendar.month_name[int(mo)]
        sam.width = wi
        sam.season = Season.objects.get(name=se)
        sam.drop = Drop.objects.get(name=dr)
        sam.gmt_vendor = g
        sam.status1 = "Accept"
        sam.save()
        terror = True
    d ={'error':error,'terror':terror, 'pro': sam1, 'gmt': gmt, 'season': season, 'drop': drop}
    return render(request, 'copy_of_bulk.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_Sample_supplier(request, pid):
    error = get_group(request.user.id)
    sam = Sampling.objects.get(id=pid)
    cour = ""
    try:
        cour = Courier_Detail.objects.filter(sample=sam).latest('id')
    except:
        pass
    if cour:
        if cour.rep_date is None:
            messages.success(request,"Sample details is already updated, Waiting for buyer's comments")
            return redirect('sample_supplier')
    
    if request.method == 'POST':
        aw = request.POST['aws']
        tabl = request.POST['c_table']
        se = request.POST['sent']
        cour = Courier_Detail.objects.create(sample=sam, sent_on=se, awb_no=aw,c_date = datetime.date.today(),supplier=sam.supplier,buyer=sam.buyer)
        if sam.count == 0:
            i1 = datetime.datetime.fromisoformat(se)
            d1 = datetime.date(i1.year, i1.month, i1.day)
            d2 = sam.dos
            d3 = d1 - d2
            d4 = int(sam.time_in_develop)
            sam.time_in_develop = d4 + int(d3.days)
            sam.save()
        else:
            i1 = datetime.datetime.fromisoformat(se)
            d1 = datetime.date(i1.year, i1.month, i1.day)
            d2 = sam.sent_on
            d3 = d1 - d2
            d4 = int(sam.time_in_develop)
            sam.time_in_develop = d4 + int(d3.days)
            sam.save()
        sam.awb_no = aw
        sam.sent_on = se
        if sam.count ==0:
            sam.c_status = "Under 1st Submit Approval"
        elif sam.count ==1:
            sam.c_status = "Under 2nd Submit Approval"
        elif sam.count ==2:
            sam.c_status = "Under 3rd Submit Approval"
        elif sam.count ==3:
            sam.c_status = "Under 4th Submit Approval"
        else:
            sam.c_status = "Under 5th Submit Approval"
        sam.save()
        messages.success(request,"Courrier Updated Successfully")
        return redirect("sample_supplier")
    d ={'error':error, 'pro': sam}
    return render(request, 'update_sample.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_multiple_Sample_supplier(request):
    error = get_group(request.user.id)
    cour = ""
    if request.method == 'POST':
        try:
            aw = request.POST['aws']
            se = request.POST['sent']
            li = request.POST.getlist('checks[]')
            for i in li:
                sam = Sampling.objects.get(id=int(i))
                try:
                    cour = Courier_Detail.objects.filter(sample=sam).latest('id')
                except:
                    pass
                if cour:
                    if cour.rep_date is None:
                        messages.success(request,"Sample details is already updated, Waiting for buyer's comments")
                        return redirect('sample_supplier')
                Courier_Detail.objects.create(sample=sam, sent_on=se, awb_no=aw,c_date = datetime.date.today(),supplier=sam.supplier,buyer=sam.buyer)
                sam.awb_no = aw
                sam.sent_on = se
                sam.c_status = "Under 1st Submit Approval"
                sam.save()
        except:
            pass
    messages.success(request,"Courrier Updated Successfully")
    return redirect('sample_supplier')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def set_delivery_date(request, pid):
    error = get_group(request.user.id)
    sam = Sampling.objects.get(id=pid)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        de = request.POST['del']
        i1 = datetime.datetime.fromisoformat(de)	
        b= datetime.date(i1.year, i1.month, i1.day)
        start = sam.dos
        t_day = (b - start).days
        sam.first = start + timedelta(days = int((t_day * 27)/100))
        sam.second = start + timedelta(days = int((t_day * 71)/100))
        sam.third = start + timedelta(days = int((t_day * 100)/100))
        sam.del_date = de
        sam.c_table = "1st Submit"
        sam.c_status = "Under 1st Submit"
        sam.save()
        messages.success(request,"1st Submit Successfully")
        return redirect('sample_supplier')
    d ={'error':error}
    return render(request, 'set_delivery_date.html', d)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def multiple_set_delivery_date(request):
    error = get_group(request.user.id)
    if request.method == 'POST':
        try:
            d = request.POST['date']
            i1 = datetime.datetime.fromisoformat(d)	
            b= datetime.date(i1.year, i1.month, i1.day)
            li = request.POST.getlist('checks[]')
            for i in li:
                sam = Sampling.objects.get(id = int(i))
                sam.del_date = d
                start = sam.dos
                t_day = (b - start).days
                sam.first = start + timedelta(days = int((t_day * 27)/100))
                sam.second = start + timedelta(days = int((t_day * 71)/100))
                sam.third = start + timedelta(days = int((t_day * 100)/100))
                sam.c_table = "1st Submit"
                sam.c_status = "Under 1st Submit"
                sam.save()
        except:
            pass
    messages.success(request,'Delivery Date Set Successfully')
    return redirect('pendel')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer','admin'])
def Sent_Update_Buyer(request, pid):
    error = get_group(request.user.id)
    sam = Courier_Detail.objects.get(id=pid)
    sample = Sampling.objects.get(id=sam.sample.id)
    do = datetime.date.today()
    if request.method == 'POST':
        st = request.POST['stat']
        me = request.POST['message']
        if sample.technique == "Rotary" or "rotary" or "ROTARY":
            if st == "Approved with Comment" or st == "Approved":
                if sample.count == 0:
                    sample.c_table = "2nd Submit"
                    sample.c_status = "Under 2nd Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.save()
                else:
                    sample.doe = do
                    sample.c_status = "Approved"
                    sample.status = "Complete"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.save()
                cor = Courier_Detail.objects.filter(sample=sample)
                count = 0
                for i in cor:
                    count += 1
                sample.count = count
                sample.save()
            elif st == "Drop":
                sample.c_status = "Drop"
                sample.status = "Close"
                sample.doe = do
                sam.rep_date = do
                d1 = do
                d2 = sam.sent_on
                d3 = d1 - d2
                d4 = sample.time_in_approve
                sample.time_in_approve = int(d4) + int(d3.days)
                sam.save()
                sample.save()
            else:
                if sample.count == 0:
                    sample.count = 1
                    sample.c_table = "2nd Submit"
                    sample.c_status = "Under 2nd Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.save()
                elif sample.count == 1:
                    sample.count = 2
                    sample.c_status = "Under 3rd Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "3rd Submit"
                    sample.save()
                elif sample.count == 2:
                    sample.count = 3
                    sample.c_status = "Under 4th Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "4th Submit"
                    sample.save()
                elif sample.count == 3:
                    sample.count = 4
                    sample.c_status = "Under 5th Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "5th Submit"
                    sample.save()
                elif sample.count == 4:
                    sample.count = 5
                    sample.c_status = "Under 6th Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "6th Submit"
                    sample.save()
                elif sample.count == 5:
                    sample.count = 6
                    sample.c_status = "Close"
                    sample.status = "Close"
                    sample.doe = do
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.save()
        else:
            if st == "Approved with Comment" or st == "Approved":
                sample.c_status = "Approved"
                sample.status = "Complete"
                sample.doe = do
                sam.rep_date = do
                d1 = do
                d2 = sam.sent_on
                d3 = d1 - d2
                d4 = sample.time_in_approve
                sample.time_in_approve = int(d4) + int(d3.days)
                sam.save()
                sample.save()
                cor = Courier_Detail.objects.filter(sample=sample)
                count = 0
                for i in cor:
                    count += 1
                sample.count = count
                sample.save()
            elif st == "Drop":
                sample.c_status = "Drop"
                sample.status = "Close"
                sample.doe = do
                d1 = do
                d2 = sam.sent_on
                d3 = d1 - d2
                d4 = sample.time_in_approve
                sample.time_in_approve = int(d4) + int(d3.days)
                sam.rep_date = do
                sam.save()
                sample.save()
            else:
                if sample.count == 0:
                    sample.count = 1
                    sample.c_table = "2nd Submit"
                    sample.c_status = "Under 2nd Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.save()
                elif sample.count == 1:
                    sample.count = 2
                    sample.c_status = "Under 3rd Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "3rd Submit"
                    sample.save()
                elif sample.count == 2:
                    sample.count = 3
                    sample.c_status = "Under 4th Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "4th Submit"
                    sample.save()
                elif sample.count == 3:
                    sample.count = 4
                    sample.c_status = "Under 5th Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "5th Submit"
                    sample.save()
                elif sample.count == 4:
                    sample.count = 5
                    sample.c_status = "Under 6th Submit"
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.c_table = "6th Submit"
                    sample.save()
                elif sample.count == 5:
                    sample.count = 6
                    sample.c_status = "Close"
                    sample.status = "Close"
                    sample.doe = do
                    sam.rep_date = do
                    d1 = do
                    d2 = sam.sent_on
                    d3 = d1 - d2
                    d4 = sample.time_in_approve
                    sample.time_in_approve = int(d4) + int(d3.days)
                    sam.save()
                    sample.save()
            cor = Courier_Detail.objects.filter(sample=sample)
            count = 0
            for i in cor:
                count += 1
            sample.count = count
            sample.save()
    
        sam.buyer_message = me
        sam.status = st
        sam.save()
        if sample.status == "Complete":
            bulk = Bulk_Order.objects.create(status1="pending", c_status="Order Not Started", sample=sample,
                                             buy=sample.buyer, season=sample.season, sup=sample.supplier)
            Griege_Status.objects.create(bulk=bulk)
            Bulk_Printed.objects.create(bulk=bulk)
            FirstBulk.objects.create(bulk=bulk)
            FPT_Status.objects.create(bulk=bulk)
            Fabric_Cheking.objects.create(bulk=bulk)
            Dispatch_Detail.objects.create(bulk=bulk,season=bulk.season,supplier=bulk.sup,buyer=bulk.buy,drop=bulk.drop)
            Payment_Status.objects.create(bulk=bulk)
        messages.success(request,"Comment Updated Successfully")
        return redirect("sample_buyer")
    d ={'error':error}
    return render(request, 'sent_update.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Running_Supplier_Bulk_Order(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    sign = Supplier.objects.get(user=user)
    order = Bulk_Order.objects.filter(sup=sign, status1="Accept").exclude(Q(c_status="Dispatched") | Q(c_status="Complete"))
    d ={'error':error, 'prod': order}
    return render(request, 'running_supplier_bulk_order.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Supplier_Bulk_Order(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    sign = Supplier.objects.get(user=user)
    order = Bulk_Order.objects.filter(sup=sign, status1="Accept")
    d ={'error':error, 'prod': order}
    return render(request, 'supplier_bulk_order.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['GMT','Supplier'])
def GMT_Bulk_Order(request):
    error = get_group(request.user.id)
    sign = GMT_Vendor.objects.get(user=request.user)
    order = Bulk_Order.objects.filter(gmt_vendor__icontains=sign.user.username).exclude(c_status__icontains = "Greige").exclude(c_status__icontains = "Printed").exclude(c_status__icontains = "FOB").exclude(c_status__icontains = "Under development").exclude(c_status__icontains = "Order Not Started")
    d ={'error': error, 'prod': order}
    return render(request, 'gmt_bulk_order.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['GMT','Supplier'])
def Current_GMT_Bulk_Order(request):
    error = get_group(request.user.id)
    sign = GMT_Vendor.objects.get(user=request.user)
    order = Bulk_Order.objects.filter(gmt_vendor__icontains=sign.user.username).exclude(c_status = "Dispatched").exclude(c_status = "Complete")
    d ={'error': error, 'prod': order}
    return render(request, 'current_gmt_bulk_order.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def Buyer_Bulk_Order(request):
    error = get_group(request.user.id)
    sign = Buyer.objects.get(user=request.user)
    order = Bulk_Order.objects.filter(buy=sign, status1="Accept")
    d ={'error':error, 'prod': order}
    return render(request, 'buy_bulk_order.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier','GMT'])
def Supplier_Bulk_Status(request, pid):
    error = get_group(request.user.id)
    bulk = Bulk_Order.objects.get(id=pid)
    a = Griege_Status.objects.get(bulk=bulk)
    b = Bulk_Printed.objects.get(bulk=bulk)
    e = FirstBulk.objects.get(bulk=bulk)
    f = FPT_Status.objects.get(bulk=bulk)
    g = Fabric_Cheking.objects.get(bulk=bulk)
    h = Dispatch_Detail.objects.get(bulk=bulk)
    i = Payment_Status.objects.get(bulk=bulk)
    d ={'error': error, 'prod': bulk, 'a': a, 'b': b, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i, 'bulk': bulk}
    return render(request, 'sup_bulk_status.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def Buyer_Bulk_Status(request, pid):
    error = get_group(request.user.id)
    bulk = Bulk_Order.objects.get(id=pid)
    a = Griege_Status.objects.get(bulk=bulk)
    b = Bulk_Printed.objects.get(bulk=bulk)
    e = FirstBulk.objects.get(bulk=bulk)
    f = FPT_Status.objects.get(bulk=bulk)
    g = Fabric_Cheking.objects.get(bulk=bulk)
    h = Dispatch_Detail.objects.get(bulk=bulk)
    i = Payment_Status.objects.get(bulk=bulk)
    d ={'error':error, 'prod': bulk, 'a': a, 'b': b, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i}
    return render(request, 'buyer_bulk_status.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_Griege(request, pid):
    error = get_group(request.user.id)
    a = Griege_Status.objects.get(id=pid)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    terror = False
    if request.method == "POST":
        de = request.POST['g_date']
        for i in bulk:
            i.c_status = "Greige Issued"
            a1 = Griege_Status.objects.get(bulk=i)
            a1.g_date = de
            i.save()
            a1.save()
        terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'uid': a.bulk.id}
    return render(request, 'update_griege.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_Griege_Admin(request, pid):
    error = get_group(request.user.id)
    a = Griege_Status.objects.get(id=pid)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    terror = False
    if request.method == "POST":
        de = request.POST['g_date']
        for i in bulk:
            i.c_status = "Greige Issued"
            a1 = Griege_Status.objects.get(bulk=i)
            if de:
                a1.g_date = de
                a1.save()
            i.save()
            a1.save()
        terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'uid': a.bulk.id}
    return render(request, 'update_griege_admin.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_Printed(request, pid):
    error = get_group(request.user.id)
    a = Bulk_Printed.objects.get(id=pid)
    print1 = Griege_Status.objects.get(bulk=a.bulk)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    gerror = False
    print_error = False
    if print1.g_date is None:
        gerror = True
    else:
        pass
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        for i in bulk:
            i.c_status = "Bulk Printed"
            i.save()
            a1 = Bulk_Printed.objects.get(bulk=i)
            i1 = datetime.datetime.fromisoformat(d)
            d1 = datetime.date(i1.year, i1.month, i1.day)
            temp_date = print1.g_date + timedelta(days=3)
            if d1 > temp_date:
                a1.pr_date = d
                a1.save()
                print_error = "yes"
            else:
                perror = "You can't take same or less date from Greige Issue Date."
            terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'perror': perror, 'uid': a.bulk.id,
         'print_error': print_error}
    return render(request, 'update_print.html', d)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_Printed_Admin(request, pid):
    error = get_group(request.user.id)
    a = Bulk_Printed.objects.get(id=pid)
    print1 = Griege_Status.objects.get(bulk=a.bulk)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    gerror = False
    print_error = False
    if print1.g_date is None:
        gerror = True
    else:
        pass
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        if d:
            for i in bulk:
                i.c_status = "Bulk Printed"
                i.save()
                a1 = Bulk_Printed.objects.get(bulk=i)
                i1 = datetime.datetime.fromisoformat(d)
                d1 = datetime.date(i1.year, i1.month, i1.day)
                temp_date = print1.g_date + timedelta(days=3)
                if d1 > temp_date:
                    a1.pr_date = d
                    a1.save()
                    print_error = "yes"
                else:
                    perror = "You can't take same or less date from Greige Issue Date."
                terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'perror': perror, 'uid': a.bulk.id,
         'print_error': print_error}
    return render(request, 'update_print_admin.html', d)




@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_FirstOfBulk(request, pid):
    error = get_group(request.user.id)
    a = FirstBulk.objects.get(id=pid)
    print1 = Bulk_Printed.objects.get(bulk=a.bulk)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    count = len(bulk)
    gerror = False
    if print1.pr_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        s = request.POST['awb']
        c = request.POST['courier']
        i1 = datetime.datetime.fromisoformat(d)
        d1 = datetime.date(i1.year, i1.month, i1.day)
        temp_date = print1.pr_date
        for i in bulk:
            i.c_status = "FOB Sent"
            a1 = FirstBulk.objects.get(bulk=i)
            a1.courier_name = c
            a1.awb_no=s
            if d1 >= temp_date:
                a1.f_date = d
                a1.save()
                i.save()
                print_error = "yes"
                terror = True
            else:
                perror = "You can't take less date from Print Date."
    d ={'error':error,'prod': a, 'terror': terror,'perror': perror, 'uid': a.bulk.id, 'gerror': gerror,'count':count}
    return render(request, 'update_first_bulk.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_FirstOfBulk_Admin(request, pid):
    error = get_group(request.user.id)
    a = FirstBulk.objects.get(id=pid)
    print1 = Bulk_Printed.objects.get(bulk=a.bulk)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    count = len(bulk)
    gerror = False
    if print1.pr_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        s = request.POST['awb']
        c = request.POST['courier']
        if d:
            i1 = datetime.datetime.fromisoformat(d)
            d1 = datetime.date(i1.year, i1.month, i1.day)
        temp_date = print1.pr_date
        for i in bulk:
            i.c_status = "FOB Sent"
            a1 = FirstBulk.objects.get(bulk=i)
            a1.courier_name = c
            a1.awb_no=s
            a1.save()
            i.save()
            
            if d:
                if d1 >= temp_date:
                    a1.f_date = d
                    a1.save()
                    i.save()
                    print_error = "yes"
                    terror = True
                else:
                    perror = "You can't take less date from Print Date."
            print_error = "yes"
            terror = True
    d ={'error':error,'prod': a, 'terror': terror,'perror': perror, 'uid': a.bulk.id, 'gerror': gerror,'count':count}
    return render(request, 'update_first_bulk_admin.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_FPT_Status(request, pid):
    error = get_group(request.user.id)
    a = FPT_Status.objects.get(id=pid)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    gerror = False
    print1 = FirstBulk.objects.get(bulk=a.bulk)
    if print1.f_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        aw = request.POST['awb']
        r = request.POST['rep']
        f = request.FILES['file']
        for i in bulk:
            a1 = FPT_Status.objects.get(bulk=i)
            a1.status = aw
            a1.rep_no = r
            a1.report = f
            a1.save()
        terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'uid': a.bulk.id, 'gerror': gerror}
    return render(request, 'update_fpt_status.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_FPT_Status_Admin(request, pid):
    error = get_group(request.user.id)
    a = FPT_Status.objects.get(id=pid)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    gerror = False
    print1 = FirstBulk.objects.get(bulk=a.bulk)
    if print1.f_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        aw = request.POST['awb']
        r = request.POST['rep']
        for i in bulk:
            a1 = FPT_Status.objects.get(bulk=i)
            if aw:
                a1.status = aw
                a1.save()
            a1.rep_no = r
            try:
                f = request.FILES['file']
                a1.report = f
                a1.save()
            except:
                pass
            a1.save()
        terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'uid': a.bulk.id, 'gerror': gerror}
    return render(request, 'update_fpt_status_admin.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_Fabric_Cheking(request, pid):
    error = get_group(request.user.id)
    a = Fabric_Cheking.objects.get(id=pid)
    bulk = Bulk_Order.objects.get(id=a.bulk.id)
    print1 = FirstBulk.objects.get(bulk=bulk)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    gerror = False
    if print1.f_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        p = request.POST['pass']
        r = request.POST['reject']
        f = request.FILES['file']
        i1 = datetime.datetime.fromisoformat(d)
        d1 = datetime.date(i1.year, i1.month, i1.day)
        temp_date = print1.f_date
        for i in bulk:
            a1 = Fabric_Cheking.objects.get(bulk=i)
            if d1 >= temp_date:
                i.c_status = "Packed"
                i.save()
                a1.qty_pass = p
                a1.qty_reject = r
                a1.f_date = d
                a1.report = f
                a1.save()
                print_error = "yes"
                terror = True
            else:
                perror = "You can't take less date from FOB Date."
    d ={'error':error,'prod': a, 'terror': terror,'perror': perror, 'uid': a.bulk.id, 'gerror': gerror}
    return render(request, 'update_fabric_checking.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_Fabric_Cheking_Admin(request, pid):
    error = get_group(request.user.id)
    a = Fabric_Cheking.objects.get(id=pid)
    bulk = Bulk_Order.objects.get(id=a.bulk.id)
    print1 = FirstBulk.objects.get(bulk=bulk)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    gerror = False
    if print1.f_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        p = request.POST['pass']
        r = request.POST['reject']
        if d:
            i1 = datetime.datetime.fromisoformat(d)
            d1 = datetime.date(i1.year, i1.month, i1.day)
            temp_date = print1.f_date
        for i in bulk:
            a1 = Fabric_Cheking.objects.get(bulk=i)
            if d:
                if d1 >= temp_date:
                    i.c_status = "Packed"
                    i.save()
                    a1.qty_pass = p
                    a1.qty_reject = r
                    a1.f_date = d
                    try:
                        f = request.FILES['file']
                        a1.report = f
                        a1.save()
                    except:
                        pass
                    a1.save()
                    print_error = "yes"
                    terror = True
                else:
                    perror = "You can't take less date from FOB Date."
            print_error = "yes"
            terror = True
    d ={'error':error,'prod': a, 'terror': terror,'perror': perror, 'uid': a.bulk.id, 'gerror': gerror}
    return render(request, 'update_fabric_checking_admin.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_Dispatch_Detail(request, pid):
    error = get_group(request.user.id)
    a = Dispatch_Detail.objects.get(id=pid)
    print1 = Fabric_Cheking.objects.get(bulk=a.bulk)
    gerror = False
    if print1.f_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        di = request.POST['dis']
        t = request.POST['tr']
        l = request.POST['lr']
        f = request.FILES['file']
        i1 = datetime.datetime.fromisoformat(d)
        d1 = datetime.date(i1.year, i1.month, i1.day)
        temp_date = print1.f_date
        a1 = Dispatch_Detail.objects.get(bulk=a.bulk)
        if d1 >= temp_date:
            a.bulk.c_status = "Dispatched"
            a.bulk.save()
            a1.dis_qty = di
            a1.c_date = datetime.date.today()
            a1.tr_name = t
            a1.lr_no = l
            a1.d_date = d
            a1.report = f
            a1.save()
            terror = True
        else:
            perror = "You can't take less date from Fabric Date."
    d ={'error':error,'prod': a, 'terror': terror, 'uid': a.bulk.id, 'gerror': gerror,'perror': perror}
    return render(request, 'update_dispatch_detail.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_Dispatch_Detail_Admin(request, pid):
    error = get_group(request.user.id)
    a = Dispatch_Detail.objects.get(id=pid)
    print1 = Fabric_Cheking.objects.get(bulk=a.bulk)
    gerror = False
    if print1.f_date is None:
        gerror = True
    terror = False
    perror = ""
    if request.method == "POST":
        d = request.POST['g_date']
        di = request.POST['dis']
        t = request.POST['tr']
        l = request.POST['lr']
        if d:
            i1 = datetime.datetime.fromisoformat(d)
            d1 = datetime.date(i1.year, i1.month, i1.day)
            temp_date = print1.f_date
        a1 = Dispatch_Detail.objects.get(bulk=a.bulk)
        a1.dis_qty = di
        a1.c_date = datetime.date.today()
        a1.tr_name = t
        a1.lr_no = l
        a.bulk.c_status = "Dispatched"
        a.save()
        a1.save()
        try:
            f = request.FILES['file']
            a1.report = f
            a1.save()
        except:
            pass
        if d:
            if d1 >= temp_date:
                a.bulk.c_status = "Dispatched"
                a.bulk.save()
                a1.d_date = d
                a1.save()
                terror = True
            else:
                perror = "You can't take less date from Fabric Date."
        terror = True
    d ={'error':error,'prod': a, 'terror': terror, 'uid': a.bulk.id, 'gerror': gerror,'perror': perror}
    return render(request, 'update_dispatch_detail_admin.html', d)




@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Update_Payment_Status(request, pid):
    error = get_group(request.user.id)
    a = Payment_Status.objects.get(id=pid)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    print1 = Dispatch_Detail.objects.get(bulk=a.bulk)
    gerror = False
    if print1.d_date is None:
        gerror = True
    terror = False
    perror = ""
    do = datetime.date.today()
    if request.method == "POST":
        s = request.POST['stat']
        d = request.POST['g_date']
        i1 = datetime.datetime.fromisoformat(d)
        d1 = datetime.date(i1.year, i1.month, i1.day)
        temp_date = print1.d_date+timedelta(days=45)
        for i in bulk:
            a1 = Payment_Status.objects.get(bulk=i)
            if d1 > temp_date:
                a1.p_date = d
                a1.status = s
                i.doe = do
                i.c_status = "Complete"
                i.save()
                a1.save()
                terror = True
            else:
                perror = "You can't take less date from Dispatch Date."
    d ={'error':error,'prod': a, 'terror': terror, 'error': error, 'uid': a.bulk.id, 'gerror': gerror, 'perror': perror}
    return render(request, 'update_payment_status.html', d)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','rm','Supplier'])
def Update_Payment_Status_Admin(request, pid):
    error = get_group(request.user.id)
    a = Payment_Status.objects.get(id=pid)
    bulk = Bulk_Order.objects.filter(pid=a.bulk.pid,dos=a.bulk.dos)
    print1 = Dispatch_Detail.objects.get(bulk=a.bulk)
    gerror = False
    if print1.d_date is None:
        gerror = True
    terror = False
    perror = ""
    do = datetime.date.today()
    if request.method == "POST":
        s = request.POST['stat']
        d = request.POST['g_date']
        if d:
            i1 = datetime.datetime.fromisoformat(d)
            d1 = datetime.date(i1.year, i1.month, i1.day)
            temp_date = print1.d_date+timedelta(days=45)
        for i in bulk:
            a1 = Payment_Status.objects.get(bulk=i)
            a1.status = s
            i.doe = do
            i.c_status = "Complete"
            i.save()
            a1.save()
            terror = True
            if d:
                if d1 > temp_date:
                    a1.p_date = d
                    a1.save()
                    terror = True
                else:
                    perror = "You can't take less date from Dispatch Date."
    d ={'error':error,'prod': a, 'terror': terror, 'error': error, 'uid': a.bulk.id, 'gerror': gerror, 'perror': perror}
    return render(request, 'update_payment_status_admin.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Assign_Status(request, pid):
    a = Supplier.objects.get(id=pid)
    error = get_group(request.user.id)
    terror = False
    if request.method == "POST":
        s = request.POST['stat']
        u = request.POST['uname']
        stat = Status.objects.get(status=s)
        a.status = stat
        a.save()
        terror = True
    d ={'error':error,'prod': a, 'terror': terror}
    return render(request, 'assign_status.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_buyer(request, pid):
    buy = Buyer.objects.get(id=pid)
    buy.delete()
    return redirect('view_buyer')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Assign_Status2(request, pid):
    error = get_group(request.user.id)
    a = GMT_Vendor.objects.get(id=pid)
    terror = False
    if request.method == "POST":
        s = request.POST['stat']
        u = request.POST['uname']
        stat = Status.objects.get(status=s)
        a.status = stat
        a.save()
        terror = True
    d ={'error':error,'prod': a, 'terror': terror}
    return render(request, 'assign_status2.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_buyer(request, pid):
    buy = Buyer.objects.get(id=pid)
    buy.delete()
    return redirect('view_buyer')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_supplier(request, pid):
    buy = Supplier.objects.get(id=pid)
    buy.delete()
    return redirect('view_supplier')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_vendor(request, pid):
    buy = GMT_Vendor.objects.get(id=pid)
    buy.delete()
    return redirect('view_vendor')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_season(request, pid):
    buy = Season.objects.get(id=pid)
    buy.delete()
    return redirect('view_season')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_drop(request, pid):
    buy = Drop.objects.get(id=pid)
    buy.delete()
    return redirect('view_drop')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_bulk(request, pid):
    buy = Bulk_Order.objects.get(id=pid)
    buy.delete()
    return redirect('view_bulk_admin')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_sampling(request, pid):
    buy = Sampling.objects.get(id=pid)
    buy.delete()
    return redirect('all_sampling')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def delete_item(request, pid):
    
    buy = Product.objects.get(id=pid)
    buy.delete()
    return redirect('view_item')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Buyer(request):
    error = get_group(request.user.id)
    buy = Buyer.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_buyer.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Supplier(request):
    error = get_group(request.user.id)
    buy = Supplier.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_supplier.html', d)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Permission(request,pid):
    error = get_group(request.user.id)
    buy = Supplier.objects.get(id=pid)
    if buy.update_perm == None:
        buy.update_perm = "Grant"
        messages.success(request,'Permission Granted')
    elif buy.update_perm == "Grant":
        buy.update_perm = None
        messages.success(request,'Permission Withdrawn')
    buy.save()
    return redirect('view_supplier')
    
        
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Vendor(request):
    error = get_group(request.user.id)
    buy = GMT_Vendor.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_vendor.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Season(request):
    error = get_group(request.user.id)
    buy = Season.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_season.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Drop(request):
    error = get_group(request.user.id)
    buy = Drop.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_drop.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Product(request):
    error = get_group(request.user.id)
    buy = Product.objects.all()
    d ={'error':error,'buy': buy}
    return render(request, 'view_item.html', d)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Product(request, id):
    error = get_group(request.user.id)
    buy = Product.objects.get(id = id)
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['count']
        cn = request.POST['construct']
        g = request.POST['gsm']
        w = request.POST['weave']
        wi = request.POST['width']
        s = request.POST['sr']
        p = request.POST['pr']
        m = request.POST['moq']
        l = request.POST['leadtime']
        d = request.POST['desc']
        buy.name = n
        buy.count = c
        buy.construct = cn
        buy.gsm = g
        buy.weave = w
        buy.width = wi
        buy.sr = s
        buy.pr = p
        buy.moq = m
        buy.leadtime = l
        buy.desc = d
        buy.save()
        messages.success(request, 'Data Updated Successfully')
        return redirect("view_item")
    d ={'error':error,'buy': buy}
    return render(request, 'update_product.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling(request):
    error = get_group(request.user.id)
    samplings=""
    if request.method == "POST":
        n = request.POST['search']
        sd = None
        ed = None
        try:
            sd = request.POST['sdate']
            ed = request.POST['edate']
        except:
            pass
        if not sd:
            sd = datetime.date.today()
            ed= sd - timedelta(days=180)
        if n:
            user = User.objects.get(username__icontains=n)
            buy = Buyer.objects.get(user=user)
            samplings = Sampling.objects.filter(Q(buyer=buy) & Q(dos__range=[ed,sd])).exclude(Q(status="Close"))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,buyer=buy).exclude(Q(status="Close"))
            #         
            # try:
            #     user = User.objects.get(username__icontains=n)
            #     try:
            #         buy = Buyer.objects.get(user=user)
            #         samplings = Sampling.objects.filter(Q(buyer=buy) & Q(dos__range=[ed,sd])).exclude(Q(status="Close"))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,buyer=buy).exclude(Q(status="Close"))
            #     except:
            #         buy = Supplier.objects.get(user=user)
            #         samplings = Sampling.objects.filter(Q(supplier=buy) & Q(dos__range=[ed,sd])).exclude(Q(status="Close"))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,supplier=buy).exclude(Q(status="Close"))
            # except:
            #     try:
            #         samplings = Sampling.objects.filter(Q(design_name__icontains=n) & Q(dos__range=[ed,sd])).exclude(Q(status="Close"))|Sampling.objects.filter(design_name__icontains=n).exclude(Q(status="Close"))
            #         messages.success(request,'Please Elaborate your search criteria.')
            #     except:
            #         pass
        else:
            samplings = Sampling.objects.filter(dos__range=[ed,sd]).exclude(Q(status="Close")) |Sampling.objects.filter(dos__gte=sd,dos__lte=ed).exclude(Q(status="Close"))
    d ={'error':error,'samplings':samplings}
    return render(request, 'all_sampling.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def All_Sampling(request):
    error = get_group(request.user.id)
    samplings=""
    if request.method == "POST":
        n = request.POST['search']
        sd = ""
        ed = ""
        try:
            sd = request.POST['sdate']
            ed = request.POST['edate']
        except:
            pass
        if not sd:
            sd = datetime.date.today()
            ed= sd - timedelta(days=30)
        if n:
            try:
                user = User.objects.get(username__icontains=n)
                try:
                    buy = Buyer.objects.get(user=user)
                    samplings = Sampling.objects.filter(Q(buyer=buy) & Q(dos__range=[ed,sd]))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,buyer=buy)
                except:
                    buy = Supplier.objects.get(user=user)
                    samplings = Sampling.objects.filter(Q(supplier=buy) & Q(dos__range=[ed,sd]))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,supplier=buy)
            except:
                try:
                    samplings = Sampling.objects.filter(Q(design_name__icontains=n) & Q(dos__range=[ed,sd]))|Sampling.objects.filter(design_name__icontains=n)
                    if not samplings:
                        messages.success(request,'Please Elaborate your search criteria.')
                except:
                    pass
        else:
            samplings = Sampling.objects.filter(dos__range=[ed,sd]).exclude(technique = "Adhoc")|Sampling.objects.filter(dos__gte=sd,dos__lte=ed).exclude(technique = "Adhoc")
    d ={'error':error,'samplings':samplings}
    return render(request, 'all_sampling.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Create_Order_Manually(request):
    error = get_group(request.user.id)
    li  = []
    bulk = Bulk_Order.objects.filter(status1="pending")
    for i in bulk:
        li.append(i.sample.id)
    samplings = Sampling.objects.filter(c_status="Approved",status="Complete")
    d ={'error':error,'samplings':samplings,'li':li}
    return render(request, 'Create_Order_Manually.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])    
def update_order_manually(request,pid):
    sample = Sampling.objects.get(id=pid)
    bulk = Bulk_Order.objects.create(status1="pending", c_status="Order Not Started", sample=sample,
                                             buy=sample.buyer, season=sample.season, sup=sample.supplier)
    Griege_Status.objects.create(bulk=bulk)
    Bulk_Printed.objects.create(bulk=bulk)
    FirstBulk.objects.create(bulk=bulk)
    FPT_Status.objects.create(bulk=bulk)
    Fabric_Cheking.objects.create(bulk=bulk)
    Dispatch_Detail.objects.create(bulk=bulk,season=bulk.season,supplier=bulk.sup,buyer=bulk.buy,drop=bulk.drop)
    Payment_Status.objects.create(bulk=bulk)
    messages.success(request,'Manual Order Created Sucessfully')
    return redirect('Create_Order_Manually')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling_Approved(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(c_status="Approved")
    d ={'error':error,'prod': buy}
    return render(request, 'view_sampling.html', d)


@login_required(login_url='login')

def View_Sampling_Underdevel(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(Q(c_status__icontains="Approval"))
    terror = ""
    sup = Buyer.objects.all()
    if request.method == "POST":
        n = request.POST['name']
        user = User.objects.get(username=n)
        to = user.email
        sup1 = Buyer.objects.get(user=user)
        to1 = sup1.additional_email
        to2 = to1.split(",")
        to2.append(to)
        task = "Approval_Rem"
        Send_Mail(to2, user.username, 'Reminder', task)
        terror = True
    d ={'error':error,'prod': buy, 'terror': terror, 'sup': sup}
    return render(request, 'view_sampling_underapproval.html', d)


@login_required(login_url='login')

def View_Sampling_Underapp(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(Q(c_status__icontains="Approval"))
    terror = ""
    sup = Buyer.objects.all()
    if request.method == "POST":
        n = request.POST['name']
        user = User.objects.get(username=n)
        to = user.email
        sup1 = Buyer.objects.get(user=user)
        to1 = sup1.additional_email
        to2 = to1.split(",")
        to2.append(to)
        task = "Approval_Rem"
        Send_Mail(to2, user.username, 'Reminder', task)
        terror = True
    d ={'error':error,'prod': buy, 'terror': terror, 'sup': sup}
    return render(request, 'view_sampling_underapproval.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling_Redevelopment(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(c_status="Under Redevelopment")
    d ={'error':error,'prod': buy}
    return render(request, 'view_sampling.html', d)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'RM'])
# def View_Sampling_late(request):
#     error = get_group(request.user.id)
#     buy = Sampling.objects.filter(time_status="Delayed")
#     d ={'error':error,'prod': buy}
#     return render(request, 'view_sampling_late.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling_ontime(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(time_status="On Time")
    d ={'error':error,'prod': buy}
    return render(request, 'view_sampling_ontime.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling_before(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(time_status="Before Time")
    d ={'error':error,'prod': buy}
    return render(request, 'view_sampling_before.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_brand_Sampling(request, pid):
    error = get_group(request.user.id)
    brand = Buyer.objects.get(id=pid)
    buy = Sampling.objects.filter(buyer=brand)
    d ={'error':error,'prod': buy, 'brand': brand}
    return render(request, 'brand_with_sample.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def View_Supplier_Sampling(request, pid):
    error = get_group(request.user.id)
    brand = Supplier.objects.get(id=pid)
    buy = Sampling.objects.filter(supplier=brand)
    d ={'error':error,'prod': buy, 'brand': brand}
    return render(request, 'supplier_with_sample.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Season_Sampling(request, pid):
    error = get_group(request.user.id)
    brand = Season.objects.get(id=pid)
    buy = Sampling.objects.filter(season=brand)
    d ={'error':error,'prod': buy, 'brand': brand}
    return render(request, 'season_with_sample.html', d)


@login_required(login_url='login')

def View_Courier_latest(request):
    error = get_group(request.user.id)
    to1 = datetime.date.today()
    yes = to1 - timedelta(days=1)
    sample = Courier_Detail.objects.filter(sent_on=yes)
    data = Search_for_date.objects.all()
    sup = Buyer.objects.all()
    terror = ""
    if request.method == "POST":
        try:
            n = request.POST['name']
            d = request.POST['dat1']
            d1 = datetime.datetime.fromisoformat(d)
            day1 = datetime.date.today() - datetime.date(d1.year,d1.month,d1.day)
            user = User.objects.get(username=n)
            to = user.email
            sup1 = Buyer.objects.get(user=user)
            to1 = sup1.additional_email
            to2 = to1.split(",")
            to2.append(to)
            task = "Dispatch_Rem" + "." + str(day1.days)
            terror = True
            Send_Mail(to2, user.username, 'Reminder', task)
        except:
            pass
        try:
            d = request.POST['date']
            try:
                data = Search_for_date.objects.get(id=1)
                data.dat = d
                data.save()
                sample = Courier_Detail.objects.filter(sent_on=data.dat)
            except:
                pass
            if not data:
                data = Search_for_date.objects.create(dat=d)
                sample = Courier_Detail.objects.filter(sent_on=data.dat)
        except:
            pass
    d ={'error':error,'prod': sample, 'yes': yes, 'data': data, 'terror': terror, 'sup': sup}
    return render(request, 'view_courier_latest.html', d)


@login_required(login_url='login')

def View_Courier_update(request):
    error = get_group(request.user.id)
    sup = Supplier.objects.all()
    terror = False
    data = Search_for_date.objects.all()
    sample = ""
    if request.method == "POST":
        try:
            n = request.POST['name']
            user = User.objects.get(username=n)
            to = user.email
            sup1 = Supplier.objects.get(user=user)
            to1 = sup1.additional_email
            to2 = to1.split(",")
            to2.append(to)
            task = "pending_app"
            Send_Mail(to2, user.username, 'Reminder', task)
            terror = True
        except:
            pass
        try:
            d = request.POST['date']
            try:
                data = Search_for_date.objects.get(id=1)
                data.dat = d
                data.save()
                sample = Courier_Detail.objects.filter(rep_date=data.dat)
            except:
                pass
            if not data:
                data = Search_for_date.objects.create(dat=d)
            sample = Courier_Detail.objects.filter(rep_date=data.dat)
            try:
                sample = sample.filter(supplier=Supplier.objects.get(user=request.user))
            except:
                pass
        except:
            pass
    d ={'error':error,'terror':terror,'prod': sample, 'yes': yes, 'data': data, 'sup': sup}
    return render(request, 'view_courier_update.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Comment_Admin(request, pid):
    error = get_group(request.user.id)
    sample = Sampling.objects.get(id=pid)
    buy = Courier_Detail.objects.filter(sample=sample)
    d ={'error':error,'prod': buy}
    return render(request, 'view_comment_admin.html', d)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Bulk_Admin(request):
    error = get_group(request.user.id)
    samplings=""
    if request.method == "POST":
        n = request.POST['search']
        sd = ""
        ed = ""
        try:
            sd = request.POST['sdate']
            ed = request.POST['edate']
        except:
            pass
        if not sd:
            sd = datetime.date.today()
            ed= sd - timedelta(days=30)
        if n:
            try:
                user = User.objects.get(username__icontains=n)
                try:
                    buy = Buyer.objects.get(user=user)
                    samplings = Bulk_Order.objects.filter(Q(buy=buy) & Q(dos__range=[ed,sd]) & Q(status1="Accept"))|Bulk_Order.objects.filter(dos__gte=sd,dos__lte=ed,buy=buy,status1="Accept")
                except:
                    buy = Supplier.objects.get(user=user)
                    samplings = Bulk_Order.objects.filter(Q(sup=buy) & Q(dos__range=[ed,sd]) & Q(status1="Accept"))|Bulk_Order.objects.filter(dos__gte=sd,dos__lte=ed,sup=buy,status1="Accept")
            except:
                try:
                    samplings = BUlk_Order.objects.filter(Q(sample__design_name__icontains=n) &  Q(dos__range=[ed,sd]) & Q(status1="Accept"))|BUlk_Order.objects.filter(dos__gte=sd,dos__lte=ed,sample__design_name__icontains=n,status1="Accept")
                    if not samplings:
                        messages.success(request,'Please Elaborate your search criteria.')
                except:
                    pass
        else:
            samplings = Bulk_Order.objects.filter(dos__range=[ed,sd],status1="Accept")|Bulk_Order.objects.filter(dos__gte=sd,dos__lte=ed,status1="Accept")
    d ={'error':error,'prod': samplings}
    return render(request, 'view_bulk_ad.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Start_Bulk_Admin(request):
    error = get_group(request.user.id)
    data = Search_for_date.objects.all()
    to = datetime.date.today()
    yes = to - timedelta(days=1)
    sample = Bulk_Order.objects.filter(dos=yes)
    if request.method == "POST":
        d = request.POST['date']
        try:
            data = Search_for_date.objects.get(id=1)
            data.dat = d
            data.save()
            sample = Bulk_Order.objects.filter(dos=data.dat)
        except:
            pass
        if not data:
            data = Search_for_date.objects.create(dat=d)
            sample = Bulk_Order.objects.filter(dos=data.dat)

    d ={'error':error,'prod': sample, 'yes': yes, 'data': data}
    return render(request, 'bulk_start_report.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_End_Bulk_Admin(request):
    error = get_group(request.user.id)
    to = datetime.date.today()
    yes = to - timedelta(days=1)
    sample = Bulk_Order.objects.filter(doe=yes)
    d ={'error':error,'prod': sample, 'yes': yes}
    return render(request, 'bulk_end_report.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Pending_Bulk(request):
    error = get_group(request.user.id)
    sample = Bulk_Order.objects.filter(status1="pending")
    d ={'error':error,'prod': sample}
    return render(request, 'view_pending_bulk.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def admin_bulk_status(request, pid):
    error = get_group(request.user.id)
    bulk = Bulk_Order.objects.get(id=pid)
    a = Griege_Status.objects.get(bulk=bulk)
    b = Bulk_Printed.objects.get(bulk=bulk)
    e = FirstBulk.objects.get(bulk=bulk)
    f = FPT_Status.objects.get(bulk=bulk)
    g = Fabric_Cheking.objects.get(bulk=bulk)
    h = Dispatch_Detail.objects.get(bulk=bulk)
    i = Payment_Status.objects.get(bulk=bulk)
    d ={'error':error,'prod': bulk, 'a': a, 'b': b, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i}
    return render(request, 'admin_bulk_status.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=["Supplier"])
def Sampling_Supplier(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    sign = Supplier.objects.get(user=user)
    sample = Sampling.objects.filter(supplier=sign).exclude(technique = "Adhoc")
    d ={'error':error,'prod': sample}
    return render(request, 'sample_supplier.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Supplier"])
def Running_Sampling_Supplier(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    sign = Supplier.objects.get(user=user)
    sample = Sampling.objects.filter(supplier=sign).exclude(Q(status="Complete") | Q(status="Close"))
    d ={'error':error,'prod': sample}
    return render(request, 'Running_Sampling_Supplier.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer','admin'])
def Sampling_Buyer(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    supp = Buyer.objects.get(user=user)
    sample = Sampling.objects.filter(buyer=supp)
    d ={'error':error,'prod': sample}
    return render(request, 'sample_buyer.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def under_develope_sample_buyer(request):
    error = get_group(request.user.id)
    sample = Sampling.objects.filter(c_status="Under Digital Development", buyer=sign) | Sampling.objects.filter(c_status="Under Digital Approval", buyer=sign) | Sampling.objects.filter(c_status="Under Development",buyer=sign) | Sampling.objects.filter(c_status="Under Table Approval", buyer=sign) | Sampling.objects.filter(c_status="Under 1st Submit Approval",buyer=sign) | Sampling.objects.filter(c_status="Under Redevelopment", buyer=sign)
    d ={'error':error,'prod': sample}
    return render(request, 'under_develope_sample_buyer.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def under_develop_bulk_buyer(request):
    error = get_group(request.user.id)
    order = Bulk_Order.objects.filter(c_status="Under Development", buy=sign, status1="Accept")
    d ={'error':error, 'prod': order}
    return render(request, 'under_develop_bulk_buyer.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def under_develope_sample_supplier(request):
    error = get_group(request.user.id)
    sample = Sampling.objects.filter(c_status="Under Digital Development", supplier=sign) | Sampling.objects.filter(
        c_status="Under Digital Approval", supplier=sign) | Sampling.objects.filter(c_status="Under Development",
                                                                                    supplier=sign) | Sampling.objects.filter(
        c_status="Under Table Approval", supplier=sign) | Sampling.objects.filter(c_status="Under 1st Submit Approval",
                                                                                  supplier=sign) | Sampling.objects.filter(
        c_status="Under Redevelopment", supplier=sign)
    d ={'error':error,'prod': sample}
    return render(request, 'under_develope_sample_supplier.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def under_develop_bulk_supplier(request):
    error = get_group(request.user.id)
    order = Bulk_Order.objects.filter(c_status="Under Development", sup=sign, status1="Accept")
    d ={'error':error, 'prod': order}
    return render(request, 'under_develop_bulk_supplier.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer','Supplier'])
def Sampling_Comment(request, pid):
    error = get_group(request.user.id)
    sample = Sampling.objects.get(id=pid)
    prod = Courier_Detail.objects.filter(sample=sample)
    d ={'error':error,'prod': prod, 'error': error}
    return render(request, 'view_comment.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Sampling_accuracy(request):
    error = get_group(request.user.id)
    per1 = 0
    per2 = 0
    per3 = 0
    per4 = 0
    le1 = 0
    le2 = 0
    le3 = 0
    le4 = 0
    sample = Sampling.objects.all()
    season = Season.objects.all()
    buyer = Buyer.objects.all()
    le = len(sample)
    terror = "Season & Buyer : ({},{})".format("All Season", "All Users")
    if request.method == "POST":
        sea = request.POST['sea']
        buy = request.POST['buy']
        if sea == "All" and buy == "All":
            terror = "Season & Buyer : ({},{})".format(sea, buy)
            sam1 = Sampling.objects.filter(count=2, c_status="Approved", technique="Rotary") | Sampling.objects.filter(count=1, c_status="Approved", technique="labdips") | Sampling.objects.filter(count=1,c_status="Approved",technique="Digital")
            sam2 = Sampling.objects.filter(count=3, c_status="Approved", technique="Rotary") | Sampling.objects.filter(count=2, c_status="Approved", technique="labdips") | Sampling.objects.filter(count=2,c_status="Approved",technique="Digital")
            sam3 = Sampling.objects.filter(count=4, c_status="Approved", technique="Rotary") | Sampling.objects.filter(count=5, c_status="Approved", technique="Rotary") | Sampling.objects.filter(count=6,c_status="Approved",technique="Rotary") | Sampling.objects.filter(count=3, c_status="Approved", technique="labdips") | Sampling.objects.filter(count=4,c_status="Approved",technique="labdips") | Sampling.objects.filter(count=5, c_status="Approved", technique="labdips") | Sampling.objects.filter(count=3,c_status="Approved",technique="Digital") | Sampling.objects.filter(count=4, c_status="Approved", technique="Digital") | Sampling.objects.filter(count=5,c_status="Approved",technique="Digital")
            sam4 = Sampling.objects.filter(doe=None)
            le1 = len(sam1)
            le2 = len(sam2)
            le3 = len(sam3)
            le4 = len(sam4)
            per1 = (le1 / le) * 100
            per2 = (le2 / le) * 100
            per3 = (le3 / le) * 100
            per4 = (le4 / le) * 100
        elif buy == "All":
            season1 = Season.objects.get(id=sea)
            sample = Sampling.objects.filter(season=season1)
            le = len(sample)
            terror = "Season & Buyer : ({},{})".format(season1.name, buy)
            sam1 = Sampling.objects.filter(count=2, c_status="Approved", technique="Rotary",season=season1) | Sampling.objects.filter(count=1, c_status="Approved",technique="labdips",season=season1) | Sampling.objects.filter(count=1, c_status="Approved", technique="Digital", season=season1)
            sam2 = Sampling.objects.filter(count=3, c_status="Approved", technique="Rotary",season=season1) | Sampling.objects.filter(count=2, c_status="Approved",technique="labdips",season=season1) | Sampling.objects.filter(count=2, c_status="Approved", technique="Digital", season=season1)
            sam3 = Sampling.objects.filter(count=4, c_status="Approved", technique="Rotary",season=season1) | Sampling.objects.filter(count=5, c_status="Approved",technique="Rotary",season=season1) | Sampling.objects.filter(count=6, c_status="Approved", technique="Rotary", season=season1) | Sampling.objects.filter(count=3,c_status="Approved",technique="labdips",season=season1) | Sampling.objects.filter(count=4, c_status="Approved", technique="labdips", season=season1) | Sampling.objects.filter(count=5,c_status="Approved",technique="labdips",season=season1) | Sampling.objects.filter(count=3, c_status="Approved", technique="Digital", season=season1) | Sampling.objects.filter(count=4,c_status="Approved",technique="Digital",season=season1) | Sampling.objects.filter(count=5, c_status="Approved", technique="Digital", season=season1)
            sam4 = Sampling.objects.filter(doe=None, season=season1)
            le1 = len(sam1)
            le2 = len(sam2)
            le3 = len(sam3)
            le4 = len(sam4)
            per1 = (le1 / le) * 100
            per2 = (le2 / le) * 100
            per3 = (le3 / le) * 100
            per4 = (le4 / le) * 100
        elif sea == "All":
            buyer1 = Buyer.objects.get(id=buy)
            sample = Sampling.objects.filter(buyer=buyer1)
            le = len(sample)
            le = len(Sampling.objects.filter(buyer=buyer1))
            terror = "Season & Buyer : ({},{})".format(sea, buyer1.user.username)
            sam1 = Sampling.objects.filter(count=2, c_status="Approved", technique="Rotary",buyer=buyer1) | Sampling.objects.filter(count=1, c_status="Approved",technique="labdips",buyer=buyer1) | Sampling.objects.filter(count=1, c_status="Approved", technique="Digital", buyer=buyer1)
            sam2 = Sampling.objects.filter(count=3, c_status="Approved", technique="Rotary",buyer=buyer1) | Sampling.objects.filter(count=2, c_status="Approved",technique="labdips",buyer=buyer1) | Sampling.objects.filter(count=2, c_status="Approved", technique="Digital", buyer=buyer1)
            sam3 = Sampling.objects.filter(count=4, c_status="Approved", technique="Rotary",buyer=buyer1) | Sampling.objects.filter(count=5, c_status="Approved",technique="Rotary",buyer=buyer1) | Sampling.objects.filter(count=6, c_status="Approved", technique="Rotary", buyer=buyer1) | Sampling.objects.filter(count=3,c_status="Approved",technique="labdips",buyer=buyer1) | Sampling.objects.filter(count=4, c_status="Approved", technique="labdips", buyer=buyer1) | Sampling.objects.filter(count=5,c_status="Approved",technique="labdips",buyer=buyer1) | Sampling.objects.filter(count=3, c_status="Approved", technique="Digital", buyer=buyer1) | Sampling.objects.filter(count=4,c_status="Approved",technique="Digital",buyer=buyer1) | Sampling.objects.filter(count=5, c_status="Approved", technique="Digital", buyer=buyer1)
            sam4 = Sampling.objects.filter(doe=None, buyer=buyer1)
            le1 = len(sam1)
            le2 = len(sam2)
            le3 = len(sam3)
            le4 = len(sam4)
            per1 = (le1 / le) * 100
            per2 = (le2 / le) * 100
            per3 = (le3 / le) * 100
            per4 = (le4 / le) * 100
        else:
            season1 = Season.objects.get(id=sea)
            buyer1 = Buyer.objects.get(id=buy)
            sample = Sampling.objects.filter(buyer=buyer1, season=season1)
            le = len(sample)
            terror = "Season & Buyer : ({},{})".format(season1.name, buyer1.user.username)
            sam1 = Sampling.objects.filter(count=2, c_status="Approved", technique="Rotary", season=season1,buyer=buyer1) | Sampling.objects.filter(count=1, c_status="Approved",technique="labdips", season=season1,buyer=buyer1) | Sampling.objects.filter(count=1, c_status="Approved", technique="Digital", season=season1, buyer=buyer1)
            sam2 = Sampling.objects.filter(count=3, c_status="Approved", technique="Rotary", season=season1,buyer=buyer1) | Sampling.objects.filter(count=2, c_status="Approved",technique="labdips", season=season1,buyer=buyer1) | Sampling.objects.filter(count=2, c_status="Approved", technique="Digital", season=season1, buyer=buyer1)
            sam3 = Sampling.objects.filter(count=4, c_status="Approved", technique="Rotary", season=season1,buyer=buyer1) | Sampling.objects.filter(count=5, c_status="Approved",technique="Rotary", season=season1,buyer=buyer1) | Sampling.objects.filter(count=6, c_status="Approved", technique="Rotary", season=season1,buyer=buyer1) | Sampling.objects.filter(count=3, c_status="Approved", technique="labdips", season=season1, buyer=buyer1) | Sampling.objects.filter(count=4, c_status="Approved", technique="labdips", season=season1, buyer=buyer1) | Sampling.objects.filter(count=5, c_status="Approved", technique="labdips", season=season1,buyer=buyer1) | Sampling.objects.filter(count=3, c_status="Approved", technique="Digital", season=season1, buyer=buyer1) | Sampling.objects.filter(count=4, c_status="Approved",technique="Digital",season=season1,buyer=buyer1) | Sampling.objects.filter(count=5, c_status="Approved", technique="Digital", season=season1, buyer=buyer1)
            sam4 = Sampling.objects.filter(doe=None, season=season1, buyer=buyer1)
            le1 = len(sam1)
            le2 = len(sam2)
            le3 = len(sam3)
            le4 = len(sam4)
            per1 = (le1 / le) * 100
            per2 = (le2 / le) * 100
            per3 = (le3 / le) * 100
            per4 = (le4 / le) * 100

    d ={'error':error,'season': season,
         'buyer': buyer,
         'terror': terror,
         'tab1': "1st Submit Approval",
         'tab2': "2nd Submit Approval",
         'tab3': "3rd Submit Approval",
         'tab4': "Under Approval",
         'per1': (str(per1)).split('.')[0],
         'per2': (str(per2)).split('.')[0],
         'per3': (str(per3)).split('.')[0],
         'per4': (str(per4)).split('.')[0],
         'le1': le1,
         'le2': le2,
         'le3': le3,
         'le4': le4
         }
    return render(request, 'sampling_accuracy.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def History_Sampling(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.all()
    d ={'error':error,'prod': buy}
    return render(request, 'history_sampling.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def History1(request, pid):
    error = get_group(request.user.id)
    sample = Sampling.objects.get(id=pid)
    courrier = Courier_Detail.objects.filter(sample=sample)
    d ={'error':error,'sample': sample, 'courrier': courrier}
    return render(request, 'history1.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling_pendingdel(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    supp = Supplier.objects.get(user=user)
    
    buy = Sampling.objects.filter(del_date=None, supplier=supp)
    d ={'error':error,'prod': buy}
    return render(request, 'pendingdelivery.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supplier'])
def Pending_Del(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    supp = Supplier.objects.get(user=user)
    buy = Sampling.objects.filter(del_date=None, supplier=supp).exclude(technique="Adhoc")
    d ={'error':error,'prod': buy}
    return render(request, 'pendingdelivery.html', d)


@login_required(login_url='login')

def Pending_Del_Admin(request):
    error = get_group(request.user.id)
    new_rm = 0
    buy = None
    if request.user.is_staff:
        new_rm = request.GET.get('rm',0)
    else:
        new_rm = request.GET.get('rm',request.user.id)
    rm = RM.objects.all()
    if new_rm:
        buy = Sampling.objects.filter(del_date=None, rm=RM.objects.get(user=int(new_rm))).exclude(technique="Adhoc")
    else:
        buy = Sampling.objects.filter(del_date=None).exclude(technique="Adhoc")
    sup = Supplier.objects.all()
    terror = False
    if request.method == "POST":
        n = request.POST['name']
        user = User.objects.get(username=n)
        to = user.email
        sup1 = Supplier.objects.get(user=user)
        to1 = sup1.additional_email
        to2 = to1.split(",")
        to2.append(to)
        task = "Set_Del"
        Send_Mail(to2, user.username, 'Reminder', task)
        terror = True
    d ={'error':error,'prod': buy, 'sup': sup, 'terror': terror,'rm':rm, 'new_rm':int(new_rm)}
    return render(request, 'pendingdelivery.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def Pending_app_buyer(request):
    error = get_group(request.user.id)
    user = User.objects.get(id=request.user.id)
    buyer = Buyer.objects.get(user=user)
    buy = Sampling.objects.filter(c_status__icontains="Approval", buyer=buyer)
    d ={'error':error,'prod': buy, 'error': error}
    return render(request, 'pending_app_buyer.html', d)
    
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer','Supplier'])
def dispatch_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier,sea,buy = None, None, None
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        pass
    dis_buy1 = ""
    dis_buy1 = Bulk_Order.objects.filter(status1="Accept", c_status__in = ["Dispatched", "Complete"])
    if buyer:
        buy = Buyer.objects.get(id=buyer)
        dis_buy1 = dis_buy1.filter(buy=buy)
    if season:
        sea = Season.objects.get(id = season)
        dis_buy1 = dis_buy1.filter(season=sea)
    if supplier:
        dis_buy1 = dis_buy1.filter(sup=supplier)
    d ={'error':error, 'prod':dis_buy1,'sea':sea,'buy':buy}
    return render(request, 'dispatched_dash.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def packed_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier,sea,buy = None, None, None
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        pass
    dis_buy1 = ""
    dis_buy1 = Bulk_Order.objects.filter(status1="Accept", c_status__in = ["Packed", "FOB Sent"])
    if buyer:
        buy = Buyer.objects.get(id=buyer)
        dis_buy1 = dis_buy1.filter(buy=buy)
    if season:
        sea = Season.objects.get(id = season)
        dis_buy1 = dis_buy1.filter(season=sea)
    if supplier:
        dis_buy1 = dis_buy1.filter(sup=supplier)
    d ={'error':error, 'prod':dis_buy1,'sea':sea,'buy':buy}
    return render(request, 'packed_dash.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def under_prodn_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier,sea,buy = None, None, None
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        pass
    dis_buy1 = ""
    dis_buy1 = Bulk_Order.objects.filter(status1="Accept", c_status__in = ["Greige Issued", "Bulk Printed","Under development", "Order Not Started"])
    if buyer:
        buy = Buyer.objects.get(id=buyer)
        dis_buy1 = dis_buy1.filter(buy=buy)
    if season:
        sea = Season.objects.get(id = season)
        dis_buy1 = dis_buy1.filter(season=sea)
    if supplier:
        dis_buy1 = dis_buy1.filter(sup=supplier)
    d ={'error':error, 'prod':dis_buy1,'sea':sea,'buy':buy}
    return render(request, 'under_prodn_dash.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def Ontime_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier,sea,buy = None, None, None
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        pass
    dis_buy1 = ""
    dis_buy1 = Bulk_Order.objects.filter(status1="Accept", time_status = "On Time", c_status__in = ["Greige Issued", "Bulk Printed","Under development", "Order Not Started"])
    if buyer:
        buy = Buyer.objects.get(id=buyer)
        dis_buy1 = dis_buy1.filter(buy=buy)
    if season:
        sea = Season.objects.get(id = season)
        dis_buy1 = dis_buy1.filter(season=sea)
    if supplier:
        dis_buy1 = dis_buy1.filter(sup=supplier)
    d ={'error':error, 'prod':dis_buy1,'sea':sea,'buy':buy}
    return render(request, 'Ontime_dash.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def Delay_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier,sea,buy = None, None, None
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        pass
    dis_buy1 = ""
    dis_buy1 = Bulk_Order.objects.filter(status1="Accept", time_status = "Delayed", c_status__in = ["Greige Issued", "Bulk Printed","Under development", "Order Not Started"])
    if buyer:
        buy = Buyer.objects.get(id=buyer)
        dis_buy1 = dis_buy1.filter(buy=buy)
    if season:
        sea = Season.objects.get(id = season)
        dis_buy1 = dis_buy1.filter(season=sea)
    if supplier:
        dis_buy1 = dis_buy1.filter(sup=supplier)
    d ={'error':error, 'prod':dis_buy1,'sea':sea,'buy':buy}
    return render(request, 'Delay_dash.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def total_qty_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier,sea,buy = None, None, None
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        pass
    dis_buy1 = ""
    dis_buy1 = Bulk_Order.objects.filter(status1="Accept")
    if buyer:
        buy = Buyer.objects.get(id=buyer)
        dis_buy1 = dis_buy1.filter(buy=buy)
    if season:
        sea = Season.objects.get(id = season)
        dis_buy1 = dis_buy1.filter(season=sea)
    if supplier:
        dis_buy1 = dis_buy1.filter(sup=supplier)
    d ={'error':error, 'prod':dis_buy1,'sea':sea,'buy':buy}
    return render(request, 'total_qty_dash_admin.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def approved_sample_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    supplier = None
    buyer = buyer
    dis_buy1 = ""
    se1 = "All"
    br1 = "All"
    if season == 0 and buyer == 0:
        dis_buy1 = Sampling.objects.filter(Q(c_status="Approved"))
    elif season == 0 and buyer != 0:
        br = Buyer.objects.get(id=buyer)
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status="Approved")& Q(buyer = br))
    elif season!=0 and buyer==0:
        se = Season.objects.get(id = season)
        se1 = se.name
        dis_buy1 = Sampling.objects.filter(Q(c_status="Approved")& Q(season = se))
    else:
        br = Buyer.objects.get(id=buyer)
        se = Season.objects.get(id = season)
        se1 = se.name
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status="Approved")& Q(season = se)& Q(buyer = br))
    try:
        supplier = Supplier.objects.get(user=request.user)
        dis_buy1 = dis_buy1.filter(supplier=supplier)
    except:
        pass
    d ={'error':error, 'prod':dis_buy1,'sea':se1,'buy':br1}
    return render(request, 'approved_sample_dash_admin.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def under_dev_sample_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    # nexmo = Sampling.objects.all()
    # for i in nexmo:
    #     i.time_in_develop = 0
    #     i.time_in_approve = 0
    #     i.save()
    season = season
    buyer = buyer
    supplier = None
    dis_buy1 = ""
    se1 = "All"
    br1 = "All"
    if season == 0 and buyer == 0:
        dis_buy1 = Sampling.objects.filter(Q(c_status = "Under 1st Submit")).exclude(technique = "Adhoc") | Sampling.objects.filter(Q(c_status="Under 2nd Submit")).exclude(technique__in=["Solid","Digital","Adhoc"])
        
    elif season == 0 and buyer != 0:
        br = Buyer.objects.get(id=buyer)
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status = "Under 1st Submit")& Q(buyer = br)).exclude(technique = "Adhoc") | Sampling.objects.filter(Q(c_status="Under 2nd Submit")& Q(buyer = br)).exclude(technique__in=["Solid","Digital","Adhoc"])
    elif season!=0 and buyer==0:
        se = Season.objects.get(id = season)
        se1 = se.name
        dis_buy1 = Sampling.objects.filter(Q(c_status = "Under 1st Submit")& Q(season = se)).exclude(technique = "Adhoc") | Sampling.objects.filter(Q(c_status="Under 2nd Submit")& Q(season = se)).exclude(technique__in=["Solid","Digital","Adhoc"])
    else:
        br = Buyer.objects.get(id=buyer)
        se = Season.objects.get(id = season)
        se1 = se.name
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status = "Under 1st Submit")& Q(season = se)& Q(buyer = br)).exclude(technique = "Adhoc") | Sampling.objects.filter(Q(c_status="Under 2nd Submit")& Q(season = se)& Q(buyer = br)).exclude(technique__in=["Solid","Digital","Adhoc"])
    try:
        supplier = Supplier.objects.get(user=request.user)
        dis_buy1 = dis_buy1.filter(supplier=supplier)
    except:
        pass
    d ={'error':error, 'prod':dis_buy1,'sea':se1,'buy':br1}
    return render(request, 'under_dev_sample_dash_admin.html', d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def under_app_sample_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    suppplier = None
    dis_buy1 = ""
    se1 = "All"
    br1 = "All"
    if season == 0 and buyer == 0:
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="Approval"))
    elif season == 0 and buyer != 0:
        br = Buyer.objects.get(id=buyer)
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="Approval")& Q(buyer = br))
    elif season!=0 and buyer==0:
        se = Season.objects.get(id = season)
        se1 = se.name
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="Approval")& Q(season = se))
    else:
        br = Buyer.objects.get(id=buyer)
        se = Season.objects.get(id = season)
        se1 = se.name
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="Approval")& Q(season = se)& Q(buyer = br))
    try:
        supplier = Supplier.objects.get(user=request.user)
        dis_buy1 = dis_buy1.filter(supplier=supplier)
    except:
        pass
    d ={'error':error, 'prod':dis_buy1,'sea':se1,'buy':br1}
    return render(request, 'under_app_sample_dash_admin.html', d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def under_redo_sample_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier = None
    dis_buy1 = ""
    se1 = "All"
    br1 = "All"
    if season == 0 and buyer == 0:
        dis_buy1 = Sampling.objects.filter(Q(c_status="Under 2nd Submit")).exclude(technique = "Rotary") | Sampling.objects.filter(Q(c_status = "Under 3rd Submit"))| Sampling.objects.filter(Q(c_status = "Under 4th Submit"))| Sampling.objects.filter(Q(c_status = "Under 5th Submit"))
    elif season == 0 and buyer != 0:
        br = Buyer.objects.get(id=buyer)
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status="Under 2nd Submit")& Q(buyer = br)).exclude(technique = "Rotary")|Sampling.objects.filter(Q(c_status = "Under 3rd Submit")& Q(buyer = br))|Sampling.objects.filter(Q(c_status = "Under 4th Submit")& Q(buyer = br))|Sampling.objects.filter(Q(c_status = "Under 5th Submit")& Q(buyer = br))
    elif season!=0 and buyer==0:
        se = Season.objects.get(id = season)
        se1 = se.name
        dis_buy1 = Sampling.objects.filter(Q(c_status="Under 2nd Submit")& Q(season = se)).exclude(technique = "Rotary")|Sampling.objects.filter(Q(c_status = "Under 3rd Submit")& Q(season = se))|Sampling.objects.filter(Q(c_status = "Under 4th Submit")& Q(season = se))|Sampling.objects.filter(Q(c_status = "Under 5th Submit")& Q(season = se))
    else:
        br = Buyer.objects.get(id=buyer)
        se = Season.objects.get(id = season)
        se1 = se.name
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status="Under 2nd Submit")& Q(season = se)& Q(buyer = br)).exclude(technique = "Rotary")|Sampling.objects.filter(Q(c_status = "Under 3rd Submit")& Q(season = se)& Q(buyer = br))|Sampling.objects.filter(Q(c_status = "Under 4th Submit")& Q(season = se)& Q(buyer = br))|Sampling.objects.filter(Q(c_status = "Under 5th Submit")& Q(season = se)& Q(buyer = br))
    try:
        supplier = Supplier.objects.get(user=request.user)
        dis_buy1 = dis_buy1.filter(supplier=supplier)
    except:
        pass
    d ={'error':error, 'prod':dis_buy1,'sea':se1,'buy':br1}
    return render(request, 'under_redo_sample_dash_admin.html', d)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def drop_sample_dash_admin(request,season,buyer):
    error = get_group(request.user.id)
    season = season
    buyer = buyer
    supplier = None
    dis_buy1 = ""
    se1 = "All"
    br1 = "All"
    if season == 0 and buyer == 0:
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="drop"))
    elif season == 0 and buyer != 0:
        br = Buyer.objects.get(id=buyer)
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="drop")& Q(buyer = br))
    elif season!=0 and buyer==0:
        se = Season.objects.get(id = season)
        se1 = se.name
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="drop")& Q(season = se))
    else:
        br = Buyer.objects.get(id=buyer)
        se = Season.objects.get(id = season)
        se1 = se.name
        br1 = br.user.username
        dis_buy1 = Sampling.objects.filter(Q(c_status__icontains="drop")& Q(season = se)& Q(buyer = br))
    try:
        supplier = Supplier.objects.get(user=request.user)
        dis_buy1 = dis_buy1.filter(supplier=supplier)
    except:
        pass
    d ={'error':error, 'prod':dis_buy1,'sea':se1,'buy':br1}
    return render(request, 'drop_sample_dash_admin.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM', 'Buyer', 'Supplier'])
def all_sample_dash_admin(request):
    error = get_group(request.user.id)
    all_sample_sea = int(request.GET.get('all_sample_sea',0))
    all_sample_buy = int(request.GET.get('all_sample_buy',0))
    supplier = None
    
    dis_buy1 = ""
    se1 = "All"
    br1 = "All"
    dis_buy1 = Sampling.objects.all().exclude(c_status = None)
    if all_sample_sea:
        se1 = Season.objects.get(id=all_sample_sea)
        dis_buy1 = dis_buy1.filter(season=se1)
    if all_sample_buy:
        br1 = Buyer.objects.get(id=all_sample_buy)
        dis_buy1 = dis_buy1.filter(buyer=br1)
    try:
        supplier = Supplier.objects.get(user=request.user)
        dis_buy1 = dis_buy1.filter(supplier=supplier)
    except:
        pass
    d ={'error':error, 'prod':dis_buy1, 'sea':se1, 'buy':br1}
    return render(request, 'all_sample_dash_admin.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def latest_greige(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=1)
    gre = Griege_Status.objects.filter(g_date = date1)
    d = {'gre':gre,'error':error}
    return render(request,'latest_greige.html',d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def latest_printed(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=1)
    gre = Bulk_Printed.objects.filter(pr_date = date1)
    d = {'gre':gre,'error':error}
    return render(request,'latest_print.html',d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def latest_checking(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=1)
    gre = Fabric_Cheking.objects.filter(f_date = date1)
    d = {'gre':gre,'error':error}
    return render(request,'latest_checking.html',d)
    
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def latest_dispatch(request):
    error = get_group(request.user.id)
    gre = Dispatch_Detail.objects.filter(c_date = (datetime.date.today()-timedelta(days=1)))
    sup = Supplier.objects.all()
    if request.method == "POST":
        try:
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            i1= datetime.datetime.fromisoformat(d1)
            i2= datetime.datetime.fromisoformat(d2)
            gre = Dispatch_Detail.objects.filter(d_date__gte = datetime.date(i1.year,i1.month,i1.day),d_date__lte = datetime.date(i2.year,i2.month,i2.day))
        except:
            pass
        try:
            d = request.POST['date1']
            d1 = datetime.datetime.fromisoformat(d)
            day1 = datetime.date.today() - datetime.date(d1.year,d1.month,d1.day)
            yes = datetime.date.today() - timedelta(days=day1.days)
            li = []
            li2 = []
            for i in Dispatch_Detail.objects.filter(d_date=yes):
                to = i.buyer.user.email
                t=i.buyer.additional_email
                if not i.buyer.user.username in li:
                    li.append(i.buyer.user.username)
                    delv = Dispatch_Detail.objects.filter(d_date=yes,buyer=i.buyer)
                    to2 = []
                    if "," in t:
                        to2 = t.split(",")
                    else:
                        to2.append(t)
                    to2.append(to)
                    task = "Bulk Dispatched Detail"
                    terror = True
                    from_email = settings.EMAIL_HOST_USER
                    sub = task
                    msg = EmailMultiAlternatives(sub, '', from_email, to2)
                    
                    d ={'del': len(delv), 'prod': delv, 'task': task, 'date': yes,'name':i.buyer.user.username}
                    html = get_template('email.html').render(d)
                    msg.attach_alternative(html, 'text/html')
                    if len(delv) > 0:
                        msg.send()
            for i in Dispatch_Detail.objects.filter(d_date=yes):
                to = i.gmt.user.email
                if not i.gmt.user.username in li2:
                    li2.append(i.gmt.user.username)
                    delv = Dispatch_Detail.objects.filter(d_date=yes,gmt=i.gmt)
                    to2 = []
                    to2.append(to)
                    task = "Bulk Dispatched Detail"
                    terror = True
                    from_email = settings.EMAIL_HOST_USER
                    sub = task
                    msg = EmailMultiAlternatives(sub, '', from_email, to2)
                    
                    d ={'del': len(delv), 'prod': delv, 'task': task, 'date': yes,'name':i.gmt.user.username}
                    html = get_template('email.html').render(d)
                    msg.attach_alternative(html, 'text/html')
                    if len(delv) > 0:
                        msg.send()

        except:
            pass
    d = {'gre':gre,'error':error,'sup':sup}
    return render(request,'latest_dispatch.html',d)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def pending_greige(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=0)
    gre = Bulk_Order.objects.filter(gre_date__lte = date1)
    d = {'gre':gre,'error':error}
    return render(request,'pending_greige.html',d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def pending_printed(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=0)
    gre = Bulk_Order.objects.filter(print_date__lte = date1)
    d = {'gre':gre,'error':error}
    return render(request,'pending_printed.html',d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])
def pending_checking(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=0)
    gre = Bulk_Order.objects.filter(checking_date__lte = date1)
    d = {'gre':gre,'error':error}
    return render(request,'pending_checking.html',d)
    
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])  
def pending_dispatch(request):
    error = get_group(request.user.id)
    date1 = datetime.date.today() - timedelta(days=0)
    gre = Bulk_Order.objects.filter(dispatch_date__lte = date1)
    d = {'gre':gre,'error':error}
    return render(request,'pending_dispatch_admin.html',d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])  
def supplier_summary(request):
    error = get_group(request.user.id)
    sup1 = ""
    sea = Season.objects.all()
    month_li = ['All','January','February','March','April','May','June','July','August','September','October','November','December']
    t_bulk = 0
    t_sample= 0
    t_qty = 0
    sup2 = SummarySupplier.objects.all()
    if request.method == "POST":
        s = request.POST['sea']
        m = request.POST['mon']
        if m == "All":
            m=""
        sup1 = Season.objects.get(name=s)
        for i in sup2:
            t_bulk = Bulk_Order.objects.filter(season=sup1,sup=Supplier.objects.get(user=User.objects.get(username=i)),status1="Accept",bpm__icontains=m).count()
            t_qty1 = Bulk_Order.objects.filter(season=sup1,sup=Supplier.objects.get(user=User.objects.get(username=i)),status1="Accept",bpm__icontains=m)
            t_sample = Sampling.objects.filter(season=sup1,supplier=Supplier.objects.get(user=User.objects.get(username=i))).count()
            t_dispatch = 0
            t_dispatch2 = 0
            for j in t_qty1:
                try:
                    t_dispatch3 = Dispatch_Detail.objects.get(bulk=j)
                    if t_dispatch3.dis_qty is not None:
                        t_dispatch2 += 1
                        t_dispatch += float(t_dispatch3.dis_qty)
                except:
                    pass
            i.t_dispatch = t_dispatch2
            i.t_dispatch_qty = t_dispatch
            i.t_sample = t_sample
            i.t_bulk = t_bulk
            i.save()
            if t_qty1:
                i.t_qty = int(float(str(t_qty1.aggregate(Sum('qunt')).values())[13:][:-2]))
                i.save()
            else:
                i.t_qty = 0
                i.save()
    d = {'error':error,'t_bulk':t_bulk,'t_qty':t_qty,'t_sample':t_sample,'sea':sea,'sup2':sup2,'sup1':sup1,'month_li':month_li}
    return render(request,'supplier_summary.html',d)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])  
def buyer_summary(request):
    error = get_group(request.user.id)
    sup1 = ""
    sea = Season.objects.all()
    month_li = ['All','January','February','March','April','May','June','July','August','September','October','November','December']
    t_bulk = 0
    t_sample= 0
    t_qty = 0
    sup2 = SummaryBuyer.objects.all()
    if request.method == "POST":
        s = request.POST['sea']
        m = request.POST['mon']
        if m == "All":
            m=""
        sup1 = Season.objects.get(name=s)
        for i in sup2:
            t_bulk = Bulk_Order.objects.filter(season=sup1,buy=Buyer.objects.get(user=User.objects.get(username=i)),status1="Accept",bpm__icontains=m).count()
            t_qty1 = Bulk_Order.objects.filter(season=sup1,buy=Buyer.objects.get(user=User.objects.get(username=i)),status1="Accept",bpm__icontains=m)
            t_sample = Sampling.objects.filter(season=sup1,buyer=Buyer.objects.get(user=User.objects.get(username=i))).count()
            t_dispatch = 0
            t_dispatch2 = 0
            for j in t_qty1:
                try:
                    t_dispatch3 = Dispatch_Detail.objects.get(bulk=j)
                    if t_dispatch3.dis_qty is not None:
                        t_dispatch2 += 1
                        t_dispatch += float(t_dispatch3.dis_qty)
                except:
                    pass
            i.t_dispatch = t_dispatch2
            i.t_dispatch_qty = t_dispatch
            i.t_sample = t_sample
            i.t_bulk = t_bulk
            i.save()
            if t_qty1:
                i.t_qty = int(float(str(t_qty1.aggregate(Sum('qunt')).values())[13:][:-2]))
                i.save()
            else:
                i.t_qty = 0
                i.save()
    d = {'error':error,'t_bulk':t_bulk,'t_qty':t_qty,'t_sample':t_sample,'sea':sea,'sup2':sup2,'sup1':sup1,'month_li':month_li}
    return render(request,'buyer_summary.html',d)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RM'])    
def sampling_status(request):
    error = get_group(request.user.id)
    data = Sampling.objects.all().exclude(technique = "Adhoc")
    for i in data:
        i.time_in_develop = 0
        i.time_in_approve = 0
        i.save()
        time_in_develop = 0
        cour = Courier_Detail.objects.filter(sample = i)
        if cour:
            count = 1
            if i.count == 1:
                latest = Courier_Detail.objects.filter(sample = i).first()
            else:
                latest = None
            for j in cour:
                if i.doe:
                    if i.count == count:
                        if not j.rep_date:
                            d1 = i.doe
                            d2 = j.sent_on
                            d4 = d1 - d2
                            d3 = time_in_develop
                            time_in_develop = int(d3) + int(d4.days)
                            break
                        else:
                            if latest.rep_date:
                                d1 = latest.rep_date
                                d2 = j.sent_on
                                d4 = d2 - d1
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                break
                            else:
                                d1 = latest.sent_on
                                d2 = j.sent_on
                                d4 = d2 - d1
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                break
                    else:
                        if count == 1:
                            d1 = i.dos
                            d2 = j.sent_on
                            d4 = d2 - d1
                            d3 = time_in_develop
                            time_in_develop = int(d3) + int(d4.days)
                            latest = j
                        else:
                            if latest.rep_date:
                                d1 = latest.rep_date
                                d2 = j.sent_on
                                d4 = d2 - d1
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                latest = j
                            else:
                                d1 = i.doe
                                d2 = j.sent_on
                                d4 = d1 - d2
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                latest = j
                else:
                    if i.count == count:
                        if not j.rep_date:
                            d1 = datetime.date.today()
                            d2 = j.sent_on
                            d4 = d1 - d2
                            d3 = time_in_develop
                            time_in_develop = int(d3) + int(d4.days)
                            break
                        else:
                            if latest.rep_date:
                                d1 = latest.rep_date
                                d2 = j.sent_on
                                d4 = d2 - d1
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                break
                            else:
                                d1 = latest.sent_on
                                d2 = j.sent_on
                                d4 = d2 - d1
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                break
                    else:
                        if count == 1:
                            d1 = i.dos
                            d2 = j.sent_on
                            d4 = d2 - d1
                            d3 = time_in_develop
                            time_in_develop = int(d3) + int(d4.days)
                            latest = j
                        else:
                            if latest.rep_date:
                                d1 = latest.rep_date
                                d2 = j.sent_on
                                d4 = d2 - d1
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                latest = j
                            else:
                                d1 = datetime.date.today()
                                d2 = j.sent_on
                                d4 = d1 - d2
                                d3 = time_in_develop
                                time_in_develop = int(d3) + int(d4.days)
                                latest = j
                count+=1
            i.time_in_develop = time_in_develop
            i.save()
        else:
            if i.doe:
                d1 = i.dos
                if d1:
                    d2 = i.doe
                    d4 = d2 - d1
                    d3 = i.time_in_develop
                    i.time_in_develop = int(d3) + int(d4.days)
                    i.save()
            else:
                d1 = i.dos
                if d1:
                    d2 = datetime.date.today()
                    d4 = d2 - d1
                    d3 = i.time_in_develop
                    i.time_in_develop = int(d3) + int(d4.days)
                    i.save()
    d = {"data":data,'error':error}
    return render(request,'sampling_status.html',d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def View_Sampling_uncomplete(request):
    error = get_group(request.user.id)
    buy = Sampling.objects.filter(Q(c_status="Under 2nd Submit") & Q(technique="Rotary") & Q(count="1"))
    d ={'error':error,'prod': buy}
    return render(request, 'View_Sampling_uncomplete.html', d)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Sampling_Admin(request,id):
    error = get_group(request.user.id)
    sam = Sampling.objects.get(id=id)
    season = Season.objects.all()
    drop = Drop.objects.all()
    product = Product.objects.all()
    supplier = Supplier.objects.all()
    if request.method == 'POST':
        d = request.POST['design']
        c = request.POST['color']
        s = request.POST['season']
        dos = request.POST['dos']
        
        try:
            i = request.FILES['image']
            sam.image = i
            sam.save()
        except:
            pass
        sam.design_name = d
        sam.color_name = c
        sam.dos = dos
        
        sam.save()
        messages.success(request, 'Data Updated Successfully')
        return redirect("all_sampling")
    d = {'sam': sam,'error':error, 'season':season, 'drop':drop, 'product':product,'supplier':supplier}    
    return render(request, 'update_sampling_admin.html',d)
    
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'RM'])
# def Update_Sampling_Admin(request,id):
#     error = get_group(request.user.id)
#     sampling = Sampling.objects.get(id =id)
#     form = SamplingForm(instance = sampling)
#     if request.method == 'POST':
#         form = SamplingForm(request.POST,request.FILES, instance = sampling)
#         if form.is_valid():
#             form.save()
#             return redirect(/)
    
#     return render(request, 'update_sampling_admin.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'RM'])
def Update_Disptch_Admin(request, id):
    error = get_group(request.user.id)
    sam = Bulk_Order.objects.get(id=id)
    dis = Dispatch_Detail.objects.get(bulk=sam)
    if request.method =='POST':
        s = request.POST['dis']
        d = request.POST['date']
        t = request.POST['tr_name']
        l = request.POST['tr_name']
        dis.dis_qty = s
        dis.d_date = d
        dis.tr_name = t
        dis.lr_no = l
        sam.c_status = "Dispatched"
        sam.save()
        dis.save()
        return redirect("pending_dispatch")
    d = {'error': error,'sam':sam}
    return render(request, 'update_dispatch.html',d)