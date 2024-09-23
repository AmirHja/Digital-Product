from turtledemo.sorting_animate import ssort

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User

import random
import uuid


class RegisterView(APIView):
    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(data={'message': 'phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            # return Response(data={'message': 'user already registered'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)


        code = random.randint(100000, 999999)
        cache.set(str(phone_number), code, 2 * 60)

        # send message (sms or email)

        return Response(data={'code': code}, status=status.HTTP_201_CREATED)



class GetTokenView(APIView):
    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        cached_code = cache.get(str(phone_number))

        if code != cached_code:
            user = User.objects.get(phone_number=phone_number)
            user.delete()
            return Response(data={'message': 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

        token = str(uuid.uuid4())

        return Response(data={'token': token}, status=status.HTTP_200_OK)