from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from django.conf import settings


def home(request):
    return render(request, 'main/index.html')


@api_view(["GET"])
@permission_classes([AllowAny])
def login(request):
    return redirect(settings.URL_BOT)