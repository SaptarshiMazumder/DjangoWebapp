

from cgitb import html, reset
from dataclasses import fields
from email.mime import image
from ftplib import all_errors
from multiprocessing import reduction
from operator import is_
import os
import re
from telnetlib import GA
from tkinter import Image
from turtle import pos, title
from unittest import result
from urllib.request import Request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.generic import ListView, DetailView
from matplotlib.style import context
from . models import GameProfile, Post, Replies, ImageFiles, Profile
from . forms import EditPostForm, EditVideoPostForm, ImageForm, PostForm, PostImageForm, PostVideoForm, EditImagePostForm, GameProfileForm, MatchmakingForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
# Create your views here.
# Paginator stuff
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .serializers import PostSerializer
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


# def home(request):
#     object_list = Post.objects.all().order_by('-post_datetime')
#     context = {
#         'object_list': object_list
#     }
#     return render(request, 'home.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home(request):
    object_list = Post.objects.all().order_by('-post_datetime')
    image_list = ImageFiles.objects.all()
    context = {
        'object_list': object_list,
        'image_list': image_list,
    }
    return render(request, 'home.html', context)


def home_timeline(request, post_id=None):

    object_list = Post.objects.all().order_by('-post_datetime')
    game_profiles = GameProfile.objects.all()
    try:
        print(request.session['post_in_view'])
    except:
        pass
    # Set up pagination
    # request.session['loaded_posts'] = object_list
    p = Paginator(object_list, 4)
    # p = Paginator(Post.objects.all().order_by('-post_datetime'), 4)
    page = request.GET.get('page')
    objects = p.get_page(page)
    a = 200
    print(objects)
    try:

        last_viewed = request.session['post_in_view']
    except:
        last_viewed = ""
    image_list = ImageFiles.objects.all()
    profiles = Profile.objects.all()
    has_images_to_show = False
    try:
        post = Post.objects.get(id=post_id)
        profile = Post.objects.get(user=post['author'])
        context = {
            'object_list': object_list,
            'image_list': image_list,
            'post': post,
            'post_id': post_id,
            'objects': objects,
            'objects': objects,
            'last_viewed': last_viewed,
            'has_images_to_show': has_images_to_show,
            'profile': profile,
        }
    except:
        context = {
            'object_list': object_list,
            'image_list': image_list,
            'objects': objects,
            'last_viewed': last_viewed,
            'has_images_to_show': has_images_to_show,
            'profiles': profiles,
            'game_profiles': game_profiles,
        }
    return render(request, 'home_timeline.html', context)


@csrf_exempt
def django_image_and_file_upload_ajax(request, pk):
    form1 = PostImageForm()
    form2 = PostVideoForm()
    imageform = ImageForm()

    post_data = return_post_data(request, pk)

    replying_to = []
    # replying_to = Post.objects.get(id=pk)
    replying_to = get_parent_post(pk, replying_to)
    replying_to = replying_to[::-1]

    replies_obj = []
    replies_to_post = []

    replies = Replies.objects.filter(reply_to=pk)

    if replies:
        print("REPLIES", replies)
        for reply in replies:
            reply_post = Post.objects.get(id=reply.post_id)
            replies_obj.append(reply_post)
        replies_to_post = replies_obj[::-1]

    context = {
        'form1': form1,
        'form2': form2,
        'replying_to': replying_to,
        'imageform': imageform,
        'replies_to_post': replies_to_post,
    }
    print('')
    context.update(post_data)
    print(context)

    if request.method == 'POST':

        form1 = PostImageForm(request.POST, request.FILES)
        form2 = PostVideoForm(request.POST, request.FILES)
        id = int(request.POST.get('postid'))
        files = request.FILES.getlist("image")
        files2 = request.FILES.getlist("video")
        print("FILES2 UPLOADED: ", files2)
        if files2:
            print("FILES 2 IS NOT NONE")
            form1 = PostVideoForm(request.POST, request.FILES)
        if form1.is_valid():
            print("FORM1 VALID")

            instance = form1.save(commit=False)

            print("POSTID: ", id)
            print(type(pk))
            print(type(id))
            instance.author = request.user
            instance.reply_to = id
            instance.is_reply = True
            instance.is_parent_a_reply = is_parent_a_reply(id)
            print("is_parent_a_reply: ", instance.is_parent_a_reply)
            if instance.is_parent_a_reply:
                instance.reply_root = id
            if instance.is_parent_a_reply:
                parent_reply_root = get_parent_reply_root(id)
                if parent_reply_root != -1:
                    instance.reply_root = parent_reply_root

                print("reply_root: ", instance.reply_root)

            print("INSTANCE: ", instance)
            if files:
                instance.has_images = True
            else:
                instance.has_images = False

            if files2:
                instance.has_video = True
            else:
                instance.has_video = False

            instance.save()

            for file in files:
                ImageFiles.objects.create(post=instance, image=file)

            for file in files2:
                print("VIDEO FILE: ", file)

            reply_to_post = Post.objects.get(id=pk)

            reply = Replies(reply_to=id, post_id=instance.id,
                            reply_to_post=reply_to_post, reply_root=instance.reply_root)
            reply.save()

            return(update_replies_list(request, pk))
            # return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})

        if form2.is_valid():
            print("FORM2 VALID")
            instance = form2.save(commit=False)
            instance.author = request.user
            instance.reply_to = pk
            instance.is_reply = True
            if request.FILES:
                instance.has_video = True
            instance.save()

            reply = Replies(reply_to=id, post_id=instance.id,
                            reply_to_post=reply_to_post)
            reply.save()
            return(update_replies_list(request, pk))
        else:
            return JsonResponse({'error': True, 'errors': form1.errors})
    else:
        form1 = PostImageForm()
        form2 = PostVideoForm()
        imageform = ImageForm()

    return render(request, 'testt.html', context)


def is_parent_a_reply(id):
    parent = Post.objects.get(id=id)
    if parent:
        return parent.is_reply
    else:
        return False


def get_parent_reply_root(id):
    parent = Post.objects.get(id=id)
    if parent:
        return parent.reply_root
    else:
        return -1


def update_replies_list(request, post_id):
    replies_obj = []
    replies_to_post = []

    replies = Replies.objects.filter(reply_to=post_id)
    if replies:
        print("REPLIES", replies)
        for reply in replies:
            reply_post = Post.objects.get(id=reply.post_id)
            replies_obj.append(reply_post)
        replies_to_post = replies_obj[::-1]
        image_list = ImageFiles.objects.all()

        replyingToAuthor = ""
        replyingToIsReply = False
        replyingTo = Post.objects.get(id=post_id)

        if replyingTo:
            replyingToAuthor = replyingTo.author.username
            replyingToIsReply = replyingTo.is_reply
            print("REPLYINGG TO: ", replyingToAuthor)
            print("REPLYING TO A REPLY?: ", replyingToIsReply)
        context = {
            'replies': replies,
            'replies_obj': replies_obj,
            'replies_to_post': replies_to_post,
            'image_list': image_list,
            'replyingToAuthor': replyingToAuthor,
            'replyingToIsReply': replyingToIsReply,

        }

        html = render_to_string('replies_list.html', context, request=request)
        # print("HTML: ", html)
        return JsonResponse({'replies_list': html, })
    else:
        return JsonResponse({'replies_list': "", })


@csrf_exempt
def fetch_replies_to_reply(request):
    id = int(request.POST.get('postid'))
    return(update_replies_list(request, id))
    # return JsonResponse({'replies_list': "lkkkk", })


def return_post_data(request, post_id):
    post = Post.objects.get(id=post_id)
    image_list = ImageFiles.objects.all()

    replies_obj = []
    replies_to_post = []

    replies = Replies.objects.filter(reply_to=post_id)

    if replies:
        print("REPLIES", replies)
        for reply in replies:
            if reply.post_id:
                reply_post = Post.objects.get(id=reply.post_id)
                if reply_post:
                    replies_obj.append(reply_post)
        replies_to_post = replies_obj[::-1]
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    total_likes = post.total_likes()
    print("Working till here")
    parents_arr = []
    if post.is_reply:
        parents_arr = get_parent_post(post.reply_to, parents_arr)
        parents_arr = parents_arr[::-1]

    context = {
        'post': post,
        'total_likes': total_likes,
        'liked': liked,
        'replies': replies,
        'replies_obj': replies_obj,
        'replies_to_post': replies_to_post,
        'parents_arr': parents_arr,
        'image_list': image_list,
        'last_viewed': "",

    }

    return context


def add_post(request):
    form = PostForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        print(request.POST)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()

            return redirect('home-page')
        else:
            return render(request, 'add_post.html', context)
    else:
        form = PostForm()

    return render(request, 'add_post.html', context)


def add_image_post(request):
    form = PostImageForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        print(request.POST)
        form = PostImageForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            # form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            if files:
                instance.has_images = True
            else:
                instance.has_images = False
            instance.save()

            for file in files:
                ImageFiles.objects.create(post=instance, image=file)

            return redirect('home-page')
        else:
            print(form.errors)
    else:
        form = PostImageForm()
        imageform = ImageForm()

    return render(request, 'add_image_post.html', {"form": form, "imageform": imageform})


def add_video_post(request):
    form = PostVideoForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        print(request.POST)
        form = PostVideoForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            if request.FILES:
                instance.has_video = True
            instance.save()

            return redirect('home-page')
        else:
            return render(request, 'add_video_post.html', context)
    else:
        form = PostVideoForm()

    return render(request, 'add_video_post.html', context)


def get_parent_post(parent_id, arr):
    parents = Post.objects.get(id=parent_id)
    if parents:
        arr.append(parents)
    if parents.is_reply:
        is_reply_to = Post.objects.get(id=parents.reply_to)
        get_parent_post(is_reply_to.id, arr)
    return arr


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    form = EditPostForm(request.POST or None, instance=post)
    context = {
        'post': post,
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('home-page')
    return render(request, 'update_post.html', context)


def edit_image_post(request, post_id):
    post = Post.objects.get(id=post_id)
    form = EditImagePostForm(request.POST or None, instance=post)
    imageform = ImageForm()
    files = request.FILES.getlist("image")

    context = {
        'post': post,
        'form': form,
        'imageform': imageform
    }

    if form.is_valid():
        form.save()
        instance = form.save(commit=False)
        if files:
            instance.has_images = True
        else:
            instance.has_images = False
        instance.save()
        ImageFiles.objects.filter(post=instance).delete()
        for file in files:
            ImageFiles.objects.create(post=instance, image=file)

        return redirect('home-page')

    return render(request, 'update_image_post.html', context)


def edit_video_post(request, post_id):
    post = Post.objects.get(id=post_id)
    form = EditVideoPostForm(request.POST or None,
                             request.FILES or None, instance=post)
    context = {
        'post': post,
        'form': form
    }

    if form.is_valid():
        # form.save()
        instance = form.save(commit=False)
        if not request.FILES:
            instance.has_video = False

        instance.save()
        return redirect('home-page')
    return render(request, 'update_video_post.html', context)


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    is_reply = False
    if post.is_reply:
        is_reply = True
        print("IS REPLY:", is_reply)
    post.delete()

    if is_reply:
        reply_object = Replies.objects.get(post_id=post_id)
        print("TO BE DELETED:", reply_object)
        reply_object.delete()

    return redirect('home-page')


@login_required
@csrf_exempt
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        print(id)
        print(post.like_count)
        test = post.likes.filter(id=request.user.id)
        print(test)
        # print(request.POST.get('elem'))
        # request.session['post_in_view'] = id
        if post.likes.filter(id=request.user.id).exists():
            print("Exists")
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            print("Doesn't exist")
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        return JsonResponse({'result': result, })


@login_required
@csrf_exempt
def set_likes(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        # print(id)
        # print(post.body, post.like_count)
        result = post.like_count
        # print(request.POST.get('elem'))

        return JsonResponse({'result': result, })


@login_required
@csrf_exempt
def update_session(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        request.session['post_in_view'] = id
        return JsonResponse({'id': request.session['post_in_view']})


@login_required
@csrf_exempt
def get_session_data(request):

    if request.POST.get('action') == 'post':
        id = request.session['post_in_view']
        post = get_object_or_404(Post, id=id)
        result = post.like_count
        print("Last post clicked on: ", request.session['post_in_view'])
        return JsonResponse({'result': result})


def category(request, cat):
    catrgory_posts = Post.objects.filter(tags=cat)
    context = {
        'cat': cat.title().replace('-', ' '),
        'catrgory_posts': catrgory_posts
    }
    return render(request, 'posts_by_category.html', context)

# REST API Views


def home_view(request):
    return render(request, "api/home_view.html", status=200)


def post_list_view(request):
    object_list = Post.objects.all().order_by('-post_datetime')
    image_list = ImageFiles.objects.all()
    post_list = [{"id": x.id, "author": x.author.username, "body": x.body}
                 for x in object_list]
    data = {
        "response": post_list
    }
    return JsonResponse(data)
    return render(request, 'home.html', context)


@api_view(['GET'])
def getPosts(request):
    object_list = Post.objects.all().order_by('-post_datetime')
    serializer = PostSerializer(object_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPost(request, pk):
    object = Post.objects.get(id=pk)
    serializer = PostSerializer(object, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updatePost(request, pk):
    print("Hello")
    data = request.data
    object = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=object, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Post was deleted!')


def posts_by_user(request, user):
    user = User.objects.get(username=user)
    posts = Post.objects.filter(author=user)
    context = {'posts': posts}
    return render(request, 'posts_by_user.html', context)


def create_game_profile(request, user):
    form = GameProfileForm()

    if(user != 'favicon.png'):
        user = User.objects.get(username=user)
        print(user.username)
        if(GameProfile.objects.filter(user=user.id)):
            print("Profile already exists")
            return render(request, 'create_gamer_profile.html', context={'form': form})
        elif(request.method == 'POST'):
            form = GameProfileForm(request.POST)
            if(form.is_valid):
                print(request.POST)
                new_profile = GameProfile(user=user, game=request.POST['game'],
                                          server=request.POST['server'], rank=request.POST['rank'])
                new_profile.save()
                context = {'form': form, 'profile': new_profile}
                return render(request, 'create_gamer_profile.html', context)

    return render(request, 'create_gamer_profile.html', context={'form': form})


def MatchmakingHome(request, user):
    form = GameProfileForm()
    print(user)
    context = {'form': form}

    if request.method == 'POST':
        pref_game = request.POST['game']
        pref_server = request.POST['server']
        rank = request.POST['rank']
        user_profiles = []
        game_profiles = GameProfile.objects.filter(game=pref_game)
        for g in game_profiles:
            this_user = User.objects.get(username=g.user).id
            user_profiles.append(Profile.objects.filter(user=int(this_user)))
        context = {'form': form,
                   'game_profiles': (game_profiles,  user_profiles)}
    return render(request, 'matchmaking.html', context)
