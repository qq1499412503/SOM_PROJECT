from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import UserInfo
from som.models import dataframe
from bson.objectid import ObjectId
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/user/login/')
def publish_view(request):
    if request.method == "GET":
        data = dataframe.objects.filter(publish=True).order_by('-time')[:5]
        # for a in data:
            # print(a._id,a.file_name,a.author,a.description)
        content = {"data":data,"page":"0"}
        return render(request, 'publish.html', content)
    if request.method == "POST":
        if 'did' in request.POST:
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
            min_color = current_object.min_color
            max_color = current_object.max_color
            content = {'did':data_id, 'name':file_name, 'Author':author, 'Date':time, 'Description':description, 'Publish':publish, 'map':map, 'Data_file':data_name, 'x':x,'y':y,"min_color":min_color,"max_color":max_color }
            return render(request, 'view.html', content)
        elif 'page_n' in request.POST:
            page = int(request.POST["page_n"])
            data = dataframe.objects.filter(publish=True).order_by('-time')[(1+page)*5:(2+page)*5]
            if len(data)>0:
                content = {"data": data, "page": str(page+1)}
                return render(request, 'publish.html', content)
            else:
                data = dataframe.objects.filter(publish=True).order_by('-time')[page * 5:(1 + page) * 5]
                content = {"data": data, "page": str(page)}
                return render(request, 'publish.html', content)
        elif 'page_l' in request.POST:
            page = int(request.POST["page_l"])
            data = dataframe.objects.filter(publish=True).order_by('-time')[(page-1)*5:page*5]
            if len(data)>0:
                content = {"data": data, "page": str(page-1)}
                return render(request, 'publish.html', content)
            else:
                data = dataframe.objects.filter(publish=True).order_by('-time')[page * 5:(1 + page) * 5]
                content = {"data": data, "page": str(page)}
                return render(request, 'publish.html', content)



# def view_view(request):
#     if request.user.is_authenticated:
#         uid = request.user.id
#         user_ob = User.objects.get(pk=uid)
#         current_user = UserInfo.objects.get(user=user_ob)
#         dataframes = dataframe.objects.get(pk=request.did)
#     if request.method == "GET":
#         content = {"uid":uid,"name":current_user.username, "polt":dataframes.map}
#         return render(request, 'view.html.bak',content)