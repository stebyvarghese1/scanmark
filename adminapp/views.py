from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Student, Course
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

def dashboard(request):
    return render(request, 'adminapp/dashboard.html')

def students_list(request):
    qs = Student.objects.all()
    batch_from = request.GET.get('batch_from')
    batch_to = request.GET.get('batch_to')
    course = request.GET.get('course')
    if batch_from:
        qs = qs.filter(batch_from__lte=batch_from)
    if batch_to:
        qs = qs.filter(batch_to__gte=batch_to)
    if course:
        try:
            qs = qs.filter(course_id=int(course))
        except ValueError:
            pass  # Ignore if course is not a valid integer
    courses = Course.objects.all()
    # If AJAX, return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        students = []
        for s in qs:
            students.append({
                'id': s.id,
                'roll_number': s.roll_number,
                'name': s.name,
                'register_number': s.register_number,
                'photo': s.photo.url if s.photo else '',
                'course': s.course.name if s.course else '',
                'batch_from': s.batch_from,
                'batch_to': s.batch_to,
                'date_of_birth': s.date_of_birth.isoformat() if s.date_of_birth else '',
                'blood_group': s.blood_group,
                'address': s.address,
                'phone_number': s.phone_number,
            })
        return JsonResponse({'students': students})
    return render(request, 'adminapp/students_list.html', {
        'students': qs,
        'courses': courses,
    })

@require_http_methods(["POST"])
def add_student(request):
    data = request.POST
    roll_number = data.get('roll_number')
    register_number = data.get('register_number')
    course_id = data.get('course')
    batch_from = data.get('batch_from')
    batch_to = data.get('batch_to')
    course = Course.objects.get(id=course_id) if course_id else None
    # Check for duplicate
    if Student.objects.filter(
        roll_number=roll_number,
        register_number=register_number,
        course=course,
        batch_from=batch_from,
        batch_to=batch_to
    ).exists():
        return JsonResponse({'success': False, 'error': 'Student with this roll number, register number, batch, and course already exists.'})
    student = Student(
        name=data.get('name'),
        roll_number=roll_number,
        register_number=register_number,
        course=course,
        batch_from=batch_from or None,
        batch_to=batch_to or None,
        date_of_birth=data.get('date_of_birth') or None,
        blood_group=data.get('blood_group'),
        address=data.get('address'),
        phone_number=data.get('phone_number'),
    )
    if request.FILES.get('photo'):
        student.photo = request.FILES['photo']
    student.save()
    return JsonResponse({'success': True})

@require_http_methods(["POST"])
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    data = request.POST
    roll_number = data.get('roll_number')
    register_number = data.get('register_number')
    course_id = data.get('course')
    batch_from = data.get('batch_from')
    batch_to = data.get('batch_to')
    course = Course.objects.get(id=course_id) if course_id else None
    # Check for duplicate (exclude current student)
    if Student.objects.filter(
        roll_number=roll_number,
        register_number=register_number,
        course=course,
        batch_from=batch_from,
        batch_to=batch_to
    ).exclude(pk=pk).exists():
        return JsonResponse({'success': False, 'error': 'Student with this roll number, register number, batch, and course already exists.'})
    student.name = data.get('name')
    student.roll_number = roll_number
    student.register_number = register_number
    student.course = course
    student.batch_from = batch_from or None
    student.batch_to = batch_to or None
    student.date_of_birth = data.get('date_of_birth') or None
    student.blood_group = data.get('blood_group')
    student.address = data.get('address')
    student.phone_number = data.get('phone_number')
    if request.FILES.get('photo'):
        student.photo = request.FILES['photo']
    student.save()
    return JsonResponse({'success': True})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    data = {
        'id': student.id,
        'name': student.name,
        'roll_number': student.roll_number,
        'register_number': student.register_number,
        'course_id': student.course.id if student.course else '',
        'course': student.course.name if student.course else '',  # <-- Add this line
        'batch_from': student.batch_from,
        'batch_to': student.batch_to,
        'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else "",
        'blood_group': student.blood_group,
        'address': student.address,
        'phone_number': student.phone_number,
        'photo': student.photo.url if student.photo else "",
    }
    return JsonResponse(data)

@require_http_methods(["DELETE"])
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return JsonResponse({'message': 'Student deleted'})

def settings_view(request):
    courses = Course.objects.all()
    return render(request, 'adminapp/settings.html', {'courses': courses})

@require_http_methods(["POST"])
def add_course(request):
    name = request.POST.get('name')
    if name and not Course.objects.filter(name=name).exists():
        Course.objects.create(name=name)
    return redirect('settings')

@api_view(['POST'])
def student_login(request):
    register_number = request.data.get('register_number')
    date_of_birth = request.data.get('date_of_birth')
    try:
        student = Student.objects.get(register_number=register_number)
        if student.date_of_birth and student.date_of_birth.strftime('%Y-%m-%d') == date_of_birth:
            return Response({
                'success': True,
                'student_id': student.id,
                'name': student.name,
                'register_number': student.register_number,
                'roll_number': student.roll_number,
                'course': student.course.name if student.course else "",
                'batch_from': student.batch_from,
                'batch_to': student.batch_to,
                'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else "",
                'blood_group': student.blood_group,
                'address': student.address,
                'phone_number': student.phone_number,
                'photo': student.photo.url if student.photo else "",
            })
        else:
            return Response({'success': False, 'error': 'Invalid credentials'})
    except Student.DoesNotExist:
        return Response({'success': False, 'error': 'Invalid credentials'})