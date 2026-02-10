from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import UserConfirmCode
from .utils import generate_confirm_code


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    Serializer.is_valid(raise_exception=True)


    data = serializer.validated_data
    username = data['username']
    password = data['password']

    user = authenticate(username=username, password=password)

    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)


    data = serializer.validated_data


    user = User.objects.create_user(
        username = data['username'],
        email=data['email'],
        password = data['password'],
        is_active=False
    )


    code = generate_confirm_code()
    UserConfirmCode.objects.create(
        user=user,
        code=code
    )

    return Response(
        {
            "message": "User created. Confirm eamil.",
            "user_id": user.id
        },
        status=status.HTTP_201_CREATED,
        )


@api_view(['POST'])
def confirm_user_api_view():
    serializer = UserConfirmSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)


    data = serializer.validated_data
    user_id = data['user_id']
    code = data['cose']


    try:
        confirm = UserConfirmCode.objects.get(
            user_id=user_id,
            code=code
        )
    except UserConfirmCode.DoesNotExist:
        return Response(
            {"error": "Invalid confirm code!"},
            status=status.HTTP_400_BAD_REQUEST
        )


    user = confirm.user
    user.is_active = True
    user.save()

    confirm.delete()

    return Response(
        {"message": "User confirmed successfully"},
        status=status.HTTP_200_ok
    )