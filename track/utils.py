from .models import Sampling, Buyer, Season, Bulk_Order, Supplier
from django.db.models import Sum,Max
from django.db.models import Q

def sampling_summary_fn(request):
    season, buyer = None,None
    season1 = request.POST.get('sea1',0)
    buyer1 = request.POST.get('buy1',0)
    supplier1 = request.POST.get('sup1',0)
    try:
        supplier = Supplier.objects.get(user = request.user)
        supplier1 = supplier.id
    except:
        pass
    
    try:
        buyer = Buyer.objects.get(user = request.user)
        buyer1 = buyer.id
    except:
        pass
    
    total_sampling = Sampling.objects.all().exclude(c_status = None)
    
    ######    Approved Sampling   #########
    approved_sampling = Sampling.objects.filter(c_status = "Approved")
    
    ### Under Development Sampling ###
    ud_sampling = Sampling.objects.filter(c_status__in =["Under 1st Submit", "Under 2nd Submit"]).exclude(technique__in=["Solid","Digital","Adhoc"])
    
    ### Under Approval Sampling ###
    ua_sampling = Sampling.objects.filter(c_status__icontains = "approval")
    
    ### Under REDO ###
    urd_sampling = Sampling.objects.filter(Q(c_status="Under 2nd Submit")).exclude(technique = "Rotary")|Sampling.objects.filter(Q(c_status = "Under 3rd Submit"))|Sampling.objects.filter(Q(c_status = "Under 4th Submit"))|Sampling.objects.filter(Q(c_status = "Under 5th Submit"))
            
    ### Under DROP ###
    drp_sampling = Sampling.objects.filter(c_status__icontains = "drop")
    
    if int(season1):
        season1 = int(season1)
        season = Season.objects.get(id = season1)
        total_sampling = total_sampling.filter(season = season)
        approved_sampling = approved_sampling.filter(season = season)
        ud_sampling =ud_sampling.filter(season = season)
        ua_sampling = ua_sampling.filter(season = season)
        urd_sampling = urd_sampling.filter(season = season)
        drp_sampling = drp_sampling.filter(season = season)
    
    if int(buyer1):
        buyer1 = int(buyer1)
        buyer = Buyer.objects.get(id = buyer1)
        total_sampling = total_sampling.filter(buyer = buyer)
        approved_sampling = approved_sampling.filter(buyer = buyer)
        ud_sampling =ud_sampling.filter(buyer = buyer)
        ua_sampling = ua_sampling.filter(buyer = buyer)
        urd_sampling = urd_sampling.filter(buyer = buyer)
        drp_sampling = drp_sampling.filter(buyer = buyer)
        
    if int(supplier1):
        supplier1 = int(supplier1)
        supplier = Supplier.objects.get(id = supplier1)
        total_sampling = total_sampling.filter(supplier = supplier)
        approved_sampling = approved_sampling.filter(supplier = supplier)
        ud_sampling =ud_sampling.filter(supplier = supplier)
        ua_sampling = ua_sampling.filter(supplier = supplier)
        urd_sampling = urd_sampling.filter(supplier = supplier)
        drp_sampling = drp_sampling.filter(supplier = supplier)
        
    return [total_sampling.count(), approved_sampling.count(), ud_sampling.count(), ua_sampling.count(), urd_sampling.count(), drp_sampling.count(), season1, buyer1, supplier1]
    
    
    
    

def bulk_summary_fn(request):
    season1 = request.POST.get('sea1',0)
    buyer1 = request.POST.get('buy1',0)
    supplier1 = request.POST.get('sup1',0)
    try:
        supplier = Supplier.objects.get(user = request.user)
        supplier1 = supplier.id
    except:
        pass
    
    try:
        buyer = Buyer.objects.get(user = request.user)
        buyer1 = buyer.id
    except:
        pass
    pass
    
    ### Total Qty ###
    total_qty = Bulk_Order.objects.filter(status1="Accept")
    
    dispatch_qty = Bulk_Order.objects.filter(status1="Accept", c_status__in = ["Dispatched", "Complete"])

    packed_qty = Bulk_Order.objects.filter(status1="Accept", c_status__in = ["Packed", "FOB Sent"])
    
    up_qty = Bulk_Order.objects.filter(status1="Accept", c_status__in = ["Greige Issued", "Bulk Printed","Under development", "Order Not Started"])
    
    ontime_qty = Bulk_Order.objects.filter(status1="Accept", time_status = "On Time", c_status__in = ["Greige Issued", "Bulk Printed","Under development", "Order Not Started"])
    
    delayed_qty = Bulk_Order.objects.filter(status1="Accept", time_status = "Delayed", c_status__in = ["Greige Issued", "Bulk Printed","Under development", "Order Not Started"])
    
    if int(season1):
        season1 = int(season1)
        season = Season.objects.get(id = season1)
        total_qty = total_qty.filter(season=season)
        dispatch_qty = dispatch_qty.filter(season=season)
        
        packed_qty= packed_qty.filter(season=season)
        
        up_qty= up_qty.filter(season=season)
        
        ontime_qty = ontime_qty.filter(season=season)
        
        delayed_qty = delayed_qty.filter(season=season)
        
        
    if int(supplier1):
        supplier1 = int(supplier1)
        supplier = Supplier.objects.get(id = supplier1)
        total_qty = total_qty.filter(sup=supplier)
        dispatch_qty = dispatch_qty.filter(sup=supplier)
        
        packed_qty= packed_qty.filter(sup=supplier)
        
        up_qty= up_qty.filter(sup=supplier)
        
        ontime_qty = ontime_qty.filter(sup=supplier)
        
        delayed_qty = delayed_qty.filter(sup=supplier)
        
    if int(buyer1):
        buyer1 = int(buyer1)
        buyer = Buyer.objects.get(id = buyer1)
        total_qty = total_qty.filter(buy=buyer)
        dispatch_qty = dispatch_qty.filter(buy=buyer)
        
        packed_qty= packed_qty.filter(buy=buyer)
        
        up_qty= up_qty.filter(buy=buyer)
        
        ontime_qty = ontime_qty.filter(buy=buyer)
        
        delayed_qty = delayed_qty.filter(buy=buyer)
    
    total_qty_count, dispatch_qty_count, packed_qty_count, up_qty_count, ontime_qty_count, delayed_qty_count = 0, 0, 0, 0, 0, 0
    if total_qty:
        total_qty_count = int(float(str(total_qty.aggregate(Sum('qunt')).values())[13:][:-2]))
    total_qty_option = total_qty.count()
    
    if dispatch_qty:
        dispatch_qty_count = int(float(str(dispatch_qty.aggregate(Sum('qunt')).values())[13:][:-2]))
    dispatch_qty_option = dispatch_qty.count()
    
    if packed_qty:
        packed_qty_count = int(float(str(packed_qty.aggregate(Sum('qunt')).values())[13:][:-2]))
    packed_qty_option = packed_qty.count()
    
    if up_qty:
        up_qty_count = int(float(str(up_qty.aggregate(Sum('qunt')).values())[13:][:-2]))
    up_qty_option = up_qty.count()
    
    if ontime_qty:
        ontime_qty_count = int(float(str(ontime_qty.aggregate(Sum('qunt')).values())[13:][:-2]))
    ontime_qty_option = ontime_qty.count()
    
    if delayed_qty:
        delayed_qty_count = int(float(str(delayed_qty.aggregate(Sum('qunt')).values())[13:][:-2]))
    delayed_qty_option = delayed_qty.count()
            
    return [total_qty_count, total_qty_option, dispatch_qty_count, dispatch_qty_option, packed_qty_count, packed_qty_option, up_qty_count, up_qty_option, ontime_qty_count, ontime_qty_option, delayed_qty_count, delayed_qty_option]

        
    