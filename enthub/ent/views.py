
from .forms import *
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from validate_email import validate_email
from django.core.mail import send_mail, EmailMessage
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token

from .models import Article, Profile, Images, Comment, Reference
import datetime
import hmac
import hashlib
import json


def article_list(request):
    adverts = []
    post_list = []

    if request.method == 'POST':
        # paystack_sk = "sk_liveffb5db8bf8d3abe7f343a743ae58ac5911c68d11"
        paystack_sk = "sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111"
        json_body = json.loads(request.body)
        computed_hmac = hmac.new(
            bytes(paystack_sk, 'utf-8'),
            str.encode(request.body.decode('utf-8')),
            digestmod=hashlib.sha512
            ).hexdigest()
        if 'HTTP_X_PAYSTACK_SIGNATURE' in request.META:
            if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == computed_hmac:
                res = request.json()
                status = res['data']['status']
                if status == "success":
                    reference = res['data']['reference']
                    user_reference = Reference1(user_reference_number=reference)
                    user_reference.save()
                    all_reference = Reference.objects.all()
                    articles = Article.published.all()
                    for article in articles:
                        if article.reference in all_reference:
                            post_list.append(article)
                        else:
                            continue
                else:
                    pass
            else:
                pass
        else:
            pass

    else:
        all_reference = Reference.objects.all()
        articles = Article.published.all()
        for article in articles:
            if article.reference in all_reference:
                post_list.append(article)
            else:
                continue

    for post in post_list:
        post_created = post.created.date()
        todays_date = datetime.date.today()
        days_left = todays_date - post_created
        if days_left.days >= 8:
            post.delete()
        else:
            adverts.append(post)



    if len(adverts) != 0:
        b = adverts[0]
    else:
        b = 'No ads available'

    if len(adverts) == 7:
        f = adverts[1:6]
        d = list(f) 
        j = adverts[5]
    else:
        f = None
        d = None
        j = None

    if len(adverts) >= 6:
        k = adverts[6:]
        g = list(k)
    else:
        k = None
        g = None



    

    

    query = request.GET.get('q')
    if query:
        posts = Article.published.filter(
        Q(title__icontains=query)|
        Q(author__username=query)|
        Q(category__icontains=query)|
        Q(body1__icontains=query)|
        Q(body2__icontains=query)|
        Q(body3__icontains=query)|
        Q(body4__icontains=query)|
        Q(body5__icontains=query)|
        Q(body6__icontains=query)|
        Q(body__icontains=query)
        )
    
    context = {

        'b': b,
        'd': d,
        'j': j,
        'g': g,
        
    }
    return render(request, 'ent/article_list.html', context)


    #postts = Product.published.all()
    



def article_details(request, id, slug):
    post = get_object_or_404(Article, id=id, slug=slug)
    #post_img = post.img.url
    #print(post_img)
    post.view_count +=1
    post.save()
    postTitle = post.title
    viewCounts = post.view_count
    subject = 'view count from TonyBrainsBlog'
    message = '%s %s ' %(postTitle, viewCounts)
    emailFrom = [settings.EMAIL_HOST_USER]
    emailTo = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    is_favourite = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            subject = 'Comments from TonyBrainsBlog'
            message = '%s %s ' %(post, content)
            emailFrom = [settings.EMAIL_HOST_USER]
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
                subject = 'Comments reply from TonyBrainsBlog'
                message = '%s %s ' %(content, comment_qs,)
                emailFrom = [settings.EMAIL_HOST_USER]
                emailTo = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()

    else:
        comment_form= CommentForm()

    

    context = {
        'post': post,
        'is_liked': is_liked,
        'is_favourite': is_favourite,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
       
    }

    if request.is_ajax():
        html = render_to_string('ent/comments.html', context, request=request)
        return JsonResponse({'form': html})
    

    return render(request, 'ent/article_details.html', context)


def about(request):
    context = {}
    template = 'ent/about.html'
    return render(request,template,context)



def favourite_post(request, id):
    post = get_object_or_404(Article, id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


def like_post(request):
    #post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post = get_object_or_404(Article, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('ent/like_section.html', context, request=request)
        return JsonResponse({'form': html})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.is_active=False
            new_user.save()
            Profile.objects.create(user=new_user)
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string("ent/activate.html", 
                {
                    'user':new_user,
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': generate_token.make_token(new_user)
                }

                )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.send()

            messages.add_message(request, messages.SUCCESS, 'account created successfully')
            return redirect('user_login')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, "ent/register.html", context)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None


        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'account activated successfully')
            return redirect('user_login')
        return render(request, "ent/activate_failed.html", status=401)



# @login_required(login_url="user_login")
# def post_create(request):
#     if request.method == 'POST':
#         form = PostCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.success(request, "Post has been successfully created.")
#             return redirect('ent:article_list')
#     else:
#         form = PostCreateForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'ent/post_create.html', context)




@login_required(login_url="user_login")
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():

            title = request.POST['title']
            duration = request.POST['duration']
            category = request.POST['category']
            amount = request.POST['amount']
            description = request.POST['description']
            

            post = form.save(commit=False)
            post.author = request.user
            post.save()
            article = Article.objects.filter(pk=1)
            reference = str(article[0].reference)
            email = request.user.email

            headers = {
                'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
                'Content-Type': 'application/json',
            }
            
            if duration == 7:
                price = 40000
            elif duration == 14:
                price = 80000
            elif duration == 21:
                price = 120000
            elif duration == 28:
                price = 160000
            elif duration == 31:
                price = 200000
            else:
                price = 14640000
                
            payment = price

            data = {"reference": reference, "amount":payment, "email":email}

            response = requests.post('https//api.paystack.co.transaction/initialize', headers=headers, json=data)
            res = response.json()

            checkout = res['data']['authorization_url']

            return redirect(checkout)
            
    else:
        form = PostCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'ent/post_create.html', context)
        
        


        



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('ent:article_list'))
                else:
                    return HttpResponse("User is not active")
            else:
                return HttpResponse("User is None")
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'ent/login.html', context)








def user_logout(request):
    logout(request)
    return redirect('ent:article_list')