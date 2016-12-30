# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students


def students_list(request):
    students = (
        {
            'id': 1,
            'first_name': u'Віталій',
            'last_name': u'Подоба',
            'ticket': 235,
            'image': 'img/st1.jpg'
        },
        {
            'id': 2,
            'first_name': u'Корост',
            'last_name': u'Андрій',
            'ticket': 2123,
            'image': 'img/st2.jpg'
        },
        {
            'id': 3,
            'first_name': u'Притула',
            'last_name': u'Тарас',
            'ticket': 5332,
            'image': 'img/st3.jpg'
        }
    )
    return render(
        request, 'students/students_list.html',
        {'students': students}
    )


def students_add(request):
    return HttpResponse(
        '<h1>Student Add Form</h1>'
    )


def students_edit(request, sid):
    return HttpResponse(
        '<h1>Edit Student {} </h1>'.format(sid)
    )


def students_delete(request, sid):
    return HttpResponse(
        '<h1>Delete Student {} </h1>'.format(sid)
    )
