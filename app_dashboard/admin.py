from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import *
from .utils import activateAccountMailFunc,technicianAssignMail,serviceStatusMail,paymentStatusCustomerMailFunc,paymentStatusTechnicianMailFun

# Register your models here.
admin.site.register(Contact)
admin.site.register(ServiceCategory)
admin.site.register(Message)
admin.site.register(TempServiceRequest)



class UserRegistrationAdmin(admin.ModelAdmin):
    list_filter = ('role','active','registration_type',)
    list_display = ('name','phone','email','role','active')
    search_fields = ['phone','role','name','email','reg_no',]
    def save_model(self, request, obj, form, change):
        if obj.active and ('active' in form.changed_data):
            activateAccountMailFunc(obj)
        super(UserRegistrationAdmin, self).save_model(request, obj, form, change)

admin.site.register(UserRegistration, UserRegistrationAdmin)


class ServiceRequestAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceRequestAdminForm, self).__init__(*args, **kwargs)
        self.fields['technician'].queryset = UserRegistration.objects.filter(role='technician')


class ServiceRequestAdmin(admin.ModelAdmin):
    form = ServiceRequestAdminForm
    # readonly_fields=('customer', )
    list_filter = ('priority', 'status',)
    list_display = ('servicereq_no','title', 'get_customer_name','get_customer_phone','get_customer_email','get_service_category_name','technician','status','update_status',)
    list_editable = ('status',)
    search_fields = ['title','customer__userregistration__phone','servicereq_no',]
    change_list_template = 'custom_change_list/custom_service_change_list.html'
    @admin.display(description='Cost Category')
    def get_service_category_name(self,obj):
        if obj.service_category:
            return f'{obj.service_category.category_name}'
        else:
            return 'Empty'

    def get_customer_name(self,obj):
        return obj.customer.userregistration.name
    get_customer_name.admin_order_field = 'customer__userregistration__name'
    get_customer_name.short_description = 'Customer Name'

    def get_customer_phone(self,obj):
        return obj.customer.userregistration.phone
    get_customer_phone.admin_order_field = 'customer__userregistration__phone'
    get_customer_phone.short_description = 'Customer Phone'

    def get_customer_email(self,obj):
        return obj.customer.userregistration.email
    get_customer_email.admin_order_field = 'customer__userregistration__email'
    get_customer_email.short_description = 'Customer Email'


    def update_status(self, obj):
        return format_html('<input type="submit" name="_save" class="default update__status" value="Save">')
    update_status.short_description = "update"

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.technician:
            # serviceStatusMail(obj)
            pass
        if obj.technician and ('technician' in form.changed_data):
            # technicianAssignMail(obj)
            pass
        super(ServiceRequestAdmin, self).save_model(request, obj, form, change)

admin.site.register(ServiceRequest,ServiceRequestAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('id','get_servicereq_no','get_service_title','status', 'get_customer_name', 'get_customer_phone', 'get_customer_email','get_technician_name','created_at')
    list_editable = ('status',)
    change_list_template = 'custom_change_list/custom_invoice_change_list.html'

    def get_servicereq_no(self,obj):
        return obj.service.servicereq_no
    get_servicereq_no.admin_order_field = 'service__servicereq_no'
    get_servicereq_no.short_description = 'Service No'

    def get_customer_name(self,obj):
        return obj.service.customer.userregistration.name
    get_customer_name.admin_order_field = 'service__customer__userregistration__name'
    get_customer_name.short_description = 'Customer Name'

    def get_customer_phone(self,obj):
        return obj.service.customer.userregistration.phone
    get_customer_phone.admin_order_field = 'service__customer__userregistration__phone'
    get_customer_phone.short_description = 'Customer Phone'

    def get_customer_email(self,obj):
        return obj.service.customer.userregistration.email
    get_customer_email.admin_order_field = 'service__customer__userregistration__email'
    get_customer_email.short_description = 'Customer Email'

    def get_service_title(self,obj):
        return obj.service.title
    get_service_title.admin_order_field = 'service__title'
    get_service_title.short_description = 'Service'

    @admin.display(description='Technician')
    def get_technician_name(self,obj):
        if obj.paid:
            if hasattr(obj,'technicianpayment'):
                return format_html(f'{obj.service.technician.name}<a class="button ml-1" disabled >Paid</a>')
            else:
                return format_html(f'{obj.service.technician.name}<a href="/admin/app_dashboard/technicianpayment/add/?invId={obj.id}" class="button ml-1 default" >Pay</a>')
        else:
            return obj.service.technician.name

        
        

    # get_technician_name.admin_order_field = 'service__title'

    def save_model(self, request, obj, form, change):
        if ('status' in form.changed_data) and (obj.status == 'Paid'):
            if obj.customerpayment:
                obj.customerpayment.paid = True
                obj.customerpayment.save()
                obj.status = 'Paid'
                obj.paid = True
                paymentStatusCustomerMailFunc(obj)

        super(InvoiceAdmin, self).save_model(request, obj, form, change)


admin.site.register(Invoice, InvoiceAdmin)



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','service_name', 'service_customer_name', 'created_at')

    @admin.display(description='Service Title')
    def service_name(self, obj):
        return obj.service.title

    @admin.display(description='Customer Name')
    def service_customer_name(self, obj):
        return obj.service.customer.userregistration.name

admin.site.register(Review,ReviewAdmin)

class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = ('get_invoice_id', 'get_customer_name', 'transition_id','payment_method','payment_date','get_paid_amount')

    @admin.display(description='Invoice ID')
    def get_invoice_id(self,obj):
        if obj.invoice:
            return f"{obj.invoice.id}"

    @admin.display(description= 'Paid Amount')
    def get_paid_amount(self, obj):
        if obj.invoice:
            return f"{obj.invoice.getTotalCharge()}"
    @admin.display(description='Customer Name')
    def get_customer_name(self, obj):
        if obj.invoice:
            return f"{obj.invoice.service.customer.userregistration.name}"

admin.site.register(CustomerPayment, CustomerPaymentAdmin)


class TechnicianPaymentAdmin(admin.ModelAdmin):
    list_display = ('get_invoice_id', 'get_technician_name','transition_id','payment_method','payment_date','amount')
    change_list_template = 'custom_change_list/custom_techpayment_change_list.html'
    add_form_template = 'custom_add_form/techpayment_add_form.html'
    
    @admin.display(description='Invoice ID')
    def get_invoice_id(self,obj):
        if obj.invoice:
            return f"{obj.invoice.id}"

    @admin.display(description='Technician Name')
    def get_technician_name(self, obj):
        if obj.invoice:
            return f"{obj.invoice.service.technician.name}"

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.paid = True
            paymentStatusTechnicianMailFun(obj.invoice)
        super(TechnicianPaymentAdmin, self).save_model(request, obj, form, change)



admin.site.register(TechnicianPayment,TechnicianPaymentAdmin)





admin.site.site_header = 'Ems'