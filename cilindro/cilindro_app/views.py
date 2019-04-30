from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *


@csrf_exempt
def clase_list (request):
    '''
    Lista de clases de empaques
    '''
    if request.method == 'GET':  # Obtener todas las clases
        clases = Clase.objects.all()
        serializer = ClaseSerializer(clases, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST': # Agregar una nueva clase
        data = JSONParser().parse(request)
        serializer = ClaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def clase_detail (request, pk):
    '''
    Detalle de clases
    '''
    try:
        clase = Clase.objects.get(pk=pk)
    except Clase.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClaseSerializer(clase)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ClaseSerializer(clase, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        clase.delete()
        return HttpResponse(status=204)


