function update_user(tag,user_id,username,email,phone_number,DOB,csrfmiddlewaretoken){

      $.ajax({
      type: "post",
      url: "/user/update_user",
      dataType: "json",
      data: JSON.stringify({user_id:user_id,
        username:username,
        email:email,
        phone_number:phone_number,
        DOB:DOB,
        csrfmiddlewaretoken: csrfmiddlewaretoken
      }),
      success: function as(raw_data) {
      var dob = tag.value.toString();
      var element = document.createElement('input');

      element.textContent=dob;
      },
      error: function() {
            alert("Failure to access, please refresh the page");
            }
      })
      ;
      }

      function update_password(user_id,passwd1,passwd2,csrfmiddlewaretoken){

      $.ajax({
      type: "post",
      url: "/user/update_passwd",
      dataType: "json",
      data: JSON.stringify({user_id: user_id,
        passwd1:passwd1,
        passwd2:passwd2,
        csrfmiddlewaretoken: csrfmiddlewaretoken
      }),
      success: function as(raw_data) {


      alert(raw_data.msg);
      // window.location.href ="{% url 'user:login' %}";
      },
      error: function() {
            alert("Failure to access, please refresh the page");
            }
      })
      ;
      }



