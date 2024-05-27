from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author (models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)


    def update_rating(self):
        postRat = self.post_set.aggregate(pRating=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('pRating')

        commentRat = self.authorUser.comment_set.aggregate(cRating=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('cRating')

        self.authorRating = pRat * 3 + cRat
        self.save()


class Category (models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=128)
    postText = models.TextField()
    postRating = models.SmallIntegerField(default=0)


    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return f'{self.postText[0:123]}...'


class PostCategory (models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()