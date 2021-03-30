from track.models import Sampling,Bulk_Order,Supplier,Buyer
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
from datetime import timedelta
from django.contrib import messages
from dateutil import parser


def sampling_report(request):
    buyer=request.GET.get('report',"0")
    try:
        buyer1 = Buyer.objects.get(id=int(buyer))
    except:
        pass
    if buyer == "0":
        obj = Sampling.objects.all()
        obj = {'obj':obj,"selected_id":int(buyer)}
        return obj
    else:
        obj = Sampling.objects.filter(buyer = buyer1)
        obj = {'obj':obj,"selected_id":int(buyer)}
        return obj

def view_sampling_report(request):
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
            ed= sd - timedelta(days=90)
        if n:
            user = User.objects.get(username__icontains=n)
            try:
                user = User.objects.get(username__icontains=n)
                try:
                    buy = Buyer.objects.get(user=user)
                    samplings = Sampling.objects.filter(Q(buyer=buy) & Q(dos__range=[ed,sd])).exclude(Q(status="Close") | Q(status="Complete"))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,buyer=buy).exclude(Q(status="Close") | Q(status="Complete"))
                except:
                    buy = Supplier.objects.get(user=user)
                    samplings = Sampling.objects.filter(Q(supplier=buy) & Q(dos__range=[ed,sd])).exclude(Q(status="Close") | Q(status="Complete"))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed,supplier=buy).exclude(Q(status="Close") | Q(status="Complete"))
            except:
                try:
                    samplings = Sampling.objects.filter(Q(design_name__icontains=n) & Q(dos__range=[ed,sd])).exclude(Q(status="Close") | Q(status="Complete"))|Sampling.objects.filter(design_name__icontains=n).exclude(Q(status="Close") | Q(status="Complete"))
                    if not samplings:
                        messages.success(request,'Please Elaborate your search criteria.')
                except:
                    pass
        else:
            samplings = Sampling.objects.filter(dos__range=[ed,sd]).exclude(Q(status="Close") | Q(status="Complete"))|Sampling.objects.filter(dos__gte=sd,dos__lte=ed).exclude(Q(status="Close") | Q(status="Complete"))
    return samplings
    

def bulk_report(request):
    if request.method == "POST":
        n = request.POST['search']
        sd = None
        ed = None
        sampling = Bulk_Order.objects.filter(status1="Accept")
        try:
            sd = request.POST['sdate']
            ed = request.POST['edate']
            sampling = sampling.filter(dos__gte=sd,dos__lte=ed)
            return sampling
        except:
            pass
        if n:
            try:
                user = User.objects.get(username__icontains=n)
                buy = Buyer.objects.get(user=user)
                sampling = sampling.filter(buy=buy)
                return sampling
            except:
                try:
                    user = User.objects.get(username__icontains=n)
                    buy = Supplier.objects.get(user=user)
                    sampling = sampling.filter(sup=buy)
                    return sampling
                except:
                    try:
                        sampling = sampling.filter(sample__design_name__icontains=n)
                        if sampling:
                            return sampling
                        else:
                            messages.success(request,'Please Elaborate your search criteria.')
                    except:
                        messages.success(request,'Please Elaborate your search criteria.')
            
        return sampling

def pending_bulk_report(request):
    sample = Bulk_Order.objects.filter(status1="pending")
    return sample
    
def create_order_manually(request):
    li  = []
    bulk = Bulk_Order.objects.filter(status1="pending")
    for i in bulk:
        li.append(i.sample.id)
    samplings = Sampling.objects.filter(c_status="Approved",status="Complete")
    obj = {'samplings':samplings,'li':li}
    return obj
    
    


report_dict = {
    "sampling report":{"template_name":"sampling_report.html", "method":sampling_report},
    "bulk report":{"template_name":"view_bulk_admin.html", "method":bulk_report},
    "pending bulk report":{"template_name":"view_pending_bulk.html", "method":pending_bulk_report},
    "create bulk order manually":{"template_name":"Create_Order_Manually.html", "method":create_order_manually},
    "view filtered sampling":{"template_name":"view_sampling.html", "method":view_sampling_report},
    # "campaign report":{"template_name":"myadmin/report/campaign_report.html", "method":campaign_report},
    # "contactlist report":{"template_name":"myadmin/report/contact_list_report.html", "method":contactlist_report},
}