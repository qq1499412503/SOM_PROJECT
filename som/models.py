from djongo import models
import datetime
from objectid import ObjectID, create_objectid
# Create your models here.


# class Blog(models.Model):
#     column1= models.CharField(max_length=100)
#     col = models.TextField()
#     data = models.FileField()
#     weight =  models.TextField()
#     parameter = models.TextField()
#
#     class Meta:
#         abstract = True
#
# class Entry(models.Model):
#     data_review = models.EmbeddedField(
#         model_container=Blog,
#     )

class dataframe(models.Model):
    _id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    name = models.CharField(max_length = 200)
    time = models.DateField(auto_now =True)
    data = models.FileField()


    class Meta:
        pass

# from django.core.files.base import ContentFile, File
# e = get()
# e.name = 'som_data'
# with open('/path/to/file') as f:
#     e.data.save('new_name', File(f))
#
# e.headline = 'The Django MongoDB connector'
# e.save()
#
# name =

def retrivedata(*):
    pass

def savedata():
    pass

def load_data():
    pass

def load_data_from_upload():
    pass

