from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q


class ProfileManager(models.Manager):
    def get_all_profiles_invites(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
        for var in qs:
            if var.status == 'accepted':
                accepted.append(var.receiver)
                accepted.append(var.sender)

        available = [profile for profile in profiles if profile not in accepted]

    def get_all_profile(self,me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User , on_delete=models.CASCADE ,unique=True)
    email = models.EmailField( max_length=200)
    avatar = models.ImageField(default='avatar.png', upload_to='avatar')
    friends = models.ManyToManyField(User, blank=True,related_name='friends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    objects = ProfileManager()

    
# we have friends
    def get_friends(self):
        return self.friends.all()

# how many freinds we have for calculating
    def get_friends_num(self):
        return self.friends.all().count()    


# how many posts calculations
    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):            #class Post --> related_name=posts
        return self.posts.all()    

# this is number of Likes relationship with posts.Model(app)->class Like
    def get_likes_given_num(self):
        likes = self.like_set.all()
        total_like = 0
        for item in likes:                   #class Post --> related_name=likes
            if item.value == 'Like':
                total_like += 1
        return total_like 


    def get_likes_recieved_no(self):
        posts = self.posts.all()               #class Post --> related_name=posts 
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked    


    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def save(self, *args,**kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + '' + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug=slugify(to_slug + '' +str(get_random_code()))
                ex =Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug= to_slug
        super().save(*args,**kwargs)            


STATUS_CHOICES=(
    ('send','send'),
    ('accepted','accepted')
)

class RelationshipManager(models.Manager):
    def invatiotion_recieved(self, receiver):
        query = Relationship.objects.filter(receiver=receiver, status='send')
        return query


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
    status = models.CharField(max_length=15,choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"



