from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    Su_Kiens = SuKien.objects.all()
    context={'Su_Kiens': Su_Kiens}
    return render(request, 'app/home.html',context)