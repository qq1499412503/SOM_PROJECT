from djongo import models

# Create your models here.


class Blog(models.Model):
    column1= models.CharField(max_length=100)
    col = models.TextField()
    data = models.FileField()
    weight =  models.TextField()
    parameter = models.TextField()

    class Meta:
        abstract = True

class Entry(models.Model):
    data_review = models.EmbeddedField(
        model_container=Blog,
    )



