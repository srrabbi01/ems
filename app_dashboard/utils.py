from datetime import datetime, timedelta
from django.http import HttpResponse
from .models import UserRegistration,ServiceRequest
from django.conf import settings
from django.core.mail import send_mail, EmailMessage,BadHeaderError
from django.template.loader import render_to_string
from geopy.distance import geodesic

def getTicketNo():
    snum = 100001
    obj = ServiceRequest.objects.last()
    if obj and obj.servicereq_no:
        last_t_no = obj.servicereq_no.replace('#', '')
        t_no = int(last_t_no)+1
    else:
        t_no=snum
    return f'#{t_no}'



def getRegnum():
    snum = 100001
    obj = UserRegistration.objects.last()
    if obj:
        rnumber = obj.reg_no+1
    else:
        rnumber=snum
    return rnumber



def accountCreatedNotifyMailFunc(obj):
    subject = 'Account Created'
    message = f'Hi admin, a new EMS account has been created.\nPlease verify and activate the account through the following link http://127.0.0.1:8000/admin/app_dashboard/userregistration/{obj.id}/change/.\nThank you.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['ayon19me@gmail.com', ]
    send_mail( subject, message, email_from, recipient_list )



def activateAccountMailFunc(obj):
    subject = 'Account Activation'
    message = f'Hi {obj.name}, Your Ems account has been activated. You can got to https://efixbd.com and use your account now. Thank you.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [obj.email, ]
    send_mail( subject, message, email_from, recipient_list )



def newServiceNotifyMailFunc(obj):
    subject = 'New Service Created'
    message = f'Hi {obj.name}, A new Service has been created.\nPlease check details for further actions.\nThank you.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [obj.email, ]
    send_mail( subject, message, email_from, recipient_list )



def technicianAssignMail(obj):
    subject = 'New Work Assingment'
    c = {
        'service_no':obj.servicereq_no,
        'service_title':obj.title,
        'customer_name':obj.customer.userregistration.name,
        'customer_phone':obj.customer.userregistration.phone,
        'customer_email':obj.customer.userregistration.email,
        'technician_name':obj.technician.name,
        'technician_phone':obj.technician.phone,
        'technician_email':obj.technician.email,
    }
    text_version = 'mail/service_assigned.txt'
    text_message = render_to_string(text_version,c)

    try:
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL,[obj.technician.email,obj.customer.userregistration.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')



def serviceStatusMail(obj):
    subject = f"{obj.servicereq_no} {obj.title}"
    c = {
        'customer_name':obj.customer.userregistration.name,
        'status':obj.status,
        'technician_name':obj.technician.name,
        'technician_phone':obj.technician.phone,
        'technician_email':obj.technician.email,
    }
    text_version = 'mail/service_request_status.txt'
    text_message = render_to_string(text_version,c)
    try:
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL,[obj.customer.userregistration.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')



def serviceInvoiceMail(obj):
    subject = f'Invoice for {obj.service.servicereq_no}-{obj.service.title}'
    c = {
        # 'domain':'127.0.0.1:8000',
        'domain':'ems.excellentworld.xyz',
        'protocol': 'https',
        # 'protocol': 'http',
        'id':obj.id,
        'date':obj.created_at,
        'parts_charge':obj.equip_charge,
        'parts_details':obj.details,
        'document':obj.files,
    }
    html_version = 'mail/invoice.html'
    html_template = render_to_string(html_version,c)
    try:
        message = EmailMessage(subject, html_template, settings.DEFAULT_FROM_EMAIL,[obj.service.customer.userregistration.email])
        message.content_subtype = 'html'
        message.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')



def paymentStatusCustomerMailFunc(obj):
    subject = f'Payment Confirmation for Invoice ID #{obj.id}'
    message = f'Hi {obj.service.customer.userregistration.name},\nYour payment for invoice #{obj.id}  {obj.service.title} has been completed.\nThank you.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [obj.service.customer.userregistration.email]
    send_mail( subject, message, email_from, recipient_list )



def paymentStatusTechnicianMailFun(obj):
    subject = f'Payment Confirmation for Invoice ID #{obj.id}'
    message = f'Hi {obj.service.technician.name},\nYour payment for invoice #{obj.id}  {obj.service.title} has been completed.\nThank you.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [obj.service.technician.email]
    send_mail( subject, message, email_from, recipient_list )




def get_months():
    date_today = datetime.today()
    month_fday = date_today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = date_today.replace(day=28) + timedelta(days=4)
    month_lday = next_month - timedelta(days = next_month.day)
    return month_fday,month_lday



def getTechnicianLocations(customer, technician_qs):
    locDict = {}
    for iLoc in technician_qs:
        if iLoc.location and customer.location:
            distance = geodesic(customer.location, iLoc.location.split(',')).kilometers
            locDict[iLoc.id] = distance

    if locDict:
        k = min(locDict, key = locDict.get)
        nearestTechnician = UserRegistration.objects.get(id=k)
        return nearestTechnician
    else:
        return None
