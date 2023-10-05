from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class BannedUsers(models.Model) : 
    authorized = models.ForeignKey("site_app.SiteUser",related_name="yetkili" ,verbose_name=("Banlayan"), on_delete=models.CASCADE)
    suspect = models.ForeignKey("site_app.SiteUser", verbose_name=("Banlanan"), on_delete=models.CASCADE)
    reason = models.CharField(("Banlanma sebebi"), max_length=110)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    class Meta : 
        verbose_name = "Banned Users"
        verbose_name_plural = "Banned Users"
    
    
    def __str__(self) -> str:
        return "{} adlı kullanıcı {} tarihinde {} tarafından banlandı".format(self.suspect.username,
                                                                              self.createdAt,
                                                                              self.authorized.username)
    
    
    
class SiteUser(AbstractUser) :
    avatar = models.ImageField(("User Avatar"), upload_to="Uploads", max_length=300,blank=True)
    isBanned = models.BooleanField(("Hesab Banladı mı?"),default=False)
    about = models.CharField(("Hakkimda"), max_length=100,default="Hakkimda")
    followers = models.ManyToManyField("self",verbose_name=("followers"),blank=True)
    banRecord = models.ForeignKey(BannedUsers, verbose_name=("Ban Kaydi"),null=True,blank=True ,on_delete=models.CASCADE)
    
    class Meta : 
        verbose_name = "Users"
        verbose_name_plural = "Users"
    
    
    def isModerator(self) : 
        role = self.groups.filter(name="Moderator").exists()
        return role
    
    def isAdmin(self) : 
        return self.is_superuser
    
    def totalFollowers(self) : 
        return self.followers.count()
    
    def handleAvatar(self) : 
        if self.avatar : 
            return self.avatar.url
        else : 
            return "https://static.vecteezy.com/system/resources/previews/009/734/564/original/default-avatar-profile-icon-of-social-media-user-vector.jpg"
       
    def rank(self) : 
        
        admin = self.isAdmin()
        if admin : 
            return "Admin"
        
        mod = self.isModerator()
        if mod : 
            return "Moderator"
        
        return "User"
    
        
class messageDetail(models.Model) : 
    author = models.ForeignKey(SiteUser, verbose_name=("Mesaj Yazarı"),related_name="message_author",on_delete=models.CASCADE)
    messageContent = models.TextField(("Mesaj İçeriği"))
    views = models.PositiveIntegerField(("Toplam Görüntülenme"),default=0)
    createdAt = models.DateTimeField(("Oluşturma Tarihi"), auto_now=True)
    likes = models.ManyToManyField(SiteUser, verbose_name=("Likes"),related_name="message_post")
    dislikes = models.ManyToManyField(SiteUser, verbose_name=("Dislikes"),related_name="message_post_dislike")
    postViews = models.IntegerField(("View"),default=0,null=True,blank=True)
    
    
    class Meta : 
        verbose_name = "Posts"
        verbose_name_plural = "Posts"
    
    def total_dislikes(self) : 
        return self.dislikes.count()
    
    def total_likes(self) : 
        return self.likes.count()
    
    def __str__(self) : 
        return "yazar : {} ,message id {}".format(self.author,self.id)
    
class Comments(models.Model) : 
    author = models.ForeignKey(SiteUser, verbose_name=("Yorum Yazari"), on_delete=models.CASCADE)
    comment = models.TextField(("Yorum"))
    post = models.ForeignKey(messageDetail,related_name="comments", verbose_name=("Yorum atilan post"), on_delete=models.CASCADE)
    createdAt = models.DateTimeField(("Yorum tarihi"), auto_now=True)
    
    class Meta : 
        verbose_name = "Comments"
        verbose_name_plural = "Comments"
    
    
    def __str__(self) : 
        return "{author} id {gonderiid} a yorum yaptı".format(author=self.author.username,gonderiid=self.post.id)
    
    
    
    
    