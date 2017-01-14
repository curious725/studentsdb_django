# -*- coding: utf-8 -*-
from datetime import datetime
from ..models import Student, Group

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm

from django.views.generic import UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
# Views for Students


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse(
            'students_edit', kwargs={'pk': kwargs['instance'].id}
        )
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'{}?status_message=Студента успішно збережено!'.format(
            reverse('home')
        )

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'{}?status_message=Редагування студента відмінено'.format(
                    reverse('home')
                )
            )
        else:
            return super(StudentUpdateView, self).post(
                request, *args, **kwargs
            )


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'{}?status_message=Студента успішно видалено!'.format(
            reverse('home')
        )


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
            return HttpResponseRedirect(
                u"{}?status_message=Додавання студента скасовано!".format(
                    reverse('home')
                )
            )

        # Якщо кнопка додати була натиснута:
        if request.POST.get('add_button') is not None:

            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}
            # validate student data will go here
            data = {
                'middle_name': request.POST.get('middle_name'),
                'notes': request.POST.get('notes')
            }
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати " \
                        u"(напр. 1993-12-30)"
                data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть групу для студента"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо студента
                student = Student(**data)
                # Зберігаємо студента в базу
                student.save()
                # Повертаємо користувача до списку студентів
                return HttpResponseRedirect(
                    u"{}?status_message=Студента {} {} {} успішно додано!".
                    format(
                        reverse('home'), data['first_name'],
                        data['last_name'], data['middle_name']
                    )
                )

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
