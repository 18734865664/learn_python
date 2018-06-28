#! /usr/local/python3.4.4/bin/python3
# encoding: utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import subprocess

@csrf_exempt
def test(request):
    return_data = request.POST['return_data']
    f = open('test.txt', 'w')
    # print(os.getcwd())
    f.write(return_data)
    f.close()
    return HttpResponse(return_data)
