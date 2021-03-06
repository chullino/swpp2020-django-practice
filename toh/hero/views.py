from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Hero

# Create your views here.
def index(request):
    return HttpResponse("hello, world!")

def hero_id(request, id=""):
    return HttpResponse(f'Your id is {id}!')

def hero_name(request, name=""):
    return HttpResponse(f'Your name is {name}!')

@csrf_exempt
def hero_list(request):
    if request.method == 'GET':
        hero_all_list = [hero for hero in Hero.objects.all().values()]
        return JsonResponse(hero_all_list, safe=False)
    elif request.method == 'POST':
        try:
            body = request.body.decode()
            hero_name = json.loads(body)['name']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        hero = Hero(name=hero_name)
        hero.save()
        response_dict = {'id': hero.id, 'name': hero.name}
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponseNotAllowed(['GET', 'POST']) 

@csrf_exempt
def hero_info(request, id=""):
    if request.method == 'GET':
        hero = [hero for hero in Hero.objects.all().filter(id=id).values()]
        return JsonResponse(hero[0], safe=False)
    elif request.method == 'PUT':
        try:
            body = request.body.decode()
            if 'name' in json.loads(body):
                name = json.loads(body)['name']
            if 'age' in json.loads(body):
                age = json.loads(body)['age']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        hero = Hero.objects.all().filter(id=id)
        hero.name = name
        hero.age = age
        response_dict = {'id': id, 'name':hero.name, 'age':hero.age}
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT'])
            
