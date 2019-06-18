from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from profile.models import Profile
from django.contrib.auth import get_user_model
# markdown
# from martor.models import MartorField
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import math


class Board(models.Model):
    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_date').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User,on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject
    # 모르겠다.
    def get_page_count(self):
        count = self.posts.count()
        # 20이 어디서 나온거?
        pages = count / 10
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)
        
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_date')[:10]

class Post(models.Model):
    # https://simpleisbetterthancomplex.com/series/2017/09/11/a-complete-beginners-guide-to-django-part-2.html
    topic = models.ForeignKey(Topic,null=True,on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User,on_delete=models.DO_NOTHING, null=True, related_name='+')

    # related_name이 무슨 뜻인가?
    # user
    created_by = models.ForeignKey(
        # Profile.objects.get(user=get_user_model()),
        # User,
        get_user_model(),
        null=True,  #explicitly set null, since it's required in django 2.x. - otherwise migrations will be incompatible later!
        on_delete=models.CASCADE,
        related_name='posts',
        )
    
    # https://gustnxodjs.tistory.com/1
    # one to many와 foreignkey만 설정한것의 차이는 무엇일까? 
    title = models.CharField(max_length=50,default="Title")
    created_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(blank=True, null=True)
    # description = MarkdownxField(default="# Hi I'm lion",help="마킄다운 미리보기")
    description = MarkdownxField(default="# Hi I'm lion", help_text="마크다운 형식으로 글을 작성하시오")
    # description = MartorField(default="#I'm likelion",blank=True,null=True)

    def __str__(self):
        return self.title
    
    @property
    def text_to_markdown(self):
        return markdownify(self.description)
