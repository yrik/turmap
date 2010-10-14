# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm, Textarea
from tagging.fields import TagField
from tagging.models import Tag

class Ad(models.Model):
    TYPE_CHOICES = (
        (u'B', u'Я хочу купить'),
        (u'S', u'Я хочу продать'),
    )
    date = models.DateTimeField(blank=True,null = True)
    name = models.CharField(blank=True,max_length=150, verbose_name=u'ФИО', error_messages={'required': 'Please let us know what to call you!'})
    email = models.EmailField(blank=True, max_length=150)
    phone = models.CharField(max_length=150, verbose_name=u'Телефон')
    content = models.TextField(max_length=150, verbose_name=u'Обьявление')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, verbose_name=u'Тип обьявления')
    tags = TagField(null=True,blank=True)
    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return u"%s \n %s" % (self.content, self.date)
    
    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self) 

class Keyword(models.Model):
    value = models.CharField(max_length=150)
    ad = models.ForeignKey(Ad)    

class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ['content','type','name','phone','email']
        widgets = {
            'content': Textarea(attrs={'cols': 40, 'rows': 4}),
        }
        
class Link(models.Model):
    
    description = models.TextField(blank=True,verbose_name=u'Текстовое описание')
    text =  models.TextField(blank=True,verbose_name=u'Код текстовой ссылки')
    banner =  models.TextField(blank=True, verbose_name=u'Код баннера')

class LinkForm(ModelForm):

    class Meta:
        model = Link
        fields = ['description', 'text', 'banner']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 2}),
            'text': Textarea(attrs={'cols': 50, 'rows': 2}),
            'banner': Textarea(attrs={'cols': 50, 'rows': 2}),
        }

