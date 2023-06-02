from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .serializers import ParagraphSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import docx



doc = docx.Document('/home/michal/Downloads/Document155.docx')
paragraphs = [p.text for p in doc.paragraphs]

data = [{'paragraph': paragraph} for paragraph in paragraphs]



def non(request):
    return HttpResponseNotFound("Token not found")




@api_view(['GET'])
def re(request, token):

    serializer = ParagraphSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
