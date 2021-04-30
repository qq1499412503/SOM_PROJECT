from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import UserInfo
from som.models import dataframe
from bson.objectid import ObjectId
import json
# Create your views here.


def publish_view(request):
    if request.method == "GET":
        data = dataframe.objects.filter(publish=True).order_by('-time')[:5]
        # for a in data:
            # print(a._id,a.file_name,a.author,a.description)
        content = {"data":data}
        return render(request, 'publish.html', content)
    if request.method == "POST":
        data_id = ObjectId(str(request.POST['did']))
        current_object = dataframe.objects.get(_id=data_id)
        file_name = current_object.file_name
        author = current_object.author
        time = current_object.time
        description = current_object.description
        publish = current_object.publish
        data_name = str(current_object.data).split('/')[-1]
        map = json.dumps(dict(current_object.map))
        x = current_object.x
        y = current_object.y
        content = {'did':data_id, 'name':file_name, 'Author':author, 'Date':time, 'Description':description, 'Publish':publish, 'map':map, 'Data_file':data_name, 'x':x,'y':y }
        return render(request, 'view.html', content)



# def view_view(request):
#     if request.user.is_authenticated:
#         uid = request.user.id
#         user_ob = User.objects.get(pk=uid)
#         current_user = UserInfo.objects.get(user=user_ob)
#         dataframes = dataframe.objects.get(pk=request.did)
#     if request.method == "GET":
#         content = {"uid":uid,"name":current_user.username, "polt":dataframes.map}
#         return render(request, 'view.html',content)