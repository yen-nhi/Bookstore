from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import BookstoreUser
from api.serializers import UserRegisterSchema




@swagger_auto_schema(method='POST', request_body=UserRegisterSchema)
@api_view(['POST'])
def register(request):
    payload = request.data
    serializer = UserRegisterSchema(data=payload)
    if not serializer.is_valid():
        return Response(status=400, data={'message': 'Invalid payload.'})

    email = payload.get('email')
    if BookstoreUser.objects.filter(email=email):
        return Response(status=400, data={'message': 'User already exists.'})

    user = BookstoreUser(email=email)
    user.set_password(payload.get('password'))
    user.save()
    return Response(status=200, data={'message': 'Successfully registered.'})

@swagger_auto_schema(method='POST', request_body=UserRegisterSchema)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(BookstoreUser, email=request.data.get('email'))
    if not user.check_password(request.data.get('password')):
        return Response(status=404, data={'message': 'Invalid password.'})
    token, _ = Token.objects.get_or_create(user=user)
    return Response(status=200, data={'token': token.key})


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    user = request.user
    token = Token.objects.filter(user=user)
    if token:
        user.auth_token.delete()
    logout(request)
    return Response(status=200, data={'message': 'Successfully logged out.'})
