from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Board
# 페이지네이션
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# CRUD
# from .forms import PostForm,NewTopicForm
from .forms import NewTopicForm,PostForm

from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now
from profile.models import Profile
from datetime import datetime

from .models import Board, Topic, Post
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from django.urls import reverse


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'blog/board.html'

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'blog/topics.html'
    # model.py의     def get_page_count(self): 숫자와 맞춰야한다.(10)
    # return self.posts.order_by('-created_date')[:10]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

# @login_required
# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 10)
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # fallback to the first page
#         topics = paginator.page(1)
#     except EmptyPage:
#         # probably the user tried to add a page number
#         # in the url, so we fallback to the last page
#         topics = paginator.page(paginator.num_pages)
    
#     return render(request, 'blog/topics.html', { 'board': board, 'topics':topics })

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                description=form.cleaned_data.get('description'),
                topic=topic,
                created_by=request.user
            )
            
            return redirect('blog:topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
        # return redirect('blog/board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    return render(request, 'blog/new_topic.html', {'board': board, 'form': form })


class PostListView(ListView):
    model = Post
    # avatar = None
    # avatar = Profile.objects.get(user=post.created_by).photo
    # 'avatar':avatar
    context_object_name = 'posts'
    template_name = 'blog/topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # 같은 유저 count 못하기
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_date')
        return queryset


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = now()
            topic.save()
            topic_url = reverse('blog:topic_posts',kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )
            # 만약에러뜬다면 REDIRECT에 blog namespace주어야한다.
            return redirect(topic_post_url)
            # return redirect('blog:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'blog/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title','description', )
    template_name = 'blog/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = now()
        post.save()
        return redirect('blog:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

# @login_required
# def post_destroy(request, pk):
#     post = Post.objects.get(pk=pk)
#     post.delete()
#     # redirect 2 notice
#     return redirect('blog:boards')

    


# @login_required
# def notice(request):
#     posts = Post.objects.all().order_by('-created_date')
#     # pagination
#     total_len = len(posts)
#     page = request.GET.get('page',1)
#     paginator = Paginator(posts,5)
    
#     try: 
#         lines = paginator.page(page) 
#     except PageNotAnInteger: 
#         lines = paginator.page(1)
#     except EmptyPage: 
#         lines = paginator.page(paginator.num_pages)
    
#     idx = lines.number -1
#     max_idx = len(paginator.page_range)
#     start_idx = idx -2 if idx >=2 else 0
#     if idx < 2:
#         end_idx = 5-start_idx
#     else:
#         end_idx = idx+3 if idx <= max_idx -3 else max_idx
    
#     page_range = list(paginator.page_range[start_idx:end_idx])
    
#     contacts = paginator.get_page(page)
#     context = {'contacts': contacts, 'result_list': lines , 'page_range':page_range, 'total_len':total_len, 'max_idx':max_idx-2 }

#     return render(request, 'blog/notice.html',context)


# # crud 구현중
# @login_required
# def post_create(request):
#     # print(get_user_model().pk) =  <property object at 0x7f4158a36b38>
#     # print(request.user.id) = 1
#     # get_user_model().profile = 
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         # 여기서 부터 user 넣어주기 시작
#         # https://tutorial.djangogirls.org/ko/django_forms/
#         if form.is_valid():
#             post = form.save(commit=False)
#             # 현재 로그인 request.user 사용 하면 된다. 
#             # post.user = Profile.objects.get(user=request.user)
#             post.created_by = request.user
#             post.save()    
#             return redirect('blog:read',pk=post.pk)
#         else:
#             print("form is not valid")
#     else: form = PostForm()
#     # # redirect to notice
#     # # render 또한 redirect 처럼 url name 으로 가져오기 가능할가?
#     return render(request, 'blog/create.html',{'form': form})
    
# # detail
# def post_read(request, pk):
#     """Display specific blog posts"""
#     post_detail = get_object_or_404(Post, pk=pk)
#     # edit 버튼 보여줄지 말지
#     flag = post_detail.created_by == request.user
#     return render(request, 'blog/read.html', {'post_detail': post_detail, 'flag':flag})
# # edit form view
# @login_required
# def post_edit(request, pk):
#     post = Post.objects.get(pk=pk)
#     # if post.user == Profile.objects.get(user=request.user):
#     if post.created_by == request.user:
#         return render(request,'blog/edit.html', {'post':post})
#     else:
#         return render(request,'blog/error.html')
# # db로 쏴주는 함수/ view 필요하지 않다.
# @login_required
# def post_update(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostForm(request.POST,instance=post)
#     print(form)
#     if form.is_valid():
#         post = form.save(commit=False)
#         # 현재 로그인 request.user 사용 하면 된다. 
#         # post.user = Profile.objects.get(user=request.user)
#         post.mod_date = now()
#         post.updated_by = request.user
#         post.save()
#     else:
#         print("form is not valid")
#     # return redirect('read',pk=form.instance.pk)
#     # return redirect('blog:read',form.instance.pk)
#     return redirect('blog:read',pk=post.pk)

