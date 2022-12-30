from django.urls import reverse


def get_dynamic_url(model, url_name):
    instance = model.objects.first()
    url = reverse(url_name, args=[instance.id])

    return url
