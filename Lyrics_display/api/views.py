from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from rest_framework.response import Response
from rest_framework.decorators import api_view



def non(request):
    return HttpResponseNotFound("Token not found")


@api_view(['GET'])
def re(request, token):
    return Response(token)