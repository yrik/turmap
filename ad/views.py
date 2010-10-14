# Create your views here.
from django.forms import ModelForm
from models import *
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from datetime import datetime
from django.http import HttpResponseRedirect


NUM_PER_PAGE = 10


def index(request):
    
    sell = Paginator(Ad.objects.filter(type='S'), 4)
    buy = Paginator(Ad.objects.filter(type='B'), 4)

    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.date = str(datetime.now())[:-7]
            ad.save()
    else:
        form = AdForm()

    return render_to_response("main.html", {
        "formset": form,
        "sell":sell.page(1),
        "buy":buy.page(1)
    })

def links(request, page=1):
    
    items = Link.objects.all()
    paginator = Paginator(items, NUM_PER_PAGE)
    
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/links/'+str(paginator.num_pages)+'/')

    else:
        form = LinkForm()

     
    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    return render_to_response("links.html",{"items":items,"formset": form})

def main(request, type = None, page = 1):
    
    items =''
    if(type == 'buy'):
    
        paginator = Paginator(Ad.objects.filter(type='B'), NUM_PER_PAGE)
        try:
            items = paginator.page(page)
        except (EmptyPage, InvalidPage):
            items = paginator.page(paginator.num_pages)

    if(type == 'sell'):

        paginator = Paginator(Ad.objects.filter(type='S'), NUM_PER_PAGE)
        try:
            items = paginator.page(page)
        except (EmptyPage, InvalidPage):
            items = paginator.page(paginator.num_pages)
    
    return render_to_response("items.html", {
        "items":items,
        "type":type,        
    })

    return ''    

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
