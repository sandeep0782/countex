from django.contrib import admin
from .models import *



# Register your models here.

class Bulk_OrderModel(admin.ModelAdmin):
    list_display = ['id','pid','dos','buy','season','drop','sample','style','sup','print_tech','qunt','rate','value','bpm','bpmstatus','del_date','gmt_vendor','c_status','time_status']
    
class SamplingModel(admin.ModelAdmin):
    list_display = ['id','dos','design_name','rm','color_name','status1','c_status','time_status','time_status2','c_table','awb_no','count','status','doe']

class Courier_DetailModel(admin.ModelAdmin):
    list_display = ['id','sample','awb_no','sent_on','rep_date','buyer_message','c_date']
    
class Fabric_ChekingModel(admin.ModelAdmin):
    list_display = ['id','bulk','qty_pass','qty_reject','f_date']

class FirstBulkModel(admin.ModelAdmin):
    list_display = ['id','bulk']

class Bulk_PrintedModel(admin.ModelAdmin):
    list_display = ['id','bulk']

admin.site.register(Status)
admin.site.register(SummarySupplier)
admin.site.register(SummaryBuyer)
admin.site.register(RM)
admin.site.register(Buyer)
admin.site.register(GMT_Vendor)
admin.site.register(Supplier)
admin.site.register(Season)
admin.site.register(Sampling, SamplingModel)
admin.site.register(Product)
admin.site.register(Drop)
admin.site.register(Courier_Detail, Courier_DetailModel)
admin.site.register(Bulk_Order,Bulk_OrderModel)
admin.site.register(Griege_Status)

admin.site.register(Bulk_Printed,Bulk_PrintedModel)

admin.site.register(FirstBulk,FirstBulkModel)
admin.site.register(FPT_Status)


admin.site.register(Fabric_Cheking, Fabric_ChekingModel)

admin.site.register(Payment_Status)
admin.site.register(Dispatch_Detail)
admin.site.register(UpToDate)



