# -*- coding: utf-8 -*-
from ..models import Student, Group

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Views for Students


def students_list(request):
    students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        students = paginator.page(paginator.num_pages)

    return render(
        request, 'students/students_list.html',
        {'students': students}
    )


def students_add(request):
    # Якщо форма була запощена:
    if request.method == "POST":
        # Якщо кнопка скасувати була натиснута:
        if request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            return HttpResponseRedirect(reverse('home'))

        # Якщо кнопка додати була натиснута:
        if request.POST.get('add_button') is not None:

            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}

            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо студента
                student = Student(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    ticket=request.POST['ticket'],
                    student_group=Group.objects.get(
                        pk=request.POST['student_group']
                    ),
                    photo=request.FILES['photo'],
                    notes=request.POST['notes'],
                )
                # Зберігаємо студента в базу
                student.save()
                # Повертаємо користувача до списку студентів
                return HttpResponseRedirect(reverse('home'))

            # Якщо дані були введені некоректно:
            else:
                # Віддаємо шаблон форми разом зі знайденими помилками та
                # попередніми введеними даними користувача
                return render(
                    request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                     'errors': errors}
                )

    # Якщо форма не була запощена:
    # повертаємо код початкового стану форми
    return render(
        request, 'students/students_add.html',
        {'groups': Group.objects.all().order_by('title')}
    )


def students_edit(request, sid):
    return HttpResponse(
        '<h1>Edit Student {} </h1>'.format(sid)
    )


def students_delete(request, sid):
    return HttpResponse(
        '<h1>Delete Student {} </h1>'.format(sid)
    )
