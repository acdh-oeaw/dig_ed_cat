from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from editions.models import Edition, Period

DATA = {"status": "ok",
        "query": "api:graph",
        "timestamp": "2016-07-21T09:56:36.803Z",
        "items": "7",
        "title": "LASK4EVER",
        "subtitle": "This is just a test to check if everythin works as expected.",
        "legendx": "Club",
        "legendy": "# of Victories",
        "measuredObject": "Victories",
        "ymin": -10,
        "payload": [
            ["Club", "# of Victories"],
            ["LASK", 10],
            ["Real Madrid", 4],
            ["Rapid Wien", 0],
            ["Blau Weiß Linz", -10]
        ]
        }

DATA_PIECHART = {
    "items": "2",
    "title": "LASK4EVER",
    "subtitle": "This is just a test.",
    "measuredObject": "# of Victories",
    "payload": [
        ["LASK", 9], ["Blau Weiß Linz", 1]
    ]
}


def barcharts_view(request):
    context = {"test": "test"}
    return render(request, 'charts/bar_charts.html', context)


def piecharts_view(request):
    context = {"test": "test"}
    return render(request, 'charts/pie_charts.html', context)


def historical_periode_json(request):
    editions = Edition.objects.values('historical_period').annotate(total=Count('historical_period')).order_by('-total')
    payload = []
    for x in editions:
        if x["historical_period"] is not None:
            temp_period = Period.objects.get(id=x["historical_period"])
            entry = [temp_period.name, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Editions per Period",
        "subtitle": "Distribution of Editions over Regions",
        "legendx": "Historical Periods",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }
    return JsonResponse(data)


def test_json(request):
    data = DATA
    return JsonResponse(data)


def test_json_pie(request):
    data = DATA_PIECHART
    return JsonResponse(data)
