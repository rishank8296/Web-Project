from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from .models import ParentProfile, Booking
from tution_app.teachers.models import TeacherProfile
from tution_app.register.models import Student


# =========================
# HOME
# =========================
def home(request):
    return render(request, 'home.html')


# =========================
# LOGIN
# =========================
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('admin_home')
            elif hasattr(user, 'teacherprofile') and user.teacherprofile.is_approved:
                return redirect('teacher_home')
            else:
                return redirect('parent_home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# =========================
# REGISTER (PARENT)
# =========================
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        image = request.FILES.get('image')

        # Check existing user
        if User.objects.filter(username=email).exists():
            return render(
                request,
                'parents/parent_register.html',
                {'error': 'Email already registered'}
            )

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Create parent profile
        ParentProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            gender=gender,
            address=address,
            image=image
        )

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'parents/parent_register.html')


# =========================
# LOGOUT
# =========================
def logout(request):
    auth_logout(request)
    return redirect('home')


# =========================
# PARENT DASHBOARD
# =========================
@login_required
def parent_home(request):
    try:
        parent_profile = ParentProfile.objects.get(user=request.user)
        approved_bookings = Booking.objects.filter(
            parent=parent_profile,
            is_approved=True
        )
        students = Student.objects.filter(parent=parent_profile)
        return render(request, 'parents/parenthome.html', {
            'approved_bookings': approved_bookings,
            'students': students
        })
    except ParentProfile.DoesNotExist:
        messages.error(request, "Parent profile not found")
        return redirect('login')


# =========================
# ADMIN DASHBOARD
# =========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    return render(request, 'admin/adminhome.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_bookings(request):
    bookings_pending = Booking.objects.filter(is_approved=False)
    bookings_approved = Booking.objects.filter(is_approved=True)
    return render(request, 'admin/bookings.html', {
        'bookings_pending': bookings_pending,
        'bookings_approved': bookings_approved
    })


# =========================
# BOOKING ACTIONS
# =========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.is_approved = True
    booking.save()
    return redirect('admin_bookings')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect('admin_bookings')


# =========================
# ADMIN APPROVALS
# =========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_approvals(request):
    pending_teachers = TeacherProfile.objects.filter(is_approved=False)
    approved_teachers = TeacherProfile.objects.filter(is_approved=True)
    pending_parents = ParentProfile.objects.filter(is_approved=False)
    approved_parents = ParentProfile.objects.filter(is_approved=True)

    return render(request, 'admin/approvals.html', {
        'pending_teachers': pending_teachers,
        'approved_teachers': approved_teachers,
        'pending_parents': pending_parents,
        'approved_parents': approved_parents
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_teacher(request, id):
    teacher = get_object_or_404(TeacherProfile, id=id)
    teacher.is_approved = True
    teacher.save()
    return redirect('admin_approvals')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_teacher(request, id):
    teacher = get_object_or_404(TeacherProfile, id=id)
    teacher.user.delete()
    return redirect('admin_approvals')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_parent(request, id):
    parent = get_object_or_404(ParentProfile, id=id)
    parent.is_approved = True
    parent.save()
    return redirect('admin_approvals')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_parent(request, id):
    parent = get_object_or_404(ParentProfile, id=id)
    parent.user.delete()
    return redirect('admin_approvals')
