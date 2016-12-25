from django.shortcuts import render
from django.http import HttpResponse

# Views for Students


def students_list(request):
    return render(
        request, 'students/students_list.html', {}
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

# Views for Groups


def groups_list(request):
    return HttpResponse(
        '<h1>Groups Listing</h1>'
    )


def groups_add(request):
    return HttpResponse(
        '<h1>Group Add Form</h1>'
    )


def groups_edit(request, gid):
    return HttpResponse(
        '<h1>Edit Group {} </h1>'.format(gid)
    )


def groups_delete(request, gid):
    return HttpResponse(
        '<h1>Delete Group {} </h1>'.format(gid)
    )
