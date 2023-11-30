from django import template
register = template.Library()

@register.filter
def is_liked_by_user(like, user):
    return like.user == user