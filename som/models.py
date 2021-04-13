from djongo import models
import datetime
from objectid import ObjectID, create_objectid
# Create your models here.

class dataframe(models.Model):
    _id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    name = models.CharField(max_length = 200)
    time = models.DateField(auto_now =True)
    data = models.FileField()

    class Meta:
        pass

# json field
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

def retrivedata():
    from som import models
    a = models.dataframe.objects.get(name='som_data1')
    a.data.open(mode='rb')
    lines = a.data.readlines()
    lines
    pass


def savedata():
    from som import models
    e = models.dataframe()
    e.name = 'som_data1'
    from django.core.files.base import ContentFile, File
    with open('./manage.py') as f:
        e.data.save('new_name', File(f))
    e.save()
    pass

def load_data():
    from som import models
    a = models.dataframe.objects.get(name='som_data1')
    pass

def load_data_from_upload():
    pass

