from djongo import models
import datetime
#from objectid import ObjectID


class dataframe(models.Model):
    _id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    file_name = models.CharField(max_length=200, default=str(datetime.datetime.now()))
    time = models.DateField(auto_now=True)
    data = models.FileField(upload_to='uploads/%Y/%m/%d/')

    class Meta:
        pass

    # def __str__(self):
    #     return self._id

    # def get_absolute_url(self):
    #     return reverse('model-detail-view', args=[str(self.id)])
