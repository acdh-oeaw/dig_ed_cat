from django.shortcuts import render
from collections import defaultdict
from django.http import JsonResponse
from editions.models import Edition


def get_strings(names):
    """ returns a list o fwordfrequences of propertie values in the database"""
    names_string = " ".join(names)
    d = defaultdict(int)
    for word in names_string.split():
        d[word] += 1
    wordcount = dict(d)
    word_list = []
    for key, value in wordcount.items():
        temp = [key, value]
        word_list.append(temp)

    return word_list


def show(request):
    context = {"test": "test"}
    return render(request, 'wordcloud/canvas.html', context)


def titlewords_js(request):
    names = [(x.name).lower() for x in Edition.objects.all()]
    payload = get_strings(names)
    data = {
        "title": "Names/Titles of the Editions",
        "payload": payload
    }

    return JsonResponse(data)


def infrastructure_js(request):
    names = [(x.infrastructure).lower() for x in Edition.objects.all()]
    payload = get_strings(names)
    data = {
        "title": "Infrastructure used",
        "payload": payload
    }

    return JsonResponse(data)
