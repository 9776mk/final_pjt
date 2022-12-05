from django.shortcuts import render
from .models import *


def index(request):
    br = BJData_br.objects.order_by("pk")
    si = BJData_si.objects.order_by("pk")
    context = {
        "br": br,
        "si": si,
    }
    return render(request, "algorithm/index.html", context)
