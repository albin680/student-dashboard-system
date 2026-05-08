from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Enquiry, Notification


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if User.objects.filter(username=username).exists():

            return render(request, 'dashboard/register.html', {
                'error': 'Username already exists'
            })
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.save()

        return redirect('login')

    return render(request, 'dashboard/register.html')

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        
        if user is not None:

            login(request, user)

            profile = Profile.objects.get(user=user)

            if profile.role == 'student':
                return redirect('student_dashboard')

            elif profile.role == 'faculty':
                return redirect('faculty_dashboard')
        return render(request, 'dashboard/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'dashboard/login.html')

def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
def student_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'student':
        return redirect('faculty_dashboard')

    if request.method == 'POST':

        subject = request.POST['subject']
        message = request.POST['message']

        Enquiry.objects.create(
            student=request.user,
            subject=subject,
            message=message
        )

        return redirect('student_dashboard')

    enquiries = Enquiry.objects.filter(student=request.user)

    notifications = Notification.objects.filter(user=request.user)

    return render(request, 'dashboard/student_dashboard.html', {
        'enquiries': enquiries,
        'notifications': notifications,
    })



@login_required
def faculty_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    
    if profile.role != 'faculty':
        return redirect('student_dashboard')

    enquiries = Enquiry.objects.all()

    return render(request, 'dashboard/faculty_dashboard.html', {
        'enquiries': enquiries
    })