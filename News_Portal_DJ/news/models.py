from django.db import models
from django.contrib.auth.models import User
from .resources import *

class Author(models.Model):
    id_users = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_users = models.IntegerField(default = 0)
    def update_rating(self):
        self.rating_users = 0
        for posts in Post.objects.all():
            if posts.id_authors == self.id:
                self.rating_users += posts.rating_post * 3
            for comments_to_post in Comment.objects.filter(id_post = posts.id):
                if posts.id_authors == self.id:
                    self.rating_users += comments_to_post.rating_post
        for comment_author in Comment.objects.all():
            if Comment.id_users == self.id:
                self.rating_users += comment_author.raiting_comment
        self.save()

class Category(models.Model):

    name_category = models.CharField(unique=True, max_length = 2, choices = category)

class Post(models.Model):
    id_authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length = 2, choices = type_post)
    time_in = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 255)
    text = models.TextField()
    rating_post = models.IntegerField(default = 0)

    post_category = models.ManyToManyField(Category, through = 'PostCategory')

    @property
    def rating(self):
        return self.rating_post

    @rating.setter
    def rating(self, value):
        self.rating_post = value if value >= 0 and isinstance(value, int) else 0
        self.save()

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

class PostCategory(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    id_users = models.ForeignKey(User, on_delete=models.CASCADE)
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add = True)
    rating_comment = models.IntegerField(default = 0)

    @property
    def rating(self):
        return self.rating_comment

    @rating.setter
    def rating(self, value):
        self.rating_comment = value if value >= 0 and isinstance(value, int) else 0
        self.save()

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


