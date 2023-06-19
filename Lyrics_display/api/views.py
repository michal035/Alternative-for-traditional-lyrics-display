from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .serializers import ParagraphSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from . import generate_qr_code
import string
import random
import docx
import json 


#All of the paths need to be changed to relative paths
# Some double checks are unnecessary and in some cases I need to add more - I need to log them as well

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



@api_view(['GET'])
def re_qr(request, token):

    image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token}.jpg"
    image_file = open(image_path, 'rb')

    response = FileResponse(image_file, content_type='image/jpeg')
    
    response.status_code = 200

    return response



@api_view(['POST'])
@csrf_exempt
def Create_new_doc(request):
   
    code = json.loads(request.body)
    code = code['code']
    print(code)
    # Generating a token with a fixed number of characters - 20 should work just fine  
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(20))
    
    #There needs to be check done in DB, if this token already exists 
    # code + token added to DB

    generate_qr_code(token)

    image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token}.jpg"
    image_file = open(image_path, 'rb')

    response = FileResponse(image_file, content_type='image/jpeg')

    response['token'] = token
    response.status_code = 200

    return response



@api_view(['GET'])
def re(request, token):

    print(token)

    try:
        doc = docx.Document(f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/file_{token}.docx")
    except:
        return HttpResponse(status=204)
    
    paragraphs = [p.text for p in doc.paragraphs]

    data = [{'paragraph': paragraph} for paragraph in paragraphs]

   
    # I guess different 'real' paragraphs my be seperated by double blank lines or so 
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