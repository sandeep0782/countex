from django.db import models
from django.contrib.auth.models import User
from PIL import Image

technique=[('Solid','Solid'),
('Rotary','Rotary'),
('Digital','Digital'),
('Yarn Dyed','Yarn Dyed'),
('Adhoc','Adhoc'),
]
# Create your models here.
class Search_for_date(models.Model):
    dat = models.DateField(null=True, blank=True)


class Status(models.Model):
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.status


class Season(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=30, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Drop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=30, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=30, null=True, blank=True)
    count = models.CharField(max_length=100, null=True, blank=True)
    construction = models.CharField(max_length=100, null=True, blank=True)
    gsm = models.CharField(max_length=100, null=True, blank=True)
    weave = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)
    moq = models.CharField(max_length=100, null=True, blank=True)
    leadtime = models.CharField(max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    solid_rate = models.CharField(max_length=100, null=True, blank=True)
    printed_rate = models.CharField(max_length=100, null=True, blank=True)
    digital_rate = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    additional_email = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class GMT_Vendor(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    

    def __str__(self):
        return self.user.first_name


class Supplier(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    update_perm = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    additional_email = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

class RM(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    additional_email = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name


class UpToDate(models.Model):
    active = models.BooleanField(default=False)
    up_to_date = models.DateField(null=True, blank=True)

import datetime
class Sampling(models.Model):
    active = models.BooleanField(default=False)
    design_name = models.CharField(max_length=100, null=True, blank=True)
    color_name = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    status1 = models.CharField(max_length=100, null=True, blank=True)
    c_status = models.CharField(max_length=100, null=True, blank=True)
    time_status = models.CharField(max_length=100, null=True, blank=True)
    time_status2 = models.CharField(max_length=100, null=True, blank=True)
    c_table = models.CharField(max_length=100, null=True, blank=True)
    status_buyer = models.CharField(max_length=100, null=True, blank=True)
    courier_name = models.CharField(max_length=100, null=True, blank=True)
    awb_no = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True,default=0, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    buyer_message = models.CharField(max_length=800, null=True, blank=True)
    sent_on = models.DateField(null=True, blank=True)
    dos = models.DateField(null=True, blank=True)
    doe = models.DateField(null=True, blank=True)
    timetaken = models.CharField(max_length=100, null=True, blank=True)
    del_date = models.DateField(null=True, blank=True)
    first = models.DateField(null=True, blank=True)
    second = models.DateField(null=True, blank=True)
    third = models.DateField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    technique = models.CharField(max_length=100,choices=technique, null=True, blank=True)
    time_in_develop = models.CharField(max_length=100, null=True, blank=True,default="0")
    time_in_approve = models.CharField(max_length=100, null=True, blank=True,default="0")
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 100 or img.weight > 100:
                output_size = (100, 100)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except:
            pass
    
    def total_day(self):
        to_date = datetime.date.today()
        if self.doe:
            return int((self.doe - self.dos).days)
        else:
            return int((to_date - self.dos).days)
        
    def time_taken_approval(self):
        doe = self.doe
        rep_date = Courier_Detail.rep_date
        to_date = datetime.date.today()
        total = 0
        count = 1
        prev = None
        for i in Courier_Detail.objects.filter(sample=self):
            if i.sent_on and i.rep_date:
                total += int((i.rep_date - i.sent_on).days)
            else:
                diff = int((to_date - i.sent_on).days)
                total+= diff
        return total
        
    def time_taken_developement(self):
        return self.total_day() - self.time_taken_approval()
    
    def time_status(self):
        count = 1
        f1 = None
        f2 = None
        f3 = None
        for i in Courier_Detail.objects.filter(sample = self):
            if count==1:
                f1 = i
            if count==2:
                f2 = i
            if count==3:
                f3 = i
                break
            count+=1
        
        ft1 = self.first
        ft2 = self.second
        ft3 = self.third
        to_date = datetime.date.today()
        if f3:
            if ft3:
                if ft3 < f3.sent_on:
                    return "Delay"
                else:
                    return "On Time"
        
        
        if f2:
            if ft3:
                if ft3 < to_date:
                    return "Delay"
                elif ft2:
                    if ft2 < f2.sent_on:
                        return "Delay"
                    else:
                        return "On Time"
        
        
        
        if f1:
            if ft2:
                if ft2 < to_date:
                    return "Delay"
            elif ft1:
                if ft1 < f1.sent_on:
                    return "Delay"
                else:
                    return "On Time"
        
        else:
            if ft1:
                if to_date > ft1:
                    return "Delay"
                else:
                    return "On Time"
        return "None Date"
            
        def __str__(self):
            return str(self.design_name)


class Courier_Detail(models.Model):
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    sample = models.ForeignKey(Sampling, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    awb_no = models.CharField(max_length=100, null=True, blank=True)
    buyer_message = models.CharField(max_length=1000, null=True, blank=True)
    sent_on = models.DateField(null=True, blank=True)
    rep_date = models.DateField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    c_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.sample.design_name + " " + self.sample.buyer.user.username + " " + self.sample.supplier.user.username  


class Bulk_Order(models.Model):
    active = models.BooleanField(default=False)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status1 = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    time_status = models.CharField(max_length=100, null=True, blank=True)
    c_status = models.CharField(max_length=100, null=True, blank=True)
    sample = models.ForeignKey(Sampling, on_delete=models.CASCADE, null=True, blank=True)
    sup = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    buy = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    print_tech = models.CharField(max_length=100, null=True, blank=True)
    style = models.CharField(max_length=100, null=True, blank=True)
    qunt = models.CharField(max_length=100, null=True, blank=True)
    rate = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    gmt_vendor = models.CharField(max_length=100, null=True, blank=True)
    del_date = models.DateField(null=True, blank=True)
    dupl_del_date = models.CharField(max_length=100, null=True, blank=True)
    dos = models.DateField(null=True, blank=True)
    doe = models.DateField(null=True, blank=True)
    bpm = models.CharField(max_length=100, null=True, blank=True)
    pid = models.IntegerField(null=True,default=0, blank=True)
    bpmstatus = models.CharField(max_length=100, null=True, blank=True)
    gre_date = models.DateField(null=True, blank=True)
    print_date = models.DateField(null=True, blank=True)
    checking_date = models.DateField(null=True, blank=True)
    dispatch_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id)+" "+self.sample.design_name
        
    def bulk_time_status(self):
        d1 = None
        d2 = None
        d3 = None
        d4 = None
        to_d = datetime.date.today()
        try:
            gr_d = Griege_Status.objects.get(bulk = self)
            d1 = gr_d.g_date
        except:
            pass
        try:
            gr_d = Bulk_Printed.objects.get(bulk = self)
            d2 = gr_d.pr_date
        except:
            pass
        try:
            gr_d = Fabric_Cheking.objects.get(bulk = self)
            d3 = gr_d.f_date
        except:
            pass
        try:
            gr_d = Dispatch_Detail.objects.get(bulk = self)
            d4 = gr_d.d_date
        except:
            pass
        
        if d4:
            if self.dispatch_date:
                if d4 > self.dispatch_date:
                    return "Delay"
                else:
                    return "On Time"
        
        if d3:
            if self.dispatch_date:
                if self.dispatch_date < to_d:
                    return "Delay"
                elif self.checking_date:
                    if d3 > self.checking_date:
                        return "Delay"
                    else:
                        return "On Time"
        
        if d2:
            if self.checking_date:
                if self.checking_date < to_d:
                    return "Delay"
                elif self.print_date:
                    if d2 > self.print_date:
                        return "Delay"
                    else:
                        return "On Time"
        
        if d1:
            if self.print_date:
                if self.print_date < to_d:
                    return "Delay"
                elif self.gre_date:
                    if d1 > self.gre_date:
                        return "Delay"
                    else:
                        return "On Time"
        else:
            if self.gre_date:
                if to_d > self.gre_date:
                    return "Delay"
                else:
                    return "On Time"
        return "None Date"
        

class Griege_Status(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    g_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username


class Bulk_Printed(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    pr_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username



class FirstBulk(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    awb_no = models.CharField(max_length=100, null=True, blank=True)
    courier_name = models.CharField(max_length=100, null=True, blank=True)
    f_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username


class FPT_Status(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    rep_no = models.CharField(max_length=100, null=True, blank=True)
    report = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username


class Fabric_Cheking(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    qty_pass = models.CharField(max_length=100, null=True, blank=True)
    qty_reject = models.CharField(max_length=100, null=True, blank=True)
    f_date = models.DateField(null=True, blank=True)
    report = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username


class Dispatch_Detail(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True, blank=True)
    dis_qty = models.CharField(max_length=100, null=True, blank=True)
    tr_name = models.CharField(max_length=100, null=True, blank=True)
    lr_no = models.CharField(max_length=100, null=True, blank=True)
    d_date = models.DateField(null=True, blank=True)
    report = models.FileField(null=True, blank=True)
    c_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username


class Payment_Status(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bulk = models.ForeignKey(Bulk_Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    p_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.bulk.sample.design_name + " " + self.bulk.sample.buyer.user.username + " " + self.bulk.sample.supplier.user.username
        
class SummarySupplier(models.Model):
    gmt = models.ForeignKey(GMT_Vendor, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, null=True, blank=True)
    t_sample = models.CharField(max_length=100,null=True,blank=True)
    t_bulk = models.CharField(max_length=100,null=True,blank=True)
    t_qty = models.CharField(max_length=100,null=True,blank=True)
    t_dispatch = models.CharField(max_length=100,null=True,blank=True)
    t_dispatch_qty = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.supplier.user.username

class SummaryBuyer(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    rm = models.ForeignKey(RM, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE, null=True, blank=True)
    t_sample = models.CharField(max_length=100,null=True,blank=True)
    t_bulk = models.CharField(max_length=100,null=True,blank=True)
    t_qty = models.CharField(max_length=100,null=True,blank=True)
    t_dispatch = models.CharField(max_length=100,null=True,blank=True)
    t_dispatch_qty = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.buyer.user.username


