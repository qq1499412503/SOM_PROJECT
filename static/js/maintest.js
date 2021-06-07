

        function pre_save(tag){
          tag.style.visibility = 'visible';
        }



        function exit_save(tag){
          tag.style.visibility = 'hidden';
        }




      function save_map(tag,user_id,data_id,vis_name,author,description){

      $.ajax({
      type: "post",
      url: "/som/save_map",
      dataType: "json",
      data: JSON.stringify({user_id: user_id,data_id: data_id,
        vis_name:vis_name,
        author:author,
        description:description
      }),
      complete: function(){
              tag.style.visibility = 'hidden';
          },
      success: function as(raw_data) {
            alert("Saved Successfully");

      },
      error: function() {
            alert("Failure to access, please refresh the page");
            }
      })
      ;
      }






      function save_and_publish(tag,user_id,data_id,vis_name,author,description){

      $.ajax({
      type: "post",
      url: "/som/save_and_publish",
      dataType: "json",
      data: JSON.stringify({user_id: user_id ,data_id:data_id,
        vis_name:vis_name,
        author:author,
        description:description
      }),
      complete: function(){
              tag.style.visibility = 'hidden';
          },
      success: function as(raw_data) {
            alert("Saved Successfully");

      },
      error: function() {
            alert("Failure to access, please refresh the page");
            }
      })
      ;
      }



