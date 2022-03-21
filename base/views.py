from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ModuleForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Cohort, Profile, Module, Discussion
from .forms import UpdateProfileForm, CohortForm, DiscussionForm
from django.contrib.auth.models import User



def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def cohorts(request):
    all_cohorts = Cohort.objects.all()
    all_cohorts = all_cohorts[::-1]
    params = {
        'all_cohorts': all_cohorts,
    }
    return render(request, 'all_cohorts.html', params)


def create_cohort(request):
    if request.method == 'POST':
        form = CohortForm(request.POST, request.FILES)
        if form.is_valid():
            cohort = form.save(commit=False)
            cohort.admin = request.user.profile
            cohort.save()
            return redirect('cohort')
    else:
        form = CohortForm()
    return render(request, 'newcohort.html', {'form': form})


def single_cohort(request, cohort_id):
    cohort = Cohort.objects.get(id=cohort_id)
    module = Module.objects.filter(cohort=cohort)
    topics = Discussion.objects.filter(cohort=cohort)
    topics = topics[::-1]
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            mod_form = form.save(commit=False)
            mod_form.cohort = cohort
            mod_form.user = request.user.profile
            mod_form.save()
            return redirect('single-cohort', cohort.id)
    else:
        form = ModuleForm()
    params = {
        'cohort': cohort,
        'module': module,
        'form': form,
        'topics': topics
    }
    return render(request, 'single_cohort.html', params)


def cohort_members(request, cohort_id):
    cohort = Cohort.objects.get(id=cohort_id)
    members = Profile.objects.filter(cohort=cohort)
    return render(request, 'members.html', {'members': members})


def create_topic(request, cohort_id):
    cohort = Cohort.objects.get(id=cohort_id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.cohort = cohort
            topic.user = request.user.profile
            topic.save()
            return redirect('single-cohort', cohort.id)
    else:
        form = DiscussionForm()
    return render(request, 'topic.html', {'form': form})

@login_required(login_url='login')
def join_cohort(request, id):
    cohort = get_object_or_404(Cohort, id=id)
    request.user.profile.cohort = cohort
    request.user.profile.save()
    return redirect('cohort')


def leave_cohort(request, id):
    cohort = get_object_or_404(Cohort, id=id)
    request.user.profile.cohort = None
    request.user.profile.save()
    return redirect('cohort')


def profile(request, username):
    return render(request, 'profile.html')


def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'editprofile.html', {'form': form})


def search_module(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Module.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any module"
    return render(request, "results.html")
