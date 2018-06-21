from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter()
		
class Post(models.Model):
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
 
	title = models.CharField(max_length=250)
 
	slug = models.SlugField(max_length=250)
 
	author = models.ForeignKey(User,on_delete=models.CASCADE)
 
	body = models.TextField()
 
	publish = models.DateTimeField(default=timezone.now)
	
	created = models.DateTimeField(auto_now_add=True)
	
	updated = models.DateTimeField(auto_now=True)
	
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
	
	objects = models.Manager() # The default manager.
	
	published = PublishedManager() # Our custom manager.
	
	tags = TaggableManager()
	
	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])	
		
	class Meta:
		ordering = ('-publish',)
		
	def __str__(self):
		return self.title
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

		
class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE,)
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	class Meta:
		ordering = ('created',)
	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)		
