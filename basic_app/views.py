from django.shortcuts import render,redirect,get_object_or_404
from .form import UserForm,UserProfileForm, PostForm,GroupForm,UserProfileInfoForm,PostGroupForm,PageForm,PostPageForm
from django.views.generic import View ,TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView
from .models import UserProfileInfo,Image,Group,Post, Comment, Like,FriendRequest,Story,PostGroup,ImageGroup,CommentGroup,Page,ImagePage,CommentPage,PostPage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from . import models
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from django.db.models import Q
from django.utils import timezone
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')
class CBView(View):
    def get(self,request):
        return HttpResponse("CLASS BASED VIEWS ARE COOL !")

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = 'BASIC INJECTION !'
        return context
    
class SchoolListView(ListView):
    context_object_name = 'school_list'
    model = models.School

class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'basic_app/school_detail.html'

class SchoolCreateView(CreateView):
    fields = ("name","principal","location")
    model = models.School
class SchoolUpdateView(UpdateView):
    fields = ("name","principal")
    model = models.School
class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy("basic_app:list")


@login_required
def special(request):
    return HttpResponse('You are logged in ! ')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


#lấy dữ liệu profile
def profile(request):
    user_profile = UserProfileInfo.objects.get(user=request.user)
    posts = models.Post.objects.filter(user=user_profile)
    posts = posts.order_by('-created_at')
    all_images = Image.objects.filter(post__in=posts)
    friends = user_profile.friends.all()
    comments = Comment.objects.filter(post__user=user_profile).select_related('post', 'author').order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'comment':
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            post = Post.objects.get(id=post_id)
            user = user_profile
            comment = Comment(content=content, author=user, post=post)
            comment.save()
            return redirect('profile')
        elif action == 'post':
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                # Lưu bài viết vào database
                post = form.save(commit=False)
                post.user = user
                post.save()

                # Lưu đường dẫn ảnh vào database
                images = request.FILES.getlist('images')
                for image in images:
                    Image.objects.create(post=post, images=image)
            return redirect('profile')

    return render(request, 'profile.html', {'friends':friends,'user_profile': user_profile,'posts': posts,'comments': comments,'all_images': all_images})
def profileindex(request):
    user_profile = UserProfileInfo.objects.get(user=request.user) or None
    # lấy friend
    friends = user_profile.friends.all()
    # lấy group
    groups = Group.objects.all().order_by('-id')
    # lấy post
    friend_ids = friends.values_list('user__id', flat=True) # lấy danh sách id người dùng bạn bè
    posts = Post.objects.filter(Q(user_id=user_profile.id) | Q(user_id__in=friend_ids))# lấy bài đăng của những người dùng trong danh sách trên
    posts = posts.order_by('-created_at')
    # comments = Comment.objects.filter(post__user=request.user).select_related('post', 'author').order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')
    story = Story.objects.all().order_by('-created_at')
    

    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'comment':
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            post = Post.objects.get(id=post_id)
            user = request.user
            comment = Comment(content=content, author=user, post=post)
            comment.save()
            return redirect('profileindex')
        elif action == 'post':
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                # Lưu bài viết vào database
                post = form.save(commit=False)
                post.user = user_profile
                post.save()

                # Lưu đường dẫn ảnh vào database
                images = request.FILES.getlist('images')
                for image in images:
                    Image.objects.create(post=post, images=image)
            return redirect('profileindex')
        elif action == 'story':
            title = request.POST.get('titleStory')
            images = request.FILES.getlist('images')
            image1 = request.POST.get('images')
            user = request.user         
            story = Story( user=user_profile, images=image1, title=title)
            story.save()
            return redirect('profileindex')
        elif action == 'like':
            post_id = request.POST.get('post_id')
            existing_like = Like.objects.filter(user=user_profile, post_id=post_id).first()
    
            if existing_like:   
                unlike = Like.objects.filter(user=user_profile, post_id=post_id)
                unlike.delete()
                return redirect('profileindex')
            else:
                like = Like( user=user_profile, post_id =post_id)
                like.save()           
                return redirect('profileindex')
    
    return render(request, 'index.html', {'story':story,'groups':groups,'user_profile': user_profile,'posts': posts,'friends':friends,'comments':comments})

def other_profile(request,id):
    user_profile = UserProfileInfo.objects.get(user=request.user)
    user = UserProfileInfo.objects.get(user_id=id)
    
    posts = models.Post.objects.filter(user=user)
    posts = posts.order_by('-created_at')
    all_images = Image.objects.filter(post__in=posts)
    friends = user.friends.all()
    comments = Comment.objects.filter(post__user=user).select_related('post', 'author').order_by('-created_at')
    check=are_friends(user_profile.user,user.user)
    check_block=are_block(user_profile ,user.user)
    return render(request, 'otherprofiles.html', {'are_block':check_block,'are_friends':check,'friends':friends,'user':user,'user_profile': user_profile,'posts': posts,'comments': comments,'all_images': all_images})
# đăng nhập ,đăng ký
def logout_view(request):
    logout(request)
    return redirect(user_login)
def register(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()
    profile_picture = None  # Initialize with a default value

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        portfolio_site = request.POST['portfolio_site']
        if 'profile_pic' in request.FILES:
            profile_picture = request.FILES['profile_pic']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.portfolio_site = portfolio_site
        user.save()

        profile = UserProfileInfo.objects.create(user=user, portfolio_site=portfolio_site, profile_pic=profile_picture,nickname=username)
       
        profile.save()
        registered = True

    return render(request, 'registration.html', {'registered': registered, 'user_form': user_form, 'profile_form': profile_form})
# @login_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('profileindex'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and fail !')
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'login.html',{})
# post
@login_required
def create_post(request):
    print(request.user)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            # Lưu bài viết vào database
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Lưu đường dẫn ảnh vào database
            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(post=post, images=image)

            return redirect('profileindex')
    else:
        form = PostForm()

    return render(request, 'postBolg.html', {'form': form})
@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)
    user = request.user
    try:
        like = Like.objects.get(user=user, post=post)
        like.delete()
        return JsonResponse({'status':'ok', 'message': 'unlike'})
    except Like.DoesNotExist:
        like = Like(user=user, post=post)
        like.save()
        return JsonResponse({'status':'ok', 'message': 'like'})
@login_required
def get_comments(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().values_list('text', flat=True)
    return JsonResponse({'comments': list(comments)})
@login_required
def delete_post(request):
    if request.method == 'POST':
      
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        img = Image.objects.filter(post = post)     
        img.delete()
        post.delete()

    return redirect('profile')
@login_required
def edit_post(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)
    img = Image.objects.filter(post = post)
    # post = get_object_or_404(Post, id=post_id)

    created_at = post.created_at
    
    if request.method == 'POST':
        # lấy thông tin từ form
        post.user = request.user
        post.title = request.POST.get('title')
        post.created_at = created_at
        post.save()
        

        img.delete()
    # for image in img:
    #     image.delete()
    # lấy danh sách các ảnh mới từ request.FILES
        images = request.FILES.getlist('images')
    # lưu trữ các ảnh mới vào database và gán chúng cho bài viết
        for image in images:
            Image.objects.create(post=post, images=image)
            
        # lưu lại post đã sửa

        return redirect('profile')

    return render(request, 'profile.html', {'post': post})

# Group
def all_groups(request):
    groups = Group.objects.all().order_by('-id')
    user_profile = UserProfileInfo.objects.get(user=request.user)
    friends = user_profile.friends.all()
    group_user = Group.objects.filter(Q(members =user_profile))
    group_userk = Group.objects.exclude(Q(members =user_profile))

    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'add_group':
            form = GroupForm(request.POST, user_profile=user_profile)
            if form.is_valid():
                group = form.save()
                messages.success(request, 'Your group has been created!')
                return redirect('all_groups')
        if action == 'add_members':
            group_id = request.POST.get('group_id')
            group = Group.objects.get(id=group_id)
            user = user_profile
            group.members.add(user)
            return redirect('all_groups')
        if action == 'exit_group':
            group_id = request.POST.get('group_id')
            group = Group.objects.get(id=group_id)
            user = user_profile
            group.members.remove(user)
            group.ad_group.remove(user)

            return redirect('all_groups')

    else:
        form = GroupForm(user_profile=user_profile)  
    return render(request, 'group.html', {'group_userk':group_userk,'group_user':group_user,'friends':friends,'groups': groups,'user_profile': user_profile ,'form':form})
def groupindex(request,id):
    user_profile = UserProfileInfo.objects.get(user=request.user) or None
    # lấy friend
    friends = user_profile.friends.all()
    # lấy group
    groups_request = Group.objects.get(id = id)
    groups = Group.objects.all().order_by('-id')
    # lấy post
    # posts = PostGroup.objects.filter(Q(group=groups_request) | Q(members=friend_ids))# lấy bài đăng của những người dùng trong danh sách trên
    posts = PostGroup.objects.filter(Q(group=groups_request) ) # lấy bài đăng của những người dùng trong danh sách trên
    posts = posts.order_by('-created_at')
    comments = CommentGroup.objects.all().order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'comment':
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            post = PostGroup.objects.get(id=post_id)
            comment = CommentGroup(content=content, author=user_profile, post=post)
            comment.save()
            return redirect('groupindex', id = id)
        elif action == 'post':
            form = PostGroupForm(request.POST,request.FILES)
            if form.is_valid():
                # Lưu bài viết vào database
                post = form.save(commit=False)
                post.user = user_profile
                post.group = groups_request
                post.save()

                # Lưu đường dẫn ảnh vào database
                images = request.FILES.getlist('images')
                for image in images:
                    ImageGroup.objects.create(post=post, images=image)
                return redirect('groupindex', id = id)
        elif action == 'delete_post':        
            post_id = request.POST.get('post_id')
            post = PostGroup.objects.get(id=post_id)
            img = ImageGroup.objects.filter(post = post)     
            img.delete()
            post.delete()
            return redirect('groupindex', id = id)
        

    return render(request, 'groupindex.html', {'groups_request':groups_request,'groups':groups,'user_profile': user_profile,'posts': posts,'friends':friends,'comments':comments})
def group_member(request,id):
    user_profile = UserProfileInfo.objects.get(user=request.user) or None
    # lấy friend
    friends = user_profile.friends.all()
    # lấy group
    groups = Group.objects.all().order_by('-id')
    groups_request = Group.objects.get(id = id)
    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'exit_group':
            user = request.POST.get('member_id')
            groups_request.members.remove(user)
            groups_request.ad_group.remove(user)

            return redirect('group_members', id = id)
        if action == 'authorization':
            user_id = request.POST.get('member_id')
            user = UserProfileInfo.objects.get(user__id=user_id)
            groups_request.ad_group.add(user)
            return redirect('group_members', id = id)
        if action == 'remove_ad':
            user_id = request.POST.get('member_id')
            user = UserProfileInfo.objects.get(user__id=user_id)
            groups_request.members.add(user)
            groups_request.ad_group.remove(user)
            return redirect('group_members', id = id)
        if action == 'out_group':
            groups_request.members.remove(user_profile)
            groups_request.ad_group.remove(user_profile)
            return redirect('all_groups')


    return render(request, 'group_member.html', {'groups_request':groups_request,'groups':groups,'user_profile': user_profile,'friends':friends})
@login_required
def delete_group(request):
    if request.method == 'POST':
        # lấy group cần xóa
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)

        # xóa group
        group.delete()

    return redirect('all_groups')
@login_required
def edit_group(request):
    # group = get_object_or_404(Group, id=group_id)
    group_id = request.POST.get('group_id')
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        # lấy thông tin từ form
        group.name = request.POST.get('name')
        group.description = request.POST.get('description')

        # lưu lại group đã sửa
        group.save()

        return redirect('all_groups')
    
    return render(request, 'group.html', {'group': group})

# page
def all_page(request):
    groups = Group.objects.all().order_by('-id')
    user_profile = UserProfileInfo.objects.get(user=request.user)
    friends = user_profile.friends.all()
    pages = Page.objects.all().order_by('-id')

    page_user = Page.objects.filter(Q(follow=user_profile))
    page_userk = Page.objects.exclude(Q(follow=user_profile))

    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'add_page':
            form = PageForm(request.POST, user_profile=user_profile)
            if form.is_valid():
                group = form.save()
                messages.success(request, 'Your page has been created!')
                return redirect('all_page')
        if action == 'add_follow':
            group_id = request.POST.get('page_id')
            group = Page.objects.get(id=group_id)
            user = user_profile
            group.follow.add(user)
            return redirect('all_page')
        if action == 'exit_page':
            group_id = request.POST.get('page_id')
            group = Page.objects.get(id=group_id)
            user = user_profile
            group.follow.remove(user)

            return redirect('all_page')

    else:
        form = PageForm(user_profile=user_profile)  
    return render(request, 'page.html', {'pages':pages,'page_user':page_user,'page_userk':page_userk,'friends':friends,'groups': groups,'user_profile': user_profile ,'form':form})
@login_required
def edit_page(request):
    # group = get_object_or_404(Group, id=group_id)
    page_id = request.POST.get('page_id')
    page = Page.objects.get(id=page_id)
    if request.method == 'POST':
        # lấy thông tin từ form
        page.name = request.POST.get('name')
        page.description = request.POST.get('description')

        # lưu lại group đã sửa
        page.save()

        return redirect('all_page')
    
    return render(request, 'page.html', {'page': page})
@login_required
def delete_page(request):
    if request.method == 'POST':
        # lấy group cần xóa
        page_id = request.POST.get('page_id')
        page = Page.objects.get(id=page_id)

        # xóa group
        page.delete()

    return redirect('all_page')
def page_index(request,id):
    user_profile = UserProfileInfo.objects.get(user=request.user) or None
    # lấy friend
    friends = user_profile.friends.all()
    # lấy group
    page_request = Page.objects.get(id = id)
    groups = Group.objects.all().order_by('-id')
    # lấy post
    posts = PostPage.objects.filter(Q(page=page_request) ) # lấy bài đăng của những người dùng trong danh sách trên
    posts = posts.order_by('-created_at')
    comments = CommentPage.objects.all().order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'comment':
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            post = PostPage.objects.get(id=post_id)
            comment = CommentPage(content=content, author=user_profile, post=post)
            comment.save()
            return redirect('page_index', id = id)
        elif action == 'post':
            form = PostPageForm(request.POST,request.FILES)
            if form.is_valid():
                # Lưu bài viết vào database
                post = form.save(commit=False)
                post.user = user_profile
                post.page = page_request
                post.save()

                # Lưu đường dẫn ảnh vào database
                images = request.FILES.getlist('images')
                for image in images:
                    ImagePage.objects.create(post=post, images=image)
                return redirect('page_index', id = id)
        elif action == 'delete_post':        
            post_id = request.POST.get('post_id')
            post = PostPage.objects.get(id=post_id)
            img = ImagePage.objects.filter(post = post)     
            img.delete()
            post.delete()
            return redirect('page_index', id = id)
        

    return render(request, 'page_index.html', {'page_request':page_request,'groups':groups,'user_profile': user_profile,'posts': posts,'friends':friends,'comments':comments})
def page_follow(request,id):
    user_profile = UserProfileInfo.objects.get(user=request.user) or None
    # lấy friend
    friends = user_profile.friends.all()
    # lấy group
    pages = Page.objects.all().order_by('-id')
    page_request = Page.objects.get(id = id)
    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'exit_group':
            user = request.POST.get('member_id')
            page_request.follow.remove(user)
            page_request.ad_page.remove(user)

            return redirect('page_follow', id = id)
        if action == 'authorization':
            user_id = request.POST.get('member_id')
            user = UserProfileInfo.objects.get(user__id=user_id)
            page_request.ad_page.add(user)
            return redirect('page_follow', id = id)
        if action == 'remove_ad':
            user_id = request.POST.get('member_id')
            user = UserProfileInfo.objects.get(user__id=user_id)
            page_request.follow.add(user)
            page_request.ad_page.remove(user)
            return redirect('page_follow', id = id)
        if action == 'out_group':
            page_request.follow.remove(user_profile)
            page_request.ad_page.remove(user_profile)
            return redirect('all_page')


    return render(request, 'page_flollow.html', {'groups_request':page_request,'groups':pages,'user_profile': user_profile,'friends':friends})


# tìm kiếm
def search(request):
    user_profile = UserProfileInfo.objects.get(user=request.user) or None
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()

    # Xử lý GET request
    query = request.GET.get('q')
    # Nếu query không tồn tại hoặc trống thì trả về kết quả trang chủ
    if not query or query.strip() == '':
        messages.warning(request, 'Không tìm thấy kết quả, hãy thử lại với từ khóa khác.')
        return redirect(reverse('profileindex'))
    # Tìm kiếm Post, Friend và Group theo title, name friend và name group
    result_list = []

# Tìm kiếm trong user
    user  = UserProfileInfo.objects.filter(user__username__contains=query)
    result_list.append(user)
# Tìm kiếm trong Group
    group = Group.objects.filter( name__contains=query)
    result_list.append(group)
# Gộp tất cả kết quả lại thành một list
    results = list(chain(*result_list))
    
    return render(request,'search.html', {'friends':friends,'groups':groups,'query':query,'results': results,'user_profile': user_profile})
    

# hàm bổ sung
def are_friends(user1, user2):
    user1_profile = UserProfileInfo.objects.get(user=user1)
    user2_profile = UserProfileInfo.objects.get(user=user2)
    if user1_profile == user2_profile:
        return '0'
    if user1_profile.friends.filter(user=user2).exists() and user2_profile.friends.filter(user=user1).exists():
        return '1'
    else:
        return '2'
def common_friends(user1, user2):
    user1_profile = UserProfileInfo.objects.get(user=user1)
    user2_profile = UserProfileInfo.objects.get(user=user2)

    friend_list1 = user1_profile.friends.all()
    friend_list2 = user2_profile.friends.all()

    common_list = friend_list1.intersection(friend_list2)

    return common_list

# setting profile
def setting_profile(request):
    # Lấy ra đối tượng UserProfileInfo của người dùng đang đăng nhập
    user_profile = UserProfileInfo.objects.get(user=request.user)
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()
    
    if request.method == 'POST':
        action = request.POST.get('action') # Lấy giá trị của trường hidden action
        if action == 'avt':
        # avt
            form = UserProfileInfoForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('setting')
        # pass
        elif action == 'pass':

            password = request.POST['password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if user_profile.user.check_password(password) and new_password == confirm_password:
                user_profile.user.set_password(new_password)
                user_profile.user.save()
                return redirect('logout')
            else:
                error_message = 'Invalid password or new password does not match confirmation'
        # email
        elif action == 'email':
            email = request.POST['email']

            if email: # ensure email field is not empty
                user_profile.user.email =email
                user_profile.user.save()
                return redirect('setting')
            else:
                error_message = 'Invalid email'
        elif action == 'bio':
            bio = request.POST['bio']
            nickname = request.POST['nickname']

            if bio: # ensure email field is not empty
                user_profile.bio =bio
                user_profile.nickname =nickname
                user_profile.save()
                return redirect('setting')
            else:
                error_message = 'Invalid bio'
    else:
        error_message = ''
        form = UserProfileInfoForm(request.POST, request.FILES, instance=user_profile)

    context = {
                'form': form,
               'groups': groups,
               'user_profile': user_profile,
               'friends':friends,
               'error_message': error_message}
    return render(request, 'setting.html', context)

def delete_stories(request):
    expired_at = timezone.now() - timezone.timedelta(days=1)
    stories_to_delete = Story.objects.filter(created_at__lte=expired_at)
    stories_to_delete.delete()
    return redirect('profileindex')   

def chat_room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

# friend
def friends(request):
    user_profile = request.user.userprofileinfo
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()    
    sent_requests = FriendRequest.objects.filter(sender=request.user, status='pending')
    received_requests = FriendRequest.objects.filter(receiver=request.user, status='pending') #

    users = UserProfileInfo.objects.exclude(user__in=friends.values('user')).exclude(
    user__in=received_requests.values('sender')).exclude(
    user__in=sent_requests.values('receiver')).distinct()

    return render(request, 'friends.html', {'groups':groups,'friends': friends, 'sent_requests': sent_requests, 'received_requests': received_requests, 'users': users, 'user_profile': user_profile})
@login_required
def add_friend(request, friend_id):
    user_profile = request.user.userprofileinfo
    
    if request.method == 'POST':

        friend = get_object_or_404(UserProfileInfo, id=friend_id)
       
        friend_request = FriendRequest.objects.create(sender=request.user, receiver=friend.user, status='pending')
        friend_request.save()

        return redirect('friends')

    return redirect('friends')
def friend_list(request):

    user_profile = UserProfileInfo.objects.get(user=request.user)
    groups = Group.objects.all().order_by('-id')
    current_user = request.user
    user_profile = current_user.userprofileinfo
    friends = user_profile.friends.all()
    friend_requests = FriendRequest.objects.filter(receiver=current_user, status='pending')

    context = {
        'friends': friends,
        'friend_requests': friend_requests,
        'user_profile' : user_profile,
        'groups':groups
    }

    return render(request, 'friend_list.html', context)
def friend_requests(request):
    user_profile = UserProfileInfo.objects.get(user=request.user)
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()

    friend_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    context = {
        'friends': friends,
        'friend_requests': friend_requests,
        'user_profile' : user_profile,
        'groups':groups
    }
    return render(request, 'friend_requests.html', context)
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
    friend_request.status = 'accepted'
    friend_request.save()

    
    receiver_profile = UserProfileInfo.objects.get(user=request.user)
    sender_profile = UserProfileInfo.objects.get(user=friend_request.sender)
    receiver_profile.friends.add(sender_profile)

    
    sender_profile.friends.add(receiver_profile)

    return redirect('friend_list')
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
    friend_request.status = 'rejected'
    friend_request.save()
    return redirect('friend_list')
def delete_friend(request, friend_id):
    friend_to_remove = UserProfileInfo.objects.get(id=friend_id)
    request.user.userprofileinfo.friends.remove(friend_to_remove)
    friend_to_remove.friends.remove(request.user.userprofileinfo)
    
    return redirect('friend_list')
@login_required
def list_follow(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = user.userprofileinfo
    followers = user_profile.user_following.all()
    followings = user_profile.following.all()
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()
    context = {
        'friends': friends,  
        'user_profile' : user_profile,
        'groups':groups,
         'user': user, 'followers': followers, 'followings': followings
    }
    return render(request, 'list_follow.html',context)

def list_followings(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = user.userprofileinfo
    followers = user_profile.user_following.all()
    followings = user_profile.following.all()
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()
    context = {
        'friends': friends,  
        'user_profile' : user_profile,
        'groups':groups,
         'user': user, 'followers': followers, 'followings': followings
    }
    return render(request, 'list_followings.html', context)
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    user_profile = request.user.userprofileinfo if hasattr(request.user, 'userprofileinfo') else None

    if user_profile:
        if hasattr(user_to_follow, 'userprofileinfo'):
            if user_profile.following.filter(id=user_to_follow.userprofileinfo.id).exists():
                return redirect('list_followings', user_id=request.user.id)  # Redirect to user's own list_follow
            else:
                user_profile.following.add(user_to_follow.userprofileinfo)
                return redirect('list_followings', user_id=request.user.id)

    return redirect('list_follow', user_id=request.user.id)
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(UserProfileInfo, user__id=user_id)
    user_profile = request.user.userprofileinfo

    # Remove the user from the following list
    user_profile.following.remove(user_to_unfollow)

    return redirect('list_followings', user_id=request.user.id)
def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    user_profile = request.user.userprofileinfo if hasattr(request.user, 'userprofileinfo') else None

    if user_profile:
        if hasattr(user_to_block, 'userprofileinfo'):
            user_profile.blocked_users.add(user_to_block.userprofileinfo)

    return redirect('list_block',user_id=user_id)
def list_block(request,user_id):
    user_profile = request.user.userprofileinfo
    blocked_users = user_profile.blocked_users.all()
    groups = Group.objects.all().order_by('-id')
    friends = user_profile.friends.all()  
    return render(request, 'list_block.html', {'friends':friends,'groups':groups,'user_profile':user_profile,'blocked_users': blocked_users})
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(User, id=user_id)
    user_profile = request.user.userprofileinfo
    user_profile.blocked_users.remove(user_to_unblock.userprofileinfo)
    return redirect('list_block',user_id=user_id)

def are_block(user1,user2):
    # Kiểm tra xem người dùng có tồn tại trong danh sách không
    filtered_users = user1.blocked_users.filter(user=user2)
    # Nếu danh sách lọc có ít nhất một người dùng, tức là người dùng tồn tại trong danh sách
    if filtered_users.exists():
        return '0'
    else:
        return '1'