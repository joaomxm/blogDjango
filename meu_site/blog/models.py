from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()\
                                           .filter(status='publicado')



class Post(models.Model):
    STATUS = (
        ('rascunho','Rascunho'), 
        ('publicado','Publicado')
    )

    titulo = models.CharField( max_length=250)
    slug = models.SlugField(max_length=250) #http://site.com/noticias/campeonato-brasileiro-2020/01/02/2020
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    conteudo = models.TextField()
    publicado = models.DateTimeField(default=timezone.now)
    criado = models.DateField(auto_now_add=True)
    alterado = models.DateField( auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='rascunho')

    objects = models.Manager()
    published= PublishedManager()

    # url absoluta
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.slug])

    def get_absolute_url_update(self):
        return reverse('post_edit',args=[self.pk])
    
    def get_absolute_url_delete(self):
        return reverse('post_delete',args=[self.pk])

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo
    
@receiver(post_save, sender=Post)
def insert_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.titulo)
        return instance.save()