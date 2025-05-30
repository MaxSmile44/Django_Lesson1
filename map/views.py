from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('''<!DOCTYPE html>
<html>
<head>
  <title>Стартовая</title>
</head>
<body>
  <h1>Здесь будет карта</h1>
</body>
</html>''')