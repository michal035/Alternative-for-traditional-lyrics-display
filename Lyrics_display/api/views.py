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
from django.shortcuts import get_object_or_404
from . import generate_qr_code
from .models import User, Doc
import datetime
import jwt
import string
import random
import docx
import json
import base64


# All of the paths need to be changed to relative paths
# Some double checks are unnecessary and in some cases I need to add more - I need to log them as well

# hardcoded just for now
global secret_key
secret_key = "tncV0f771WGyvUR9U4LFtHf213NdsjJdas"


def barer_token_verification(token):

    token = token.replace('Bearer ', '')
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return {decoded_token, 200}
    except jwt.ExpiredSignatureError:
        return ({"message": "Token has expired"}, 401)
    except jwt.DecodeError:
        return ({"message": "Invalid token"}, 401)


@api_view(['POST'])
def login(request):

    data = json.loads(request.body.decode('utf-8'))
    username_ = data.get("username")
    password = data.get("password")

    try:
        user = User.objects.filter(username=username_).first()

        if ((users_password := user.passwd) == password):
            token_payload = {
                "username": username_,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(
                token_payload, secret_key, algorithm="HS256")

            print(token)
            return JsonResponse(data={"token": token, "username": username_}, status=200)
        else:
            return HttpResponse("Wrong credentials", status=401)

    except:
        # This needs to be logged
        return HttpResponse("Wrong credentials", status=401)


@api_view(['POST'])
@csrf_exempt
def upload_file(request, token_):

    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    return HttpResponse(authorization_header, status=200)
    """if request.method == 'POST' and 'file' in request.FILES:

        up_file = request.FILES['file']
        passwd = request.POST.get('code')

        the_doc = get_object_or_404(Doc, token=token_)
        if the_doc.passwd != passwd:
            # This sould be logged
            return HttpResponse('Invalid password.', status=401)

        extension = (up_file.name).split(".")[len((up_file.name).split("."))-1]
        file_name = f"file_{token_}.{extension}"

        destination = open(
            '/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/' + file_name, 'wb+')

        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()

        return HttpResponse('File uploaded successfully.', status=200)
    else:
        return HttpResponse('File upload failed.', status=400)"""


@api_view(['GET'])
def re_qr(request, token):

    image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token}.jpg"
    image_file = open(image_path, 'rb')

    response = FileResponse(image_file, content_type='image/jpeg', status=200)

    return response


@api_view(['POST'])
@csrf_exempt
def Create_new_doc(request):

    # Generating a token with a fixed number of characters - 20 should work just fine
    characters = string.ascii_letters + string.digits
    token_ = ''.join(random.choice(characters) for _ in range(20))

    the_doc = User.objects.filter(token=token_)

    # THis needs to get data from JWT
    username = "username"
    user_obj = User.objects.get(user=username)

    if not the_doc:
        new_record = Doc(token=token_, user=user_obj)
        new_record.save()
    else:
        JsonResponse(data={"message": ""}, status=500)

    generate_qr_code.generate_qr(token_)

    image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token_}.jpg"
    image_file = open(image_path, 'rb')

    response = JsonResponse(data={"token": token_}, status=200)

    return response


@api_view(['GET'])
def re(request, token):

    print(token)

    try:
        doc = docx.Document(
            f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/file_{token}.docx")
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

    # serializer = ParagraphSerializer(data=data, many=True)
    # serializer.is_valid(raise_exception=True)

    # return Response(serializer.data)

    return JsonResponse(data, status=200, content_type='application/json', safe=False)


@api_view(['GET'])
def check_for_password(request, token_):

    the_doc = get_object_or_404(Doc, token=token_)
    if the_doc.passwd != None:

        data = [{'passwd': True}]
    else:
        data = [{'passwd': False}]

    return JsonResponse(data, status=200, content_type='application/json', safe=False)


# This needs to be remade - like this is not even needed at this point
@api_view(['POST'])
def set_password(request, token_):

    body = request.data
    password = body["code"]

    record = Doc.objects.get(token=token_)
    # record.passwd = password

    record.save()

    return HttpResponse(status=201)


def non(request):
    return HttpResponseNotFound("Token not found")
