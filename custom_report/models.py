from django.db import models

# Create your models here.
SAMPLING = [("Sampling","Sampling"), ("Bulk Order","Bulk Order")]
class Report(models.Model):
    report_name = models.CharField(max_length=100,null=True,blank=True)
    report_type = models.CharField(max_length=100,choices=SAMPLING,null=True,blank=True)
    
    def __str__(self):
        return self.report_name

