from django.db import models
from django.conf import settings
from django.utils import timezone
# one2one
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from sorl.thumbnail import ImageField, get_thumbnail

# Create your models here.
class Profile(models.Model):
    # ONE2ONE
    # null=True, blank=True 를 사용하여 user만 먼저 만들어도 되도록 하였다.
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 응 안됨 ㅋ
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=10)
    # email = models.EmailField(default="minkj1992@gmail.com")
    phone = models.CharField(max_length=13, default="01095673530")
    major = models.CharField(max_length=100, default="영어영문")
    
    # 사진 / media
    photo = models.ImageField(null=True, upload_to='profile')
    # 운영진 여부/ boolean type
    lion = models.BooleanField(default=False)
    grade = models.CharField(max_length=2, default="12")
    purpose = models.TextField(default="지원동기")
    service = models.TextField(default="만들고싶은서비스")
    proj_exp = models.TextField(default="프로젝트 경험")
    domain = models.TextField(default="관심분야")
    
    portfolio = models.URLField(default="www.naver.com")
    # 여기에 list형식으로 숙제에 대한 
    
    # admin페이지에서 이름을 보여주는 코드
    def __str__(self):
        return self.name
    
    def summary(self):
        return self.purpose[:20]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()