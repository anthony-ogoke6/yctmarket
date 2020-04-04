from __future__ import unicode_literals

from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
#from ckeditor.fields import RichTextField


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Article(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    DURATION_CHOICES = (
        (7,'1 Week'),
        (14,'2 Weeks'),
        (28,'3 Weeks'),
        (31,'1 Month'),
        (366,'1 Year'),

    )

    CATEGORY_CHOICES = (
        ('Agriculture & Food','Agriculture & Food'),
        ('Animals & Pets','Animals & Pets'),
        ('Babies & Kids','Babies & Kids'),
        ('Commercial Equipment & Tool','Commercial Equipment & Tool'),
        ('Electronics','Electronics'),
        ('Fashion','Fashion'),
        ('Health & Beauty','Health & Beauty'),
        ('Home, Furniture & Appliances','Home, Furniture & Appliances'),
        ('Mobile Phones & Tablets','Mobile Phones & Tablets'),
        ('Property','Property'),
        ('Repair & Construction','Repair & Construction'),
        ('Seeking Work - CVs','Seeking Work - CVs'),
        ('Services','Services'),
        ('Sport, Art & Outdoors','Sport, Art & Outdoors'),
        ('Vehicles','Vehicles'),
        
    )

    reference           =       models.UUIDField( editable=False, unique=True, default=uuid.uuid4)
    title               =       models.CharField(max_length=200)
    slug                =       models.SlugField(max_length=200)
    status              =       models.CharField(max_length=10, choices=BLANK_CHOICE_DASH + list(STATUS_CHOICES))
    
    author              =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    amount              =       models.PositiveIntegerField(default=0)
    category            =       models.CharField( max_length=100, choices=BLANK_CHOICE_DASH + list(CATEGORY_CHOICES))
    description         =       models.TextField()
    video               =       models.FileField(blank=True, null=True)
    image               =       models.ImageField(blank=True, null=True)
    bodysnippet         =       models.TextField(default='', blank=True, null=True)
    body                =       RichTextUploadingField(default='', blank=True, null=True)
    link1                =       models.TextField(default='', blank=True, null=True)
    video2               =       models.FileField(blank=True, null=True)
    image2              =       models.ImageField(blank=True, null=True)
    body1               =       RichTextUploadingField(default='', blank=True, null=True)
    link2                =       models.TextField(default='', blank=True, null=True)
    video3               =       models.FileField(blank=True, null=True)
    image3              =       models.ImageField(blank=True, null=True)
    body2               =       RichTextUploadingField(default='', blank=True, null=True)
    link3                =       models.TextField(default='', blank=True, null=True)
    video4               =       models.FileField(blank=True, null=True)
    image4              =       models.ImageField(blank=True, null=True)
    body3               =       RichTextUploadingField(default='', blank=True, null=True)
    link4                =       models.TextField(default='', blank=True, null=True)
    video5               =       models.FileField(blank=True, null=True)
    image5              =       models.ImageField(blank=True, null=True)
    body4               =       RichTextUploadingField(default='', blank=True, null=True)
    link5                =       models.TextField(default='', blank=True, null=True)
    video6               =       models.FileField(blank=True, null=True)
    image6              =       models.ImageField(blank=True, null=True)
    body5               =       RichTextUploadingField(default='', blank=True, null=True)
    link6                =       models.TextField(default='', blank=True, null=True)
    video7               =       models.FileField(blank=True, null=True)
    image7              =       models.ImageField(blank=True, null=True)
    body6               =       RichTextUploadingField(default='', blank=True, null=True)
    link7                =       models.TextField(default='', blank=True, null=True)
    video8               =       models.FileField(blank=True, null=True)
    image8              =       models.ImageField(blank=True, null=True)
    body7               =       RichTextUploadingField(default='', blank=True, null=True)
    link8                =       models.TextField(default='', blank=True, null=True)
    video9               =       models.FileField(blank=True, null=True)
    image9              =       models.ImageField(blank=True, null=True)
    body8               =       RichTextUploadingField(default='', blank=True, null=True)
    link9                =       models.TextField(default='', blank=True, null=True)
    video10               =       models.FileField(blank=True, null=True)
    image10              =       models.ImageField(blank=True, null=True)
    body9               =       RichTextUploadingField(default='', blank=True, null=True)
    link10                =       models.TextField(default='', blank=True, null=True)
    video11               =       models.FileField(blank=True, null=True)
    image11             =       models.ImageField(blank=True, null=True)
    body10               =       RichTextUploadingField(default='', blank=True, null=True)
    link11                =       models.TextField(default='', blank=True, null=True)
    video12               =       models.FileField(blank=True, null=True)
    image12             =       models.ImageField(blank=True, null=True)
    link12                =       models.TextField(default='', blank=True, null=True)
    view_count          =       models.PositiveIntegerField(default=0)
    duration          =       models.PositiveIntegerField(default=10, choices=BLANK_CHOICE_DASH + list(DURATION_CHOICES))
    likes               =       models.ManyToManyField(User, related_name='likes', blank=True)
    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)
    restrict_comment    =       models.BooleanField(default=False)
    favourite           =       models.ManyToManyField(User, related_name='favourite', blank=True)
    #reference           =       models.CharField(max_length=300, unique=True, editable=False, default=uuid.uuid4)
    



    def __str__(self):
        return str(self.post.id)


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def snippet(self):
        return self.bodysnippet[:200] + "..."

    def total_likes(self):
        return self.likes.count()

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.image2.delete()
        self.image3.delete()
        super().delete(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("ent:article_details", args=[self.id, self.slug])


@receiver(pre_save, sender=Article)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug




class AdvertImages(models.Model):
    company_name    =       models.CharField(max_length=200)
    amount          =       models.PositiveIntegerField(default=0)
    duration        =       models.CharField(max_length=10)
    bodysnippet     =       models.TextField(default='', blank=True, null=True)
    body            =       RichTextUploadingField(default='', blank=True, null=True)
    pic             =       models.ImageField(upload_to='images/', blank=True, null=True)
    vid             =       models.FileField(blank=True, null=True)


    def __str__(self):
        return str(self.company_name.id)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.company_name

    def snippet(self):
        return self.bodysnippet[:100] + "..."



class Reference(models.Model):
    user_reference_number      =       models.CharField(max_length=200)



    def __str__(self):
        returnnstr(self.reference)



class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)


    def __str__(self):
        return "Profile of user {}".format(self.user.username)


class Images(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return str(self.post.id)