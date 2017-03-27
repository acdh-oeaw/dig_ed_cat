from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from editions.models import Edition, Period
from collections import Counter

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


def xmltei_json(request):
    CHOICES_TEI = {
        "N/A": "N/A",
        "no information provided": "no information provided",
        "not provided": "not provided",
        "0": "XML not used",
        "0.5": "XML but not TEI",
        "1": "XML-TEI is used"
    }

    editions = Edition.objects.values(
        'tei_transcription').annotate(total=Count('tei_transcription')).order_by('-total')
    payload = []
    for x in editions:
        if x["tei_transcription"] is not None:
            legend = CHOICES_TEI[x["tei_transcription"]]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Usage of XML and TEI",
        "subtitle": "The source text is encoded in XML-TEI.",
        "legendx": "Encoding",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def editions_per_country_json(request):
    editions = Edition.objects.all()
    countries = []
    for x in editions:
        for y in x.institution.all():
            if y.place is not None:
                countries.append(y.place.part_of.name)

    countries = Counter(countries)
    payload = list(map(list, countries.items()))

    data = {
        "items": len(editions),
        "title": "Editions per country",
        "subtitle": "Geographical distribution of editions based on producing institutions.",
        "legendx": "Countries",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def images_json(request):
    CHOICES_DOWNLOAD = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "images not available"),
        ("0.5", "some images available"),
        ("1", "images available"),
        ("N/A", "N/A")
    )

    editions = Edition.objects.values(
        'images').annotate(total=Count('images')).order_by('-total')
    payload = []
    for x in editions:
        if x["images"] is not None:
            legend = dict(CHOICES_DOWNLOAD)[x["images"]]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Images?",
        "subtitle": "Are editions linked to images?.",
        "legendx": "images?",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def xmldownload_json(request):
    CHOICES_DOWNLOAD = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "no"),
        ("0.5", "partially"),
        ("1", "yes"),
        ("N/A", "N/A")
    )

    editions = Edition.objects.values(
        'download').annotate(total=Count('download')).order_by('-total')
    payload = []
    for x in editions:
        if x["download"] is not None:
            legend = dict(CHOICES_DOWNLOAD)[x["download"]]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Access to the Data",
        "subtitle": "The XML-TEI encoded text is available for download.",
        "legendx": "download possible",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def indices_json(request):
    editions = Edition.objects.values(
        'indices').annotate(total=Count('indices')).order_by('-total')
    payload = []
    for x in editions:
        if x["indices"] is not None:
            legend = x["indices"]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Indices provided",
        "subtitle": "Is the edition's content accessable by indices?",
        "legendx": "indices",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def cc_json(request):
    editions = Edition.objects.values(
        'cc_license').annotate(total=Count('cc_license')).order_by('-total')
    payload = []
    for x in editions:
        if x["cc_license"] is not None:
            legend = x["cc_license"]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Creative Commons License",
        "subtitle": "Is the work published using a Creative Commons-license",
        "legendx": "cc-license",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def advanced_search_json(request):
    editions = Edition.objects.values(
        'advanced_search').annotate(total=Count('advanced_search')).order_by('-total')
    payload = []
    for x in editions:
        if x["advanced_search"] is not None:
            legend = x["advanced_search"]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Advanced Search Functionalites",
        "subtitle": "Are there any advanced search functionalites available?",
        "legendx": "advanced search",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def search_json(request):
    editions = Edition.objects.values(
        'search').annotate(total=Count('search')).order_by('-total')
    payload = []
    for x in editions:
        if x["search"] is not None:
            legend = x["search"]
            entry = [legend, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Full Text Search",
        "subtitle": "Is the work searchable in its full text (string match search)?",
        "legendx": "searchable",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)


def historical_periode_json(request):
    editions = Edition.objects.values(
        'historical_period').annotate(total=Count('historical_period')).order_by('-total')
    payload = []
    for x in editions:
        if x["historical_period"] is not None:
            temp_period = Period.objects.get(id=x["historical_period"])
            entry = [temp_period.name, x['total']]
            payload.append(entry)

    data = {
        "items": len(Edition.objects.all()),
        "title": "Editions per Period",
        "subtitle": "Distribution of Editions over Periods",
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
