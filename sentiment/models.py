from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class fileupload(models.Model):
    filename = models.CharField(max_length=100)
    filetype = models.FileField(upload_to='filefolder')
    upload_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('home')


class overall_rating(models.Model):
    filename = models.CharField(max_length=100)
    process_date = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=0.0)
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()
    rat = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('filehome')

#cursor.execute("create table if not exists '%s' (product_id int, product_name varchar(50), review_date date, category varchar(30), rating float, review_text varchar(250), positive float, negative float, neutral float)"% sfile)

class individual_rating(models.Model):
    filename = models.ForeignKey(overall_rating,on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    review_date = models.DateField()
    review_text = models.TextField()
    process_review = models.TextField()
    rating = models.FloatField(default=0.0)
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()

class individual(models.Model):
    filename = models.CharField(max_length=100)
    review_text = models.TextField()
    process_review = models.TextField()
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()
    rat = models.CharField(max_length=100)