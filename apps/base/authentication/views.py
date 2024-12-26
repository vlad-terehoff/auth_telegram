from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import JsonResponse
import uuid
from user.models import User


def home(request):
    return render(request, 'main/index.html')


@api_view(["GET"])
@permission_classes([AllowAny])
def login(request):
    random_uuid = uuid.uuid4()
    url = f'{settings.URL_BOT}?start={random_uuid}'
    return JsonResponse({'url': url, 'auth_key': str(random_uuid)})


def success(request):
    data = request.GET.get("name")
    name = {'name': data}
    return render(request, 'main/success.html', context=name)


@api_view(["POST"])
@permission_classes([AllowAny])
def check_status_login(request):
    token = request.data.get('auth_key')
    user: User = User.objects.filter(auth_token=token).first()

    if user:
        name = user.first_name
        return JsonResponse({'status': 'auth', 'name': name})

    return JsonResponse({'status': 'not_auth'})




