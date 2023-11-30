#this should be at the top of your custom template tags file
#in templatetags directory in your app and don't forget to add also an __init__.py file
from django.template import Library
from django.template.defaultfilters import stringfilter
import re

register = Library()

#custom template filter - place this in your custom template tags file
@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True

@register.filter
@stringfilter
def remove_excess_linebreaks(text):
    text = re.sub('  ',' ', text)
    text = re.sub('   ',' ', text)
    text = re.sub(' <br> ','<br>', text)
    text = re.sub(' <br>','<br>', text)
    text = re.sub('<br> ','<br>', text)
    text = re.sub('<br><br><br>','<br>', text)
    text = re.sub('<br><br>','<br>', text)
    return text
remove_excess_linebreaks.is_safe = True

# @register.filter
# @stringfilter
# def remove_excess_linebreaks(text):
#     text = re.sub(r'(<br>){2,}','<br>', text)
#     return text
# remove_excess_linebreaks.is_safe = True
