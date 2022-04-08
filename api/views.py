from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app_dashboard.models import *
from app_dashboard.decorators import *
from api.models import *
from app_dashboard.utils import *


# Create your views here.
def sendChat_view(request):
    ticketID = request.POST.get('ticketID',None)
    service_obj = ServiceRequest.objects.get(id = ticketID)
    msg = request.POST.get('chat_field',None)
    message = Message(user=request.user.userregistration,service_ticket=service_obj,message=msg)
    message.save()
    return JsonResponse({})



def receiveChat_view(request):
    ticketID = request.POST.get('ticketID',None)
    msg_qs = Message.objects.filter(service_ticket__id = ticketID,seen=False).exclude(user = request.user.userregistration)
    if request.user.userregistration.role == 'customer':
        receiver_name = 'Technician'
    if request.user.userregistration.role == 'technician':
        receiver_name = 'Customer'
    data = {
        'messages' : list(msg_qs.values()),
        'receiver_name':receiver_name,
        }
    msg_qs.update(seen=True)
    return JsonResponse(data)



def serviceNotify_view(request):
    service_qs = TempServiceRequest.objects.filter(nearest_tech = request.user.userregistration)
    data = {
        'unassigned_qs':list(service_qs.values())
        }
    return JsonResponse(data)



def serviceAccept_view(request):
    tempServiceId = request.POST.get('tempServiceId',None)
    tempService = TempServiceRequest.objects.get(id = tempServiceId)
    service = tempService.service
    service.technician = request.user.userregistration
    service.assigned = True
    service.save()
    tempService.delete()
    technicianAssignMail(service)
    return JsonResponse({'status':1})



def serviceAccept_customerNotify_view(request):
    assignedService = ServiceRequest.objects.filter(assigned = True, customer = request.user).order_by('-id')
    techList = []
    for service in assignedService:
        techList.append({'title':service.title, 'name':service.technician.name, 'email':service.technician.email, 'phone':service.technician.phone})
    return JsonResponse({'techInfo':techList})



def getServiceInfo(request):
    temp_service_id = request.POST.get('service_details_id')
    getTempService = TempServiceRequest.objects.get(id = temp_service_id)
    serviceInfo = ServiceRequest.objects.get(id = getTempService.service.id)
    context = {
        'title':serviceInfo.title,
        'details':serviceInfo.details,
        'priority':serviceInfo.priority,
        'date':serviceInfo.created_at,
    }
    return JsonResponse({'details_info': context})



def serviceReject(request):
    tempServiceId = request.POST.get('tempServiceId',None)
    tempService = TempServiceRequest.objects.get(id = tempServiceId)
    rjt_tech_list = tempService.rejected_tech_id.split(',')
    rjt_tech_list.append(str(request.user.userregistration.id))
    tempService.rejected_tech_id = ",".join(rjt_tech_list)
    rjt_tech_list = [int(item) for item in rjt_tech_list if item]
    customer = tempService.service.customer.userregistration
    technician_qs = UserRegistration.objects.filter(role='technician').exclude(id__in=rjt_tech_list)

    if not technician_qs:
        technician_qs = UserRegistration.objects.filter(role='technician')
        tempService.rejected_tech_id = ''

    nearestTechnician = getTechnicianLocations(customer, technician_qs)
    tempService.nearest_tech = nearestTechnician
    tempService.save()
    newServiceNotifyMailFunc(nearestTechnician)
    
    return JsonResponse({'status':1})



def getDistrict_view(request):
    divisionName = request.POST.get('division')
    districts = District.objects.filter(division__name = divisionName)
    districtsList = list(districts.values())
    return JsonResponse({'districtsList':districtsList})



def getUpazila_view(request):
    districtName = request.POST.get('district')
    upazilas = Upazila.objects.filter(district__name = districtName)
    upazilaList = list(upazilas.values())
    return JsonResponse({'upazilaList':upazilaList})



def getEmail_view(request):
    emailName = request.POST.get('emailName')
    Customerinfo = UserRegistration.objects.filter(email__icontains = emailName)
    if Customerinfo.count() > 0:
        return JsonResponse({'status' : 1})
    else:
        return JsonResponse({'status' : 0})



def getPhone_view(request):
    phoneNum = request.POST.get('phoneNum')
    Customerinfo = UserRegistration.objects.filter(phone__icontains = phoneNum)
    if Customerinfo.count() > 0:
        return JsonResponse({'status' : 1})
    else:
        return JsonResponse({'status' : 0})



# @login_required(login_url='login')
def admin_servicelist_view(request):
    technician_id = request.POST.get('technician_id')
    servicelist = ServiceRequest.objects.filter(technician__id = technician_id)
    context = {
        'servicelist':list(servicelist.values()),
    }
    return JsonResponse(context,safe=False)



@login_required(login_url='login')
@user_is_admin
@user_is_technician
def satusUpdate(request):
    status = request.GET.get('status')
    id = request.GET.get('id')
    service_obj = ServiceRequest.objects.get(id = id)

    if service_obj.status == status:
        return JsonResponse({'status' : 'null', 'service_no': service_obj.servicereq_no })
    elif service_obj and status and service_obj.status != status:
        service_obj.status = status
        service_obj.save()
        serviceStatusMail(service_obj)
        return JsonResponse({'status' : 1, 'service_no': service_obj.servicereq_no })
    else:
        return JsonResponse({'status' : 0})



def map_api(request):
    technician_qs = UserRegistration.objects.filter(role='technician')
    context ={
        'technician_list':list(technician_qs.values('location'))
    }
    return JsonResponse(context)


