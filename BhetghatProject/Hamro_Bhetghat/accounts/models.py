from django.db import models
from django.contrib.auth.models import User




INTEREST_CHOICES = [
  ('chai', 'Chai'),
  ('futsal', 'Futsal'),
  ('gaming', 'Gaming'),
  ('study', 'Study'),
  ('movie', 'Movie'),
  ('hiking', 'Hiking'),
]


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  is_free = models.BooleanField(default=False)
  interests = models.CharField(max_length=200, blank=True, default='')
  avatar = models.ImageField(upload_to='avatars/', blank=True)
  bio = models.CharField(max_length=200, blank=True, default='')
  updated_at = models.DateTimeField(auto_now=True)
  
  
  
  def __str__(self):
    return f'{self.user.username}  -  {"Free" if self.is_free else "Busy"}'
  
  @property
  def get_interests_list(self):
    if not self.interests:
      return []
    
    return [i.strip() for i in self.interests.split(',')]
  
  
  
  def set_interests_list(self, interest_list):
    self.interests = ','.join(interest_list)