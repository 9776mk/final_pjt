from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    studies = Study.objects.all()

    context = {
        'studies': studies,
    }

    return render(request, 'studies/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        study_form = StudyForm(request.POST, request.FILES)

        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host_user = request.user
            study.save()

            return redirect('studies:detail', study.pk)

    else:
        study_form = StudyForm()

    context = {
        'study_form': study_form,
    }

    return render(request, 'studies/create.html', context)


def detail(request, study_pk):
    study = Study.objects.get(pk=study_pk)

    context = {
        'study': study,
    }

    return render(request, 'studies/detail.html', context)


@login_required
def update(request, study_pk):
    study = Study.objects.get(pk=study_pk)

    if request.user != study.host_user:
        return redirect('studies:index')

    if request.method == 'POST':
        study_form = StudyForm(request.POST, request.FILES, instance=study)

        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host_user = request.user
            study.save()

            return redirect('studies:detail', study.pk)

    else:
        study_form = StudyForm(instance=study)

    context = {
        'study_form': study_form,
    }

    return render(request, 'studies/create.html', context)


@login_required
def delete(request, study_pk):
    study = Study.objects.get(pk=study_pk)

    if request.user == study.host_user and request.method == 'POST':
        study.delete()
        
    return redirect('studies:index')