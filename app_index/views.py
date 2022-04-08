from django.shortcuts import render,redirect
from django.contrib import messages
from app_dashboard.models import *
from app_dashboard.forms import *
# Create your views here.

# Create your views here.
def index_view(request):
    reviews = Review.objects.all().order_by('-id')

    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
    context = {
        'form': form,
        'reviews': reviews
    }
    return render(request, 'app_index/index.html', context)

