import collections
import json
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from collections import Counter
from sklearn.cluster import KMeans
from django.contrib.contenttypes.models import ContentType
from browsing.views import serialize
from editions.models import Edition


def hashed(string):
    return hash(string)


def kmeans_json(request):
    selected_class = ContentType.objects.get(app_label="editions", model="edition")

    value_list = []
    for x in selected_class.get_all_objects_for_this_type():
        values = serialize(x)
        value_list.append(values)

    headers = [f.name for f in Edition._meta.get_fields()]
    df = pd.DataFrame(value_list, columns=headers)
    df.index = pd.DataFrame(df[df.columns[2]].tolist())
    df = df[['scholarly', 'digital', 'edition', 'api', 'language']]
    df = df.applymap(hashed)
    X = np.array(df)
    kmeans = KMeans(random_state=0).fit(X)
    cluster = dict(collections.Counter(kmeans.labels_))
    payload = []
    for key, value in cluster.items():
        payload.append([int(key), int(value)])

    data = {
        "items": len(Edition.objects.all()),
        "title": "Kmeans of Editions (experimental)",
        "subtitle": "Vectorizes the cataloge entries and clusters them by 'k-means'.",
        "legendx": "Cluster",
        "legendy": "# of Editions",
        "measuredObject": "Editions",
        "ymin": 0,
        "payload": payload
    }

    return JsonResponse(data)
