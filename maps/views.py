from django.shortcuts import render


def maps(req):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(req, 'maps/maps.html', {'mapbox_access_token': mapbox_access_token})
