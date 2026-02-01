from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from tution_app.parents.models import ParentProfile, Booking
from tution_app.teachers.models import TeacherProfile

@login_required
def add_student(request):
    parent_profile = ParentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        Student.objects.create(
            parent=parent_profile,
            name=request.POST['name'],
            school=request.POST['school'],
            class_name=request.POST['class_name']
        )
        return redirect('parent_home')
    return render(request, 'register/add_student.html', {'parent_name': parent_profile.name, 'user_name': request.user.username})

@login_required
def book_teacher(request):
    if request.method == 'POST':
        parent_profile = ParentProfile.objects.get(user=request.user)
        student = Student.objects.get(id=request.POST['student'])
        teacher = TeacherProfile.objects.get(id=request.POST['teacher'])
        booking = Booking.objects.create(
            parent=parent_profile,
            teacher=teacher,
            subject=teacher.subject,
            student_name=student.name,
            school=student.school,
            class_name=student.class_name
        )
        return redirect('payment', booking_id=booking.id)
    parent_profile = ParentProfile.objects.get(user=request.user)
    booked_student_names = Booking.objects.filter(parent=parent_profile).values_list('student_name', flat=True)
    students = Student.objects.filter(parent__user=request.user).exclude(name__in=booked_student_names)
    subjects = TeacherProfile.objects.filter(is_approved=True).values_list('subject', flat=True).distinct()
    selected_subject = request.GET.get('subject')
    if selected_subject:
        teachers = TeacherProfile.objects.filter(is_approved=True, subject=selected_subject)
    else:
        teachers = TeacherProfile.objects.filter(is_approved=True)
    return render(request, 'register/book_teacher.html', {'students': students, 'teachers': teachers, 'subjects': subjects, 'selected_subject': selected_subject})

@login_required
def payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        # Process payment 
        booking.payment_status = 'paid'
        booking.save()
        return redirect('parent_home')
    return render(request, 'register/payment.html', {'booking': booking})
