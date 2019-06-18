# from django import template
# # space 처리하기
# from django.template import Library
# from django.template.defaultfilters import stringfilter
# from django.utils.html import conditional_escape
# from django.utils.safestring import mark_safe
# import re
# from django.contrib.auth import user_logged_in

# register = Library()

# # https://stackoverflow.com/questions/721035/django-templates-stripping-spaces
# @register.filter
# @stringfilter
# def spacify(value, autoescape=None):
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#     return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))
# spacify.needs_autoescape = True
# register.filter(spacify)