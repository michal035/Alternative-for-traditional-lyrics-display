from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from . import generate_qr_code
from dotenv import load_dotenv
from .models import User, Doc
import datetime
import logging
import jwt
import string
import random
import docx
import json
import os


# All of the paths need to be changed to relative paths

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'api.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=LOG_PATH, filemode='a')
logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
logger.addHandler(c_handler)


load_dotenv()
global SECRET_KEY
SECRET_KEY = os.getenv("KEY")


def barer_token_verification(token):

    token = token.replace('Bearer ', '')
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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
                token_payload, SECRET_KEY, algorithm="HS256")
            token = str(token)[2:][:-1]

            response = JsonResponse(
                {'message': 'Login successful'}, status=200)
            response.set_cookie('access_token', token, httponly=True,
                                expires=token_payload["exp"], secure=True, samesite='Strict')

            return response
            # return JsonResponse(data={"token": (str(token)[2:])[:-1], "username": username_}, status=200)
        else:
            return JsonResponse(data="Wrong credentials", status=401)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        return JsonResponse({'error': "Invalid credentials"}, status=401)


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
def get_qr(request, token):

    image_path = f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token}.jpg"
    if not os.path.exists(image_path):
        return HttpResponse("QR code not found ", status=404)
    image_file = open(image_path, 'rb')

    response = FileResponse(
        image_file, content_type='image/jpeg', status=200)

    return response


@api_view(['POST'])
@csrf_exempt
def Create_new_doc(request):
    if (authorization_header := request.META.get('HTTP_AUTHORIZATION')):
        res = barer_token_verification(authorization_header)

        if ((res := tuple(res))[0] == 200):
            username_ = (tuple(res))[1]
            user_obj = User.objects.get(username=username_)

            # Generating a token with a fixed number of characters - 20 should work just fine
            characters = string.ascii_letters + string.digits
            token_ = ''.join(random.choice(characters) for _ in range(20))

            if (not (the_doc := Doc.objects.filter(token=token_))):

                generate_qr_code.generate_qr(token_)
                new_record = Doc(token=token_, user=user_obj)
                new_record.save()

                return JsonResponse(data={"token": token_}, status=201, safe=False)
            else:
                JsonResponse(
                    data={"message": "Resource not found"}, status=404, safe=False)

        else:
            # Further investigation needed
            try:
                # int(res[1])
                return JsonResponse(data={"message": (res[0]["message"])}, status=401, safe=False,)
            except Exception as e:
                logger.error("An error occurred: %s", str(e))
                # int(res[1])
                return JsonResponse(data={"message": (res)}, status=401, safe=False)
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

    return JsonResponse(data, status=200, content_type='application/json', safe=False)


@api_view(['POST'])
def create_new_account(request):

    data = json.loads(request.body.decode('utf-8'))
    username_ = data.get("username")
    password = data.get("password")

    if (not User.objects.filter(username=username_)):
        new_record = User(username=username_, passwd=password)
        new_record.save()
        return HttpResponse("User has beeen created", status=201)
    else:
        return HttpResponse("This email already has been registered", status=409)


def non(request):
    return HttpResponseNotFound("Token not found")
