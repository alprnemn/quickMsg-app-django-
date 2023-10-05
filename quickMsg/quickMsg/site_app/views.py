from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from site_app.models import *
from site_app.form import updateUserDetail,CreateMessage,CreateComment,AvatarForm
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.shortcuts import get_object_or_404


def index(request) : 
    context = {}
    
    message = messageDetail.objects.all().annotate(like_count=models.Count('likes')).order_by('-like_count')
    
    if request.user.is_authenticated: 
            context["IsAuthorized"] = request.user.isAdmin() or request.user.isModerator()
    
    if request.method == "POST" : 
        form = CreateMessage(request.POST)
        gelenmes = request.POST.get("messageContent")
        
        if form.is_valid() : 
            form = form.save(commit=False)
            form.author = request.user 
            form.messageContent = gelenmes
            form.save()
            success_emoji = '✅'
            messages.success(request,"Mesaj Başarıyla oluşturuldu {}".format(success_emoji))
            return redirect("homepage")
        
        else : 
            return redirect("homepage")
    
    else:
        keyword = request.GET.get("keyword")
        
        if keyword :
            messagesFromSearch = messageDetail.objects.filter(messageContent__contains = keyword)
            return render(request,"index.html",{"posts" : messagesFromSearch})
         
        
        context["posts"] = message
        context["createMessage"] = CreateMessage()
        
        if request.user.is_authenticated: 
            context["IsAuthorized"] = request.user.isAdmin() or request.user.isModerator()

        return render(request,"index.html",context)    
        
        
    
def updateMessage(request,messageId) : 
    context = {}
    message = get_object_or_404(messageDetail,id=messageId)
    
    
    if request.method == "POST" : 
        form = CreateMessage(request.POST or None,instance=message)
        
        if form.is_valid() :
            message = form.save(commit=False)
            message.author = request.user
            message.save()  
            success_emoji = '✅'
            messages.success(request,"Mesaj Başarıyla güncellendi {}".format(success_emoji))
            return redirect("homepage")
        else : 
            error_emoji = "❌" 
            messages.success(request,"Mesaj Güncellenemedi {}".format(error_emoji))
            return redirect("homepage")
        
    else : 
        context["message"] = message
        context["updateMessage"] = CreateMessage(instance=message)
            
        
    return render(request,"updateMessage.html",context)
    
    
def likeView(request,messageId) : 
    message = messageDetail.objects.filter(id=messageId).first()
    
    message.likes.add(request.user)
    
    
    return redirect("homepage")

def dislikeView(request,messageId) : 
    message = messageDetail.objects.filter(id=messageId).first()
    message.dislikes.add(request.user)
    return redirect("homepage")

def messageView(request,messageId) : 
    message = messageDetail.objects.filter(id=messageId).first()
    message.postViews = message.postViews + 1
    message.save()
        

def deleteMessage(request,messageId) : 
    
    message = messageDetail.objects.filter(id=messageId).first()
    
    if request.user.is_authenticated : 
        
        if request.user == message.author or request.user.isAdmin() or request.user.isModerator(): 
            message.delete()
            success_emoji = '✅'
            messages.success(request,"Mesaj Başarıyla silindi {}".format(success_emoji))
            return redirect("homepage")
        
        else : 
            error_emoji = "❌" 
            messages.success(request,"Mesaj silinemedi {}".format(error_emoji))
            return redirect("homepage")
        
    else : 
        error_emoji = "❌" 
        messages.success(request,"Yekiniz yok {}".format(error_emoji))
        return redirect("homepage")
        
    
def deleteComment(request,messageId,commentId) : 
    comment = get_object_or_404(Comments,id=commentId)
    
    if request.user == comment.author : 
        comment.delete()
        success_emoji = '✅'
        messages.success(request,"Yorum Başarıyla silindi {}".format(success_emoji))
        return redirect("message-page",messageId)
    else : 
        error_emoji = "❌" 
        messages.success(request,"Yorum silinemedi {}".format(error_emoji))
        return redirect("homepage")
    
        
def messagePage(request,messageId) : 
    
    context = {} 
    message = messageDetail.objects.filter(id=messageId).first() 
    
    if message is None : 
        return redirect("homepage") 
    
    if request.method == "POST" : 
        
        form = CreateComment(request.POST) 
        
        if form.is_valid(): 
            form = form.save(commit=False) 
            form.author = request.user 
            form.post = message 
            form.save() 
            success_emoji = '✅'
            messages.success(request,"Yorum oluşturuldu {}".format(success_emoji))
            return redirect("message-page",messageId)
        else : 
            error_emoji = "❌" 
            messages.success(request,"Yorum oluşmadı {}".format(error_emoji))
            return redirect("homepage")
            
    
    else : 
        message.postViews = message.postViews + 1
        message.save()
        context["messagess"] = message
        context["commentForm"] = CreateComment()
        return render(request,"messagedetail.html",context)
    


def loginPage(request) : 
    hello_emoji = "👋" 
    error_emoji = "❌" 
    if request.method == "POST" : 
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password : 
            
            user = authenticate(request,
                                username = username,
                                password = password)
            
            if user : 
                if user.isBanned == True : 
                    messages.error(request,"Bu hesap banlandı {}".format(error_emoji))
                    return redirect("login-page")
                login(request,user)
                messages.success(request,"Welcome, {kullanici} {emoji}".format(kullanici=request.user.first_name,emoji=hello_emoji))
                return redirect("homepage")
            else : 
                messages.error(request,"Username ya da Password hatalı {}".format(error_emoji))
                return redirect("login-page")
             
    return render(request,"login.html")
                


def logoutpage(request) : 
    logout(request)
    return redirect("homepage")


def signup(request): 
    context = {}
    success_emoji = '✅'
    error_emoji = "❌"
    if request.method == "POST" : 
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        email = request.POST.get("email")
        
        
        if len(firstname) < 15 and len(firstname) >= 3:
            if len(lastname) < 15 and len(lastname) >= 3:
                if len(username) < 15 and len(username) >= 3:
                    if password == confirmpassword :
                       
                        try:
                            user = SiteUser.objects.get(email=email)
                            messages.error(request, "Bu E-Mail kullanılıyor {}".format(error_emoji))
                            return redirect("signup-page")
                        except SiteUser.DoesNotExist:
                            pass

                        try:
                            user = SiteUser.objects.get(username=username)
                            messages.error(request, "Bu Username kullanılıyor {}".format(error_emoji))
                            return redirect("signup-page")
                        except SiteUser.DoesNotExist:
                            pass

                        SiteUser.objects.create_user(first_name = firstname,
                                     last_name = lastname,
                                     username = username,
                                     email = email,
                                     password = password,
                                     )
                        
                        messages.success(request,"Başarıyla Kayıt Oldunuz {}".format(success_emoji))
                        return redirect("login-page")
                    else : 
                        messages.error(request,"Parolalar ayni olmalidir {}".format(error_emoji))
                        return redirect("signup-page")
                else : 
                    messages.error(request, "Username en az 3 en fazla 15 karakter olmalidir {}".format(error_emoji))
                    return redirect("signup-page")
            else : 
                messages.error(request,  "Lastname en az 3 en fazla 15 karakter olmalidir {}".format(error_emoji))
                return redirect("signup-page")
        else : 
            messages.error(request,"Firstname en az 3 en fazla 15 karakter olmalidir {}".format(error_emoji))
            return redirect("signup-page")
            
    else : 
        return render(request,"signup.html",context)                                      
    

def profilePage(request,userId) : 
    context = {}
    
    user = SiteUser.objects.filter(id=userId).first()
    users = SiteUser.objects.filter(id=userId).first()
    
    if user : 
        context["user"] = user
        context["banCount"] = BannedUsers.objects.filter(suspect__id = user.id).count()
        context["isBanned"] = user.isBanned == True
    else :
        return redirect("homepage")        
            
    if request.method == "POST" : 
        form = updateUserDetail(request.POST,instance=user)
        
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmpassword")
 
        if form.is_valid(): 
            if  (new_password and confirm_password) and (new_password == confirm_password) :
                user.set_password(new_password)
                form.save()
                user.save()
                success_emoji = '✅'
                messages.success(request,"Bilgiler başarıyla güncellendi {}".format(success_emoji))
                return redirect("profile-page",user.id)
            else : 
                error_emoji = "❌"
                messages.success(request,"Alanları doldurunuz veya bilgileri kontrol ediniz {}".format(error_emoji))
                return redirect("profile-page",user.id)
            
        else : 
            print("formhatası",form.errors)
            error_emoji = "❌"
            messages.success(request,"Alanları doldurunuz {}".format(error_emoji))            
            return redirect("profile-page",user.id)
   
    else : 
        if request.user.is_authenticated: 
            context["IsAuthorized"] = request.user.isAdmin() or request.user.isModerator()
            
        context["users"] = users
        context["form"] = updateUserDetail(instance=user)
        return render(request,"profile.html",context)
    
def followUser(request,userId) : 
    user = SiteUser.objects.filter(id=userId).first()
    logged_in_user = SiteUser.objects.filter(id=request.user.id).first()
    
    if user :         
        user.followers.add(logged_in_user)
        user.save()  
        success_emoji = '✅'
        messages.success(request,"{} adlı kullancııyı takip ettin {}".format(user,success_emoji))
        return redirect("profile-page",userId)
        
    else :
        return redirect("homepage")
            
        
        
def unfollowUser(request,userId) : 
    user = SiteUser.objects.filter(id=userId).first()
    logged_in_user = SiteUser.objects.filter(id=request.user.id).first()
        
    if user :
        user.followers.remove(logged_in_user)
        user.save()
        error_emoji = "❌"
        messages.success(request,"{} adlı kullancııyı takipten çıktın {}".format(user,error_emoji)) 
        return redirect("profile-page",userId)
    else : 
        return redirect("profile-page")
    

def deleteAccount(request,userId) : 
    
    user = SiteUser.objects.filter(id = int(userId)).first()
    
    if user : 
        user.is_active = False
        user.save()
        return redirect("homepage")
        
    else : 
        return redirect("profile-page",userId)
    

def changeAvatar(request, userId):
    user = SiteUser.objects.filter(id=userId).first()

    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data['avatar']
            user.avatar = avatar
            user.save()
            success_emoji = '✅'
            messages.success(request, "Profil resmi güncellendi {}".format(success_emoji))
            return redirect("profile-page", userId)
    else:
        form = AvatarForm()

    return render(request, 'profile.html', {'formavatar': form})

    
    
    
    
    
        
    

def promoteToModerator(request) :
    
    user = SiteUser.objects.filter(id=request.user.id).first()
    modRole,id = Group.objects.get_or_create(name="Moderator")
    
    if user : 
        user.groups.add(modRole)
        
    return redirect("homepage")


def banUser(request,userId): 
    context = {}
    
    user = SiteUser.objects.filter(id=userId).first()
    
    if user is None : 
        return redirect("homepage")
    
    if request.method == "POST" : 
        reason = request.POST.get("reason")
        BannedUsers.objects.create(authorized=request.user,
                                   suspect = user,
                                   reason = reason)
        user.isBanned = True
        user.save()
        success_emoji = '✅'
        messages.success(request,"Kullanıcı Banlandı {}".format(success_emoji))
        return redirect("homepage")
           
    else : 
        context["user"] = user
        
    return render(request,"banuser.html",context)

def unbanUser(request,userId) : 
     
    
    user = SiteUser.objects.filter(id = userId).first()
    
    if user : 
        user.isBanned = False
        user.save()
        success_emoji = '✅'
        messages.success(request,"Kullanıcı Banı Kaldırıldı {}".format(success_emoji))
        return redirect("homepage")
    else : 
        error_emoji = "❌"
        messages.success(request,"Bişeyler ters gitti OOPS {}".format(error_emoji))   
        return redirect("homepage")
        
   




    
    
     
    