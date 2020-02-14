from django import template
from django.contrib.auth.models import Group 
import base64
import codecs

register = template.Library()

@register.filter(name="encode_js")
def encode_js(value):
    data = value.encode('utf-8')
    data = codecs.encode(data,'hex')
    return data

    # print(data)
    # data = base64.b64encode(data)   
    # return data

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 