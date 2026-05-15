from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Avg, Q

from .models import Student, Marks
from .forms import StudentForm, MarksForm


# ---------------- DASHBOARD ----------------
@login_required(login_url='/login/')
def dashboard(request):
    students = Student.objects.filter(user=request.user)
    marks = Marks.objects.filter(student__user=request.user)

    total_students = students.count()
    total_marks = marks.count()

    avg_marks = marks.aggregate(avg=Avg('marks'))['avg']
    avg_marks = round(avg_marks, 2) if avg_marks else 0

    return render(request, 'students/dashboard.html', {
        'total_students': total_students,
        'total_marks': total_marks,
        'avg_marks': avg_marks
    })


# ---------------- STUDENT LIST ----------------
@login_required(login_url='/login/')
def student_list(request):
    query = request.GET.get('q')

    students = Student.objects.filter(user=request.user).order_by('id')

    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(course__icontains=query)
        )

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/list.html', {'page_obj': page_obj})


# ---------------- ADD STUDENT ----------------
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, "Student added successfully")
            return redirect('/')
    else:
        form = StudentForm()

    return render(request, 'students/add.html', {'form': form})


# ---------------- DELETE STUDENT ----------------
def delete_student(request, id):
    student = get_object_or_404(Student, id=id, user=request.user)
    student.delete()
    messages.success(request, "Student deleted successfully")
    return redirect('/')


# ---------------- EDIT STUDENT ----------------
def edit_student(request, id):
    student = get_object_or_404(Student, id=id, user=request.user)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully")
            return redirect('/')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit.html', {'form': form})


# ---------------- LOGIN ----------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'students/login.html', {'error': 'Invalid credentials'})

    return render(request, 'students/login.html')


# ---------------- LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect('/login/')


# ---------------- MARKS ----------------
def view_marks(request, id):
    student = get_object_or_404(Student, id=id, user=request.user)
    marks = Marks.objects.filter(student=student)

    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.student = student
            mark.save()
            return redirect(f'/marks/{id}/')
    else:
        form = MarksForm()

    total = sum(m.marks for m in marks)
    count = marks.count()
    percentage = (total / count) if count > 0 else 0

    return render(request, 'students/marks.html', {
        'student': student,
        'marks': marks,
        'form': form,
        'total': total,
        'percentage': percentage
    })


def edit_marks(request, id):
    mark = get_object_or_404(Marks, id=id, student__user=request.user)

    if request.method == "POST":
        form = MarksForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect(f'/marks/{mark.student.id}/')
    else:
        form = MarksForm(instance=mark)

    return render(request, 'students/edit_marks.html', {'form': form})


def delete_marks(request, id):
    mark = get_object_or_404(Marks, id=id, student__user=request.user)
    student_id = mark.student.id
    mark.delete()
    messages.success(request, "Marks deleted successfully")
    return redirect(f'/marks/{student_id}/')