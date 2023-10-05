from django import forms
from .models import SiteUser,messageDetail,Comments


class updateUserDetail(forms.ModelForm) :     
    class Meta : 
        model = SiteUser
        fields = ["about","first_name","last_name","username","email"]
        help_texts = {
            "username" : None
        }
        
class CreateMessage(forms.ModelForm) : 
    class Meta : 
        model = messageDetail
        fields = ["messageContent"]
        
class CreateComment(forms.ModelForm) : 
    class Meta : 
        model = Comments
        fields = ["comment"]
        
class AvatarForm(forms.Form):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}))
        

        

        
        