from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .serializers import ParagraphSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import docx
import json 


doc = docx.Document('/home/michal/Downloads/Document155.docx')
paragraphs = [p.text for p in doc.paragraphs]

data = [{'paragraph': paragraph} for paragraph in paragraphs]



def non(request):
    return HttpResponseNotFound("Token not found")



@api_view(['POST'])
@csrf_exempt
def upload_file(request):
    up_file = request.FILES['file']
    print(up_file.name)
    destination = open('/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/' + up_file.name, 'wb+')
    for chunk in up_file.chunks():
        destination.write(chunk)
    destination.close()  

    
    #response = HttpResponse(content_type='application/octet-stream')
    #response['Content-Disposition'] = 'attachment; filename=' + up_file.name
    response = HttpResponse("Block")
    
    return HttpResponse('File upload failed.', status=200)




"""
@api_view(['POST'])
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            

            return JsonResponse({'message': 'File upload successful'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
"""       


@api_view(['GET'])
def re(request, token):

    serializer = ParagraphSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data)
