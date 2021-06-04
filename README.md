---
description: Developer guidance of self organizing map database system
---

# Developer Document

## Getting Start:

### Hardware Requirements

make sure there is CPU virtualization supported, both Windows or Linux server working for docker, suggest greater than 30G storage as a minimum since the database server included in one server, for expanding just separate the database server to a different container then config the connection configuration under Django setting.

### **Step 1: Install docker**

Following Docker doc for initializing docker environment:

{% embed url="https://www.docker.com/get-started" %}

### **Step 2: Prepare Docker File and Project**

Git Clone the Project:

```
$ git clone https://github.com/qq1499412503/SOM.git
```

###  **Step 3: Building Docker Image**

Once Project prepared, starting building the image:

```
sudo docker build -t som:v1 .
```

### **Step 4: Run Docker container**

After Image built, run the following command to start the docker container:

```bash
sudo docker run -d -p 20:22 8080:8080 80:80 som:v1 /usr/sbin/sshd -D
```

{% hint style="info" %}
 Port number issued here, allowed to config custom
{% endhint %}

### **Step 5: Visit Web Page**

Since Docker Server initialized, now you can access the system by the web browser.

## Technology: Self-Organizing Map

### Initialization

_x and y_

x and y defined for row and column of neuron nodes

_weights matrix_

based on defined x and y, the weights matrix initialized by the random value of shape \(x, y, length of data\)

_neighborhood function_

the neighbor function used weights the neighborhood of a position in the map, such as Gaussian distribution

![](.gitbook/assets/gaussian.png)

_decay function_

the decay function used to update the learning rates and sigma based on each iteration

$$
learning rate(t) = learning rate / ( 1 + t / max iterations /2 ) )
$$

_sigma_

the sigma refers to the spread of the neighbor

$$
sigma(t) = sigma / (1 + t/T)
$$

_learning rate_

learning rate used for updating the weights matrix

$$
learning rate(t) = learning rate / (1+t/T)
$$

_activation distance_

the function used for calculating the distance between nodes, such as euclidean

![](.gitbook/assets/euc.png)

### Training

_Winner method_

the first step to finding the winner node based on initialized weights matrix to each data row

![](.gitbook/assets/win.png)

_update sigma and learning rate_

the second step since the decay function allocated, its sigma and learning rate updated by iteration number

_update gaussian matrix_

in the third step, the gaussian matrix updated by winner location, sigma and learning rate

![](.gitbook/assets/gas%20%281%29.png)

_update weights matrix_

the weights matrix updated by input vector, weights vector of neuron i and neighborhood function

$$
weights(t+1) = weights_i(t) + neighbour matrix(input vector(t) - weights_i(t))
$$

_u-matrix_

the u-matrix calculate the distance\(such as euclidean\) of the target neuron node to the nodes around the target nodes under hexagonal topology

### Plotting

since the map data calculated, it should include the weights vector of each node\(following updating steps\), distance to neighbor nodes and label to neuron node\(calculated by winner method\), the color of the map now generating by distance map\(distance between nodes\) which is u-matrix

### Other Action

the other action taken involved the relation plotted after the map dragged.

_updating neighbor matrix_

as the x-axis being an example, since there are relation out of map range, the range for calculating neighbor matrix expand_s_ to 3 times \(range\_x \*3\)

_expands weights matrix_

as the neighbor matrix should be expanded, the weights matrix expands to 3 times\(3x3 to original matrix\) by copy the original matrix with the winner location updated

_update weights matrix_

since the weights matrix expanded, its neighbor matrix of each winner nodes been calculated and updated for new weights matrix\(pick central matrix as new weights matrix for updating\)

## Packages:

#### the packages in the project involved:



| Name | description |
| :---: | :--- |
| pandas | package for matrix calculation |
| djongo | package for django based database |
| MiniSom | package for self organized model |
| django | package for framework |
| djangorestframework | package for API implementation |
| matplotlib | package for graph calculation |
| bokeh | package for graph calculation |
| numpy | package for matrix calculation |
| D3 | package for drawing the map |
| ajax | package for API request |



## Method:

{% api-method method="get" host="" path="/" %}
{% api-method-summary %}
Home Url
{% endapi-method-summary %}

{% api-method-description %}
Locate the pages of the system by default URL, where the user is Login, render project list page, if a user is not Login then render the login page
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
redirect to web page
{% endapi-method-response-example-description %}

```markup
/publish/list/
or
/user/login/
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="" path="/user/login/" %}
{% api-method-summary %}
HTTP: Login
{% endapi-method-summary %}

{% api-method-description %}
Render Login page
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
HTTP Response
{% endapi-method-response-example-description %}

```
/user/login/
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/user/login/" %}
{% api-method-summary %}
HTTP: Login
{% endapi-method-summary %}

{% api-method-description %}
Submit form data for Login
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-form-data-parameters %}
{% api-method-parameter name="email" type="string" required=true %}
Email for login
{% endapi-method-parameter %}

{% api-method-parameter name="password" type="string" required=true %}
User password
{% endapi-method-parameter %}
{% endapi-method-form-data-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
redirect to project list page where success or error message with login page
{% endapi-method-response-example-description %}

```
/publish/list/
or
/user/login/  -- {"code":"164" ,"msg": "username or password incorrect"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="" path="/user/register/" %}
{% api-method-summary %}
HTTP: Register
{% endapi-method-summary %}

{% api-method-description %}
Render register page
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
HTTP Response 
{% endapi-method-response-example-description %}

```
/user/register/
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/user/register/" %}
{% api-method-summary %}
HTTP: Register
{% endapi-method-summary %}

{% api-method-description %}
Submit form data for register
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-form-data-parameters %}
{% api-method-parameter name="username" type="string" required=true %}
User name
{% endapi-method-parameter %}

{% api-method-parameter name="email" type="string" required=true %}
Email
{% endapi-method-parameter %}

{% api-method-parameter name="password" type="string" required=true %}
Password
{% endapi-method-parameter %}
{% endapi-method-form-data-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Redirect to project list or render register page where there is an error
{% endapi-method-response-example-description %}

```
/publish/list/
or
/user/register/  -- 
{"code": "111", "msg": "username existed"}
{"code": "222", "msg": "username error or username existed"}
{"code": "333", "msg": "email existed"}
{"code": "444", "msg": "email error or email existed"}
{"code": "555", "msg": "password error"}
{"code": "200", "msg": "all correct"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="" path="/user/profile/" %}
{% api-method-summary %}
HTTP: User Profile
{% endapi-method-summary %}

{% api-method-description %}
Render profile page
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Render profile page with user profile
{% endapi-method-response-example-description %}

```
/user/profile/ --
{"UID": uid, "username": request.user.username, "mail_address": request.user.email, "phone_number": current_user.phone_number , "DOB":current_user.DOB.strftime('%Y-%m-%d'), "data":data, "page":"0"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/user/profile/" %}
{% api-method-summary %}
HTTP: User Profile
{% endapi-method-summary %}

{% api-method-description %}
View specific project or view pages of the project list
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="did" type="number" required=true %}
project id
{% endapi-method-parameter %}

{% api-method-parameter name="page\_n" type="number" required=true %}
current page number and access next project list
{% endapi-method-parameter %}

{% api-method-parameter name="page\_l" type="number" required=true %}
current page number and access previous project list
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
specific project or next project list
{% endapi-method-response-example-description %}

```
/publish/view -- {'did':data_id, 'name':file_name, 'Author':author, 'Date':time, 'Description':description, 'Publish':publish, 'map':map, 'Data_file':data_name, 'x':x,'y':y }
or
/user/profile/ -- {"UID": uid, "username": request.user.username, "mail_address": request.user.email, "phone_number": current_user.phone_number , "DOB":current_user.DOB.strftime('%Y-%m-%d'), "data": data, "page": str(page + 1), "show_data":"True"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="" path="/user/logout/" %}
{% api-method-summary %}
HTTP: Logout
{% endapi-method-summary %}

{% api-method-description %}
Logout current user
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Redirect to Login page
{% endapi-method-response-example-description %}

```
/user/login/
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/update\_user" %}
{% api-method-summary %}
API: Update User
{% endapi-method-summary %}

{% api-method-description %}
update user profile
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="DOB" type="object" required=true %}
current user date of birth with date object
{% endapi-method-parameter %}

{% api-method-parameter name="user\_id" type="number" required=true %}
current user id
{% endapi-method-parameter %}

{% api-method-parameter name="username" type="string" required=true %}
current user name
{% endapi-method-parameter %}

{% api-method-parameter name="email" type="string" required=true %}
current user email
{% endapi-method-parameter %}

{% api-method-parameter name="phone\_number" type="number" required=true %}
current user phone number
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Response API status
{% endapi-method-response-example-description %}

```
{"code": "200", "msg": "success"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/update\_passwd" %}
{% api-method-summary %}
API: Change Password
{% endapi-method-summary %}

{% api-method-description %}
Change user password
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="user\_id" type="number" required=true %}
current user id
{% endapi-method-parameter %}

{% api-method-parameter name="passwd1" type="string" required=true %}
new password
{% endapi-method-parameter %}

{% api-method-parameter name="passwd2" type="string" required=true %}
confirm new password
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Response status code
{% endapi-method-response-example-description %}

```
{"code": "200", "msg": "password successful changed, please login again"}
{"code": "211", "msg": "password can not be none or different"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="" path="/som/model" %}
{% api-method-summary %}
HTTP: New Project
{% endapi-method-summary %}

{% api-method-description %}
render pages of creating a new object
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
HTTP Response
{% endapi-method-response-example-description %}

```
/som/model  -- {'name': 'file not uploaded', "attribute": "no attribute detected", "size": "empty_size"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/som/model" %}
{% api-method-summary %}
HTTP: Upload File
{% endapi-method-summary %}

{% api-method-description %}
Upload file to the server
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="data" type="object" required=true %}
file to upload
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
HTTP Response
{% endapi-method-response-example-description %}

```
/som/model -- 
{"name": f_name, "attribute": data_info[0], "size": data_info[1], "data_id": str(saved_data._id)
{"upload_msg": "not valid file"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/som/user\_query\_info" %}
{% api-method-summary %}
API: Train Map
{% endapi-method-summary %}

{% api-method-description %}
upload parameter for training the map
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="random\_seed" type="number" required=false %}
random seed
{% endapi-method-parameter %}

{% api-method-parameter name="activation" type="string" required=true %}
distance method ex. 'euclidean', 'cosine', 'manhattan', 'chebyshev'
{% endapi-method-parameter %}

{% api-method-parameter name="topology" type="string" required=true %}
ex. 'rectangular', 'hexagonal'
{% endapi-method-parameter %}

{% api-method-parameter name="iteration" type="integer" required=true %}
number of the iteration loop
{% endapi-method-parameter %}

{% api-method-parameter name="neigubour" type="string" required=true %}
neighbor function, ex. 'gaussian', 'mexican\_hat', 'bubble', 'triangle'
{% endapi-method-parameter %}

{% api-method-parameter name="lr" type="number" required=true %}
learning rate
{% endapi-method-parameter %}

{% api-method-parameter name="x" type="integer" required=true %}
size of x axis
{% endapi-method-parameter %}

{% api-method-parameter name="y" type="integer" required=true %}
size of y axis
{% endapi-method-parameter %}

{% api-method-parameter name="len" type="integer" required=false %}
size of data
{% endapi-method-parameter %}

{% api-method-parameter name="sigmas" type="number" required=true %}
sigma for training som, spread of neighbor function
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
JSON Response for map drawing
{% endapi-method-response-example-description %}

```
map data include {nodes, weights, color_var, label}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/som/save\_map" %}
{% api-method-summary %}
API: Save Map
{% endapi-method-summary %}

{% api-method-description %}
save the current map to database
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="user\_id" type="number" required=false %}
current user id
{% endapi-method-parameter %}

{% api-method-parameter name="data\_id" type="number" required=false %}
current data id
{% endapi-method-parameter %}

{% api-method-parameter name="author" type="string" required=false %}
current author name
{% endapi-method-parameter %}

{% api-method-parameter name="vis\_name" type="string" required=false %}
current project name
{% endapi-method-parameter %}

{% api-method-parameter name="description" type="string" required=false %}
current description
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Response status code
{% endapi-method-response-example-description %}

```
{"code":"200","msg":"successful"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}





{% api-method method="get" host="" path="/publish/list/" %}
{% api-method-summary %}
HTTP: Project List
{% endapi-method-summary %}

{% api-method-description %}
render project list page
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
HTTP Response
{% endapi-method-response-example-description %}

```
{"data":<list of project>,"page":"0"}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="" path="/publish/list/" %}
{% api-method-summary %}
HTTP: Project List
{% endapi-method-summary %}

{% api-method-description %}
render different pages of the project list
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="did" type="number" required=false %}
data id to view
{% endapi-method-parameter %}

{% api-method-parameter name="page\_n" type="string" required=false %}
current page number and required next page
{% endapi-method-parameter %}

{% api-method-parameter name="page\_l" type="string" required=false %}
current page number and required last page
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
HTTP Response to different pages or view the specific project
{% endapi-method-response-example-description %}

```
{"data": data, "page": str(page)}
or
project view -- {'did':data_id, 'name':file_name, 'Author':author, 'Date':time, 'Description':description, 'Publish':publish, 'map':map, 'Data_file':data_name, 'x':x,'y':y }
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}































