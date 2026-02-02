from django.core.paginator import Paginator


def default_paginator(object_list, request):
    paginator = Paginator(object_list, 5)
    if request.method == "GET":
        page_number = request.GET.get('page')
    else:
        page_number = request.POST.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
