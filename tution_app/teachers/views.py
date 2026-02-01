from django.shortcuts import render, redirect,get_object_or_404, redirect   
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import TeacherProfile
from tution_app.parents.models import Booking

# TEACHER REGISTRATION
def teacher_register(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']

        # Prevent duplicate emails
        if User.objects.filter(username=email).exists():
            return render(request, 'teachers/teacher_register.html', {'error': 'Email already registered!'})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=False  # admin approval required
        )

        TeacherProfile.objects.create(
            user=user,
            name=request.POST['Name'],
            phone=request.POST['Number'],
            gender=request.POST['Gender'],
            address=request.POST['Address'],
            subject=request.POST['Subject'],
            experience=request.POST['Expirience'],
            image=request.FILES.get('image')
        )

        return redirect('pending_teacher')

    return render(request, 'teachers/teacher_registration.html')


# PENDING PAGE
def pending_teacher(request):
    return render(request, 'teachers/pending.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_teacher(request, id):
    teacher = get_object_or_404(TeacherProfile, id=id)
    teacher.is_approved = True
    teacher.save()
    teacher.user.is_active = True
    teacher.user.save()
    return redirect('admin_approvals')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_teacher(request, id):
    teacher = get_object_or_404(TeacherProfile, id=id)
    teacher.user.delete()
    teacher.delete()
    return redirect('admin_approvals')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_teacher(request, id):
    teacher = get_object_or_404(TeacherProfile, id=id)
    teacher.user.delete()
    teacher.delete()
    return redirect('admin_approvals')


@login_required
def teacher_home(request):
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
        context = {
            'teacher': teacher_profile,
        }
        return render(request, 'teachers/teacherhome.html', context)
    except TeacherProfile.DoesNotExist:
        return redirect('home')


@login_required
def teacher_students(request):
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
        bookings = Booking.objects.filter(teacher=teacher_profile, is_approved=True)
        context = {
            'teacher': teacher_profile,
            'bookings': bookings,
        }
        return render(request, 'teachers/teacher_students.html', context)
    except TeacherProfile.DoesNotExist:
        return redirect('home')
