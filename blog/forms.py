from django import forms
from .models import Post,Topic
from markdownx.fields import MarkdownxFormField
# from martor.fields import MartorFormField
from markdownx.widgets import MarkdownxWidget

class NewTopicForm(forms.ModelForm):
    description = MarkdownxFormField()
    class Meta:
        model = Topic
        fields = ['subject', 'description']
        widgets = {
            'description': MarkdownxWidget(attrs={'class': 'textarea'}),
        }


#  post form을 생성한다. 
# https://narito.ninja/blog/detail/102/
class PostForm(forms.ModelForm):
    # description = MarkdownxFormField()
    class Meta:
        model = Post
        # fields = "__all__"
        # description 이것 넣어주어야 할까?
        fields = ('title','description',)
        # widgets = {
        #     'description': MarkdownxWidget(attrs={'class': 'textarea'}),
        # }
