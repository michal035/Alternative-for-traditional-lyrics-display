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
import os
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
        return {decoded_token["username"], 200}
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
            return JsonResponse(data={"token": (str(token)[2:])[:-1], "username": username_}, status=200)
        else:
            return HttpResponse("Wrong credentials", status=401)
    except:
        # This needs to be logged
        return HttpResponse("Wrong credentials", status=401)


@api_view(['POST'])
@csrf_exempt
def upload_file(request, token_):

    if (authorization_header := request.META.get('HTTP_AUTHORIZATION')):
        res = barer_token_verification(authorization_header)

        if ((res := tuple(res))[0] == 200):
            if request.method == 'POST' and 'file' in request.FILES:

                the_doc = get_object_or_404(Doc, token=token_)
                if (the_doc.user.username == res[1]):

                    up_file = request.FILES['file']

                    extension = (up_file.name).split(".")[
                        len((up_file.name).split("."))-1]
                    file_name = f"file_{token_}.{extension}"

                    destination = open(
                        '/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/' + file_name, 'wb+')

                    for chunk in up_file.chunks():
                        destination.write(chunk)
                    destination.close()

                    return HttpResponse('File uploaded successfully.', status=200)
            else:
                return HttpResponse('File upload failed.', status=400)
        else:
            return HttpResponse(res[0]["message"], status=int(res[1]))
    else:
        return HttpResponse("Authorization header not present", status=401)


@api_view(['GET'])
def re_qr(request, token):

    if (authorization_header := request.META.get('HTTP_AUTHORIZATION')):
        res = barer_token_verification(authorization_header)
        if ((res := tuple(res))[0] == 200):
            image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token}.jpg"
            if not os.path.exists(image_path):
                return HttpResponse("QR code not found ", status=404)
            image_file = open(image_path, 'rb')

            response = FileResponse(
                image_file, content_type='image/jpeg', status=200)

            return response
        else:
            return HttpResponse(res[0]["message"], status=int(res[1]))
    else:
        return HttpResponse("Authorization header not present", status=401)


@api_view(['POST'])
@csrf_exempt
def Create_new_doc(request):

    if (authorization_header := request.META.get('HTTP_AUTHORIZATION')):
        res = barer_token_verification(authorization_header)

        # Generating a token with a fixed number of characters - 20 should work just fine
        characters = string.ascii_letters + string.digits
        token_ = ''.join(random.choice(characters) for _ in range(20))

        if ((res := tuple(res))[0] == 200):
            username_ = (tuple(res))[1]
            user_obj = User.objects.get(username=username_)

            if (not (the_doc := Doc.objects.filter(token=token_))):
                new_record = Doc(token=token_, user=user_obj)
                new_record.save()

                return HttpResponse("Resource successfully created", status=201)
            else:
                JsonResponse(
                    data={"message": "Resource not found"}, status=404)

            generate_qr_code.generate_qr(token_)

            # image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token_}.jpg"
            # image_file = open(image_path, 'rb')

            response = JsonResponse(data={"token": token_}, status=200)

            return response
        else:
            return HttpResponse(res[0]["message"], status=int(res[1]))
    else:
        return HttpResponse("Authorization header not present", status=401)


@api_view(['GET'])
def re(request, token):

    # No need to log in for this one

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


def non(request):
    return HttpResponseNotFound("Token not found")
