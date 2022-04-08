from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from app_dashboard.forms import *
from app_dashboard.models import *
from app_dashboard.utils import *
from app_dashboard.decorators import *
from api.models import *

#------------------------- Dashboard -------------------------#
@login_required(login_url='login')
@user_is_admin
def dashboard_view(request):
    if hasattr(request.user, 'userregistration'):
        if request.user.userregistration.active:
            remainingServices = 0
            completedServices = 0
            totalServices = 0
            cancelledServices = 0
            tech_total_charge=0
            equip_total_charge=0
            total = 0
            totalDue=0
            if request.user.userregistration.role == 'customer':
                service_qs = ServiceRequest.objects.filter(customer = request.user)
                totalServices = service_qs.count()
                remainingServices = service_qs.exclude(status='Closed').exclude(status='Cancelled').count()
                completedServices = service_qs.filter(status = 'Closed').count()
                cancelledServices = service_qs.filter(status = 'Cancelled').count()
                invoice_qs = Invoice.objects.filter(service__customer=request.user)

                for i in invoice_qs:
                    total += (i.service.service_category.cost + i.equip_charge)
                    if i.status == 'Unpaid':
                        totalDue += (i.service.service_category.cost + i.equip_charge)

            elif request.user.userregistration.role == 'technician':
                service_qs = ServiceRequest.objects.filter(technician = request.user.userregistration)
                totalServices = service_qs.count()
                remainingServices = ServiceRequest.objects.filter(Q(technician = request.user.userregistration)).exclude(status = 'Closed').count()
                completedServices = ServiceRequest.objects.filter(Q(technician = request.user.userregistration)&Q(status='Closed')).count()
                invoice_qs = Invoice.objects.filter(service__technician=request.user.userregistration)
                for i in invoice_qs:
                    tech_total_charge += i.service.service_category.cost
                    equip_total_charge += i.equip_charge
                for i in invoice_qs:
                    if i.status == 'Unpaid':
                        totalDue += i.service.service_category.cost
            
            
            Due=False
            if totalDue > 0:
                Due=True
            
            context = {
                'total':total,
                'totalDue':totalDue,
                'dueStatus': Due,
                'tech_total_charge':tech_total_charge,
                'equip_total_charge':equip_total_charge,

                'totalServices':totalServices,
                'remainingServices':remainingServices,
                'completedServices':completedServices,
                'cancelledServices':cancelledServices,

            }
            return render(request, 'app_dashboard/dashboard.html', context)
        else:
            return render(request, 'app_dashboard/comfirm_account.html')
    else:
        raise Http404



@login_required(login_url='login')
def technician_payments_view(request):
    invoice_qs = Invoice.objects.filter(service__technician=request.user.userregistration)

    total = 0
    totalDue=0
    for i in invoice_qs:
        total += i.service.service_category.cost
        if i.status == 'Unpaid':
            totalDue += i.service.service_category.cost



    print(total,totalDue)
    
    Due=False
    if totalDue > 0:
        Due=True




    context = {
        'total':total,
        'totalDue':totalDue,
        'invoice_qs':invoice_qs,
    }
    return render(request, 'app_dashboard/technician/payments.html', context)


@login_required(login_url='login')
def customer_payments_view(request):
    form = CustomerPaymentForm()
    if request.method == 'POST':
        form = CustomerPaymentForm(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.invoice = Invoice.objects.filter(id = request.POST.get('invoiceID',None)).first()
            newForm.save()
            return redirect('customerPayments')

    invoice_qs = Invoice.objects.filter(service__customer=request.user)

    total = 0
    totalDue=0
    for i in invoice_qs:
        total += (i.service.service_category.cost + i.equip_charge)
        if i.status == 'Unpaid':
            totalDue += (i.service.service_category.cost + i.equip_charge)



    print(total,totalDue)
    
    Due=False
    if totalDue > 0:
        Due=True




    context = {
        'total':total,
        'totalDue':totalDue,
        'invoice_qs':invoice_qs,
        'form':form,
    }
    return render(request, 'app_dashboard/customer/payments.html', context)



@login_required(login_url='login')
@user_is_admin
def updateProfile_view(request, pk):
    customer_info = UserRegistration.objects.get(id=pk)
    form = UserRegistrationUpdateForm(instance= customer_info)
    if request.method == 'POST':
        form = UserRegistrationUpdateForm(request.POST,request.FILES, instance= customer_info)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            user.email = request.POST.get('email')
            user.save()
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.country=request.POST.get('country')
            new_form.division=request.POST.get('division')
            new_form.district=request.POST.get('district')
            new_form.upazila=request.POST.get('upazila')
            new_form.save()
            messages.success(request, 'Your information has been updated!')
            return redirect('updateProfile', pk)
    divisions = Division.objects.all()
    context = {
        'divisions':divisions,
        'form' : form,
        'customer_info':customer_info
    }
    return render(request, 'app_dashboard/update_info.html',context)



@login_required(login_url='login')
@user_is_admin
@user_is_customer
def create_service_view(request):
    form = ServiceRequestForm()
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.customer = request.user
            newform.servicereq_no = getTicketNo()
            newform.save()
            customer = request.user.userregistration
            technician_qs = UserRegistration.objects.filter(role='technician')
            nearestTechnician = getTechnicianLocations(customer, technician_qs)
            TempServiceRequest.objects.create(service_title=newform.title,service=newform,nearest_tech=nearestTechnician)
            messages.success(request, 'Your requested service has been created!')
            newServiceNotifyMailFunc(nearestTechnician)
            return redirect('create_service')
    context ={
        'form': form
    }

    return render(request, 'app_dashboard/customer/create_service.html', context)



@login_required(login_url='login')
@user_is_admin
@user_is_customer
def customerServiceRequestList_view(request):
    service_list = ServiceRequest.objects.filter(customer = request.user)
    context ={
        'service_list': service_list 
        }
    return render(request, 'app_dashboard/customer/service_request_list.html', context)



@login_required(login_url='login')
@user_is_admin
@user_is_technician
def technicianServiceRequestList_view(request):
    work_list = ServiceRequest.objects.filter(technician = request.user.userregistration).order_by('-created_at')

    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        service_id = request.POST.get('service_id')
        print(service_id)
        curr_status = request.POST.get('curr_status')
        service_obj = ServiceRequest.objects.get(id = service_id)

        if service_obj and curr_status and service_obj.status != curr_status:
            service_obj.status = curr_status
            service_obj.save()
            if form.is_valid():
                newform = form.save(commit=False)
                newform.service =  service_obj
                newform.save()
                serviceStatusMail(service_obj)
                serviceInvoiceMail(newform)
                
                messages.success(request, 'Your requested service has been created!')
                return redirect('technicianServiceList')
        else:
            messages.success(request,'No changes Detected')
    context ={
        'work_list': work_list,
        }
    return render(request, 'app_dashboard/technician/service_request_list.html', context)



@login_required(login_url='login')
def details_service_view(request, pk):
    details = ServiceRequest.objects.get(id = pk)
    context ={
        'obj': details
    }

    return render(request, 'app_dashboard/details_service.html', context)



@login_required(login_url='login')
def admin_invoice_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        service_id = request.POST.get('service_id')
        curr_status = request.POST.get('curr_status')
        service_obj = ServiceRequest.objects.get(id = service_id)
        if service_obj and curr_status and service_obj.status != curr_status:
            service_obj.status = curr_status
            service_obj.save()
            if form.is_valid():
                newform = form.save(commit=False)
                newform.service =  service_obj
                newform.save()
                serviceStatusMail(service_obj)
                serviceInvoiceMail(newform)
                messages.success(request, '1 service request was changed successfully.')
        else:
            messages.success(request,'No changes Detected')

    return redirect('/admin/app_dashboard/servicerequest/')



@login_required(login_url='login')
def get_technician_work_list(request):
    technicianList = UserRegistration.objects.filter(role = 'technician' )
    technician_id = request.POST.get('technician_id')
    if technician_id:
        technician_id =  int(technician_id)
    servicelist = ServiceRequest.objects.filter(technician__id = technician_id)
    context = {
        'technicianList':technicianList,
        'servicelist':servicelist,
        'technician_id':technician_id,
    }
    return render(request,'technician_work_list.html',context)



@login_required(login_url='login')
def chat_view(request):
    ticket_id = request.GET.get('ticket',None)
    if request.user.userregistration.get_role() == 'customer':
        service_qs = ServiceRequest.objects.filter(customer = request.user,assigned=True).order_by('-created_at','-id')
    elif request.user.userregistration.get_role() == 'technician':
        service_qs = ServiceRequest.objects.filter(technician = request.user.userregistration,assigned=True).order_by('-created_at','-id')
    if not ticket_id and service_qs.first():
        ticket_id = service_qs.first().id
    else:
        ticket_id = None

    message_qs = Message.objects.filter(service_ticket__id=ticket_id).order_by('-sent_date')

    context ={
        'message_qs': message_qs,
        'service_qs':service_qs,
        'ltickeID':ticket_id
    }
    message_qs.update(seen = True)
    return render(request, 'app_dashboard/chat.html', context)


def customer_review_view(request):
    service_closed_list = ServiceRequest.objects.filter(customer = request.user, status = 'closed')
    form  = ReviewForm(request.POST)
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        newService = ServiceRequest.objects.get(id=service_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.service = newService
            newform.save()

            return redirect('customer_review')

    context ={
        'form': form,
        'service_closed_list': service_closed_list 
        }
    return render(request, 'app_dashboard/customer/review.html', context)


@login_required(login_url='login')
def techmap_view(request):
    technician_qs = UserRegistration.objects.filter(role='technician')
    print(technician_qs.values('location'))
    context ={
        'technician_list':technician_qs.values('location')
    }
    return render(request, 'app_dashboard/customer/techmap.html', context)


@login_required(login_url='login')
@user_is_admin
def changePassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app_dashboard/change_password.html', {'form': form})




# custom error handling page
def custom_page_not_found_view(request, exception=None):
    return render(request, "custom-error-page/404.html", {})



