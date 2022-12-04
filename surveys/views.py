from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def create(request):
    if request.method == 'POST':
        survey_form = SurveyForm(request.POST)
        print(survey_form.is_valid())

        if survey_form.is_valid():
            survey_form.save()
            return redirect('home')

    else:
        survey_form = SurveyForm()
    
    context = {
        'survey_form': survey_form,
    }

    return render(request, 'surveys/create.html', context)