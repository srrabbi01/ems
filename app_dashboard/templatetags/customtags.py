from django import template
from app_dashboard.models import Review

register = template.Library()

@register.filter
def add2var(var1,var2):
    return var1+var2

@register.filter
def sub2var(var1,var2):
    return var1-var2



@register.filter
def uppercon(value):
    if value == 'new':
        return 'New'
    elif value == 'in_progress':
        return 'In Progress'
    elif value == 'waittingoncustomer':
        return 'Waitting on Customer'
    elif value == 'fixed':
        return 'Fixed'
    elif value == 'closed':
        return 'Closed'
    elif value == 'cancelled':
        return 'Cancelled'
    else:
        return value

@register.filter
def reviewCheck(id):
    review = Review.objects.filter(service_id = id)
    
    if review:
        return True
    else:
        return False

@register.filter
def getPercent(val_1, val_2):
    if type(val_1) == int and type(val_2) and val_2:
        return round((val_1*100)/val_2, 2)
    else:
        return val_1