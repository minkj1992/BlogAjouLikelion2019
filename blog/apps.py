from django.apps import AppConfig
# from profile.models import Profile 

class BlogConfig(AppConfig):
    name = 'blog'
# https://stackoverflow.com/questions/25680803/django-1-7-upgrade-error-appregistrynotready-models-arent-loaded-yet/26636758#26636758
# user 넣기 문제
    # def ready(self):
    #     Post = self.get_model('Post')
    #     Post.user = Profile.objects.get(user=get_user_model())
        