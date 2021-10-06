from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound
from .models import Person


def index(request):
    people = Person.objects.all()
    return render(request, "index.html", {"people": people})


def emulator(request):
    return render(request, "emul.html")


def create(request):
    if request.method == "POST":
        person = Person()
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.save()
        return JsonResponse({"id": person.id,
                             "name": person.name,
                             "age": person.age})


def edit(request, id):
    try:
        person = Person.objects.get(id=id)

        if request.method == "POST":
            person.name = request.POST.get("name")
            person.age = request.POST.get("age")
            person.save()
            return JsonResponse({"id": person.id,
                                 "name": person.name,
                                 "age": person.age})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def delete(request, id):
    if request.method == "DELETE":
        try:
            person = Person.objects.get(id=id)
            person.delete()
            return HttpResponse(status=200)
        except Person.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")


def detail(request, id):
    person = Person.objects.get(id=id)
    stats = person.product_set.all()
    return render(request, "detail.html", {"person": person,
                                           "stats": stats})
