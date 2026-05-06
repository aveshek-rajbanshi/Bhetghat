from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Choose a username',
                                 })
                              )
    
    email = forms.EmailField(
                            required=False,
                            widget=forms.EmailInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'your@email.com (optional)',
                              })
                            )
    
    password1 = forms.CharField(
                                label='Password',
                                widget=forms.PasswordInput(attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Create a password',
                                  })
                                )
    
    password2 = forms.CharField(
                              label='Confirm Password',
                              widget=forms.PasswordInput(attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Repeat your password',
                                  })
                                )
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
          
        return username
      
      
    def clean(self):
      cleaned_data = super().clean()
      
      p1 = cleaned_data.get('password1')
      p2 = cleaned_data.get('password2')
      if p1 and p2 and p1 != p2:
          raise forms.ValidationError('Passwords do not match.')
        
      return cleaned_data
