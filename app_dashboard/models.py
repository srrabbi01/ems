from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from .helper_func import *


class UserRegistration(models.Model):
    registrationType = (
        ('','Please Select'),
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Other', 'Other')
    )

    roleType = (
        ('customer', 'customer'),
        ('admin', 'admin'),
        ('technician', 'technician'),
    )

    user = models.OneToOneField(User, on_delete =models.CASCADE, null=True)
    reg_no = models.BigIntegerField(null=True)
    name = models.CharField(max_length=122, null=True)
    email = models.EmailField(max_length=122, null=True , blank=True)
    phone = models.CharField(max_length=122, null=True)
    other_phone = models.CharField(max_length=122, null=True, blank=True)
    registration_type = models.CharField(max_length=122, choices = registrationType ,null=True, blank=True)
    role = models.CharField(max_length=122, choices = roleType ,null=True, default=roleType[0][0])
    business_name = models.CharField(max_length=122, null=True, blank=True)
    country = models.CharField(max_length=122, null=True, blank=True)
    division = models.CharField(max_length=122, null=True, blank=True)
    district = models.CharField(max_length=122, null=True, blank=True)
    upazila = models.CharField(max_length=122, null=True, blank=True)
    post_office_or_union = models.CharField(max_length=122, null=True, blank=True)
    house_info = models.CharField(max_length=122, null=True, blank=True)
    location = models.CharField(max_length=999, null=True, blank=True)
    nid = models.CharField(max_length=122, null=True, blank=True)
    picture = models.ImageField(upload_to= 'image', null=True, blank=True)
    active = models.BooleanField(default=False,null=True)
    tech_percentage = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def get_role(self):
        return f'{self.role}'



class ServiceCategory(models.Model):
    category_name = models.CharField(max_length= 255, null=True)
    cost = models.FloatField(null=True)

    def __str__(self):
        return f'{self.category_name} -{self.cost}TK'



class ServiceRequest(models.Model):
    priority_choice  = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )
    STATUS_CHOICE = (
        ('New','New'),
        ('Waitting on Customer','Waitting on Customer'),
        ('In Progress','In Progress'),
        ('Fixed','Fixed'),
        ('Closed','Closed'),
        ('Cancelled','Cancelled'),
    )
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    technician = models.ForeignKey(UserRegistration, on_delete=models.SET_NULL, null=True,related_name='technician')
    servicereq_no = models.CharField(max_length=122, null=True)
    title = models.CharField(max_length=250, null=True)
    details = models.TextField(max_length=1000, null=True)
    files = models.FileField(upload_to= 'service_file', null=True, blank=True)
    priority = models.CharField(max_length=122, choices=priority_choice, null=True)
    created_at = models.DateField(auto_now_add=True)
    status =  models.CharField(max_length=122, choices=STATUS_CHOICE, null=True,blank=True,default='new')
    assigned = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.title}'



class Invoice(models.Model):
    PAYMENT_STATUS = (
        ('Paid','Paid'),
        ('Unpaid','Unpaid'),
    )
    service = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True)
    details = models.TextField(max_length=1000, null=True)
    equip_charge = models.FloatField(max_length=250, null=True, blank=True)
    files = models.FileField(upload_to= 'invoice_file', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    status =  models.CharField(max_length=122, choices=PAYMENT_STATUS, null=True,blank=True,default='Unpaid')
    paid = models.BooleanField(default=False,editable=False)
    
    def __str__(self):
        return f'#{self.id}-Invoice-{self.service.title}'
        
    def getTotalCharge(self):
        cost = 0
        if self.service.priority == 'High':
            cost = self.service.service_category.cost*2
        elif self.service.priority == 'Medium':
            cost = self.service.service_category.cost*1.5
        else:
            cost = self.service.service_category.cost
            
        return f'{self.equip_charge + cost}'
    



class CustomerPayment(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.SET_NULL, null=True)
    transition_id = models.CharField(max_length=255, null=True)
    payment_method = models.CharField(max_length=255, null=True)
    payment_date = models.DateField(default=timezone.now)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False,editable=False)

    def _str_(self):
        return f'{self.invoice.id} {self.transition_id}'


class TechnicianPayment(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.SET_NULL, null=True)
    transition_id = models.CharField(max_length=255, null=True)
    payment_method = models.CharField(max_length=255, null=True)
    payment_date = models.DateField(default=timezone.now)
    amount = models.FloatField(default=0, editable=False)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False,editable=False)

    def save(self,*args, **kwargs):
        self.amount = calcAmountFunc(self.invoice.service.service_category.cost,self.invoice.service.technician.tech_percentage)
        return super(TechnicianPayment,self).save(*args, **kwargs)

    def _str_(self):
        return f'{self.invoice.id} {self.transition_id}'


class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    desc = models.TextField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(UserRegistration,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=999999,null=True)
    service_ticket = models.ForeignKey(ServiceRequest,on_delete=models.SET_NULL,null=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        ordering = ['-sent_date']

class TempServiceRequest(models.Model):
    service_title = models.CharField(max_length=255,null=True)
    service = models.ForeignKey(ServiceRequest, on_delete=models.SET_NULL,null=True)
    nearest_tech = models.ForeignKey(UserRegistration,on_delete=models.SET_NULL,null=True)
    rejected_tech_id = models.CharField(max_length=255, null=True, default='')

    def __str__(self):
        return f'{self.service}'


class Review(models.Model):
    service = models.ForeignKey(ServiceRequest, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=500, null=True)
    created_at = models.DateField(auto_now_add=True)

    def _str_(self):
        return f'{self.created_at}'