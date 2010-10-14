from django.forms import ModelForm
from models import *
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from gmapi import maps
from gmapi.forms.widgets import GoogleMap


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))


def index(request):
    gmap = maps.Map(opts = {
        'center': maps.LatLng(38, -97),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 3,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(38, -97),
    })
    maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
    info = maps.InfoWindow({
        'content': 'Hello!',
        'disableAutoPan': True
    })
    info.open(gmap, marker)

    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('index.html', context)

NUM_PER_PAGE = 10

def with_tag(request, tag, page=1 ) :

    from tagging.models import Tag,TaggedItem
    query_tag = Tag.objects.get(name=tag)
    entries = TaggedItem.objects.get_by_model(Ad, query_tag)
    entries = entries.order_by('-date')
    paginator = Paginator(entries, NUM_PER_PAGE)
    items = paginator.page(page)

    return render_to_response("with_tag.html", dict(tag=tag, items=items))

def init_tags(request):
    import string
    for item in Ad.objects.all():
        tags = (item.content).replace(" ",',')
        tags = tags.split(',')
        tags = map(lambda x: x.strip(),tags)
        tags = filter(lambda x: len(x) > 2, tags)
        item.tags = ','.join(tags)
        item.save()
