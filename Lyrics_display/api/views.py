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




def non(request):
    return HttpResponseNotFound("Token not found")


@api_view(['POST'])
@csrf_exempt
def upload_file(request,token):

    print(token)
    # Needs to be added to db ig - yeah the file path 

    if request.method == 'POST' and 'file' in request.FILES:
        up_file = request.FILES['file']

        print(up_file.name)

        extension = (up_file.name).split(".")[len((up_file.name).split("."))-1]
        file_name = f"file_{token}.{extension}"

        destination = open('/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/' + file_name, 'wb+')

        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()  
    

        return HttpResponse('File uploaded successfully.', status=200)
    else:
        return HttpResponse('File upload failed.', status=400)




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

    print(token)

    try:
        doc = docx.Document(f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/file_{token}.docx")
    except:
        return HttpResponse(status=204)
    
    paragraphs = [p.text for p in doc.paragraphs]

    #to print(paragraphs)
    data = [{'paragraph': paragraph} for paragraph in paragraphs]

    
    index = 0
    while index < len(data) - 1:
        if data[index]['paragraph'] == '' and data[index + 1]['paragraph'] == '':
            del data[index + 1]  
        else:
            index += 1  


    #serializer = ParagraphSerializer(data=data, many=True)
    #serializer.is_valid(raise_exception=True)

    #return Response(serializer.data)


    return JsonResponse(data, status=200, content_type='application/json', safe=False)