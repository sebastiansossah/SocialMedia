
from hashlib import new
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import profile, post, likePost, followsModel
from django.contrib.auth import authenticate
from itertools import chain
import random

# Create your views here.


@login_required(login_url='signin')
def index(request):

    var_profile = profile.objects.get(user=request.user)
    currently_user = request.user.username
    print(currently_user)
    following_feed = followsModel.objects.filter(follower = currently_user)
    following_list = []
    feedList = []

    #users sugestions
    allUsers = User.objects.all()
    user_following = []
    

    for user in following_feed:
        following_list.append(user)

    for usernames in following_list:
        feedVar = post.objects.filter(user=usernames)
        feedList.append(feedVar)
    
    feedVar = list(chain(*feedList))

    largo = len(feedVar)

    for i in following_feed:
        usuario_lista = User.objects.get(username = i.user)
        user_following.append(usuario_lista)

    currently_profile = User.objects.filter(username= request.user.username)
    
    new_suggestion = [x for x in allUsers if x not in user_following]
    final_suggestion = [x for x in new_suggestion if x not in currently_profile]
    random.shuffle(final_suggestion)

    theIdes = []
    this_final= []

    for x in final_suggestion:
        theIdes.append(x.id)

    for x in theIdes:
        profileList = profile.objects.filter(id_user = x)
        this_final.append(profileList)
    
    print('----------------------')

    print(this_final)

    final_list = list(chain(*this_final))

    lis_long = len(final_list)
    print('----------------------')
    print(lis_long)
      
    return render(request, 'index.html',  {'var_profile': var_profile, 'feed': feedVar, 'allUsers': allUsers, 'currently_user': currently_user, 'largo': largo, 'thisProfile': final_list[:4], 'lis_long': lis_long })

def delete(request, id):
    deleteobject = post.objects.filter(id= id)
    deleteobject.delete()

    return redirect('/')

@login_required(login_url='signin')
def search(request):
    userProfile = profile.objects.get(user=request.user)

    if request.method == 'POST':
        searchuser = request.POST['searchuser']
        username_profile = User.objects.filter(username__icontains = searchuser)

        user_profile=[]
        username_profile_list=[]

        for users in username_profile:
            user_profile.append(users.id)
        
        for ids in user_profile:
            usernameVar = profile.objects.filter(id_user = ids)
            username_profile_list.append(usernameVar)

        username_profile_list = list(chain(*username_profile_list))
        print(user_profile)

    return render(request, 'search.html', {'user_profile': userProfile, 'searchuser': searchuser,  'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def indexfollow(request):

        if request.method == 'POST':
            follower = request.POST['follower']
            user = request.POST['user']

            if followsModel.objects.filter(follower=follower, user=user).first():
                delete_follower = followsModel.objects.get(follower=follower, user=user)
                delete_follower.delete()
                return redirect('/')
            
            else:
                new_follower= followsModel.objects.create(follower=follower, user=user)
                new_follower.save()
                return redirect('/' )



def like(request):
    username = request.user.username
    post_id = request.GET.get('posting')
    print(post_id)

    postVar = post.objects.get(id = post_id)

    like_filter = likePost.objects.filter(post_id=post_id, username = username).first()

    if like_filter == None:
        new_like = likePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        postVar.number_likes = postVar.number_likes + 1
        postVar.save()
        return redirect('/')

    else:
        like_filter.delete()
        postVar.number_likes = postVar.number_likes -1
        postVar.save()
        return redirect('/')

def theProfile(request, pk):
    user_objects = User.objects.get(username=pk)
    user_profile = profile.objects.get(user=user_objects)
    user_post = post.objects.filter(user=pk)
    user_post_lenght = len(user_post)

    follower = request.user.username
    user = pk
    follow_number = len(followsModel.objects.filter(user=pk))
    following_numbe = len(followsModel.objects.filter(follower=pk))

    if followsModel.objects.filter(follower=follower, user=user).first():
        button_text= 'Unfollow'
    else:
        button_text='Follow'
    context = {
        'user_objects': user_objects, 
        'user_profile': user_profile, 
        'user_post': user_post,
        'user_post_lenght': user_post_lenght,
        'button_text': button_text,
        'follow_number': follow_number,
        'following_numbe': following_numbe

    }
    return render (request, 'profile.html', context)

@login_required(login_url='signin')
def follows(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if followsModel.objects.filter(follower=follower, user=user).first():
            delete_follower = followsModel.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        
        else:
            new_follower= followsModel.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='signin')
def upload(request):
    user_profile = profile.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('imagePost')
        caption = request.POST['caption']
        profileImage = user_profile.profileImg

        new_post = post.objects.create(user=user, image=image, caption=caption, profileImage= profileImage)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileImg
            bio =request.POST['bio']
            location = request.POST['location']

            user_profile.profileImg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('myImage') != None:
            image = request.FILES.get('myImage')
            bio =request.POST['bio']
            location = request.POST['location']

            user_profile.profileImg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect("settings")

 
    return render (request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            
            else: 
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username= username)
                new_profile =profile.objects.create(user=user_model, id_user= user_model.id)
                new_profile.save()
                return redirect('settings')


        else: 
            messages.info(request, 'Password Not matching')
            return redirect ('signup')


    else:
        return  render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']

        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('/signin')
    else: 
        return render (request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')