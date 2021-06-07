describe("update profile", function() {
it("should be able to update profile", function() {
    var element = document.createElement('div');

    element.id = 'testElement';

    var user_id=1;
    var username= "nathan";
    var email = "Som@123.com";
    var phone_number="0426276721";
    var DOB= "2021-05-31";
    var csrfmiddlewaretoken = 'ShJlhm6rMtKaJ1dHHJvTfPKAmo0O8BNC';
    update_user(element,user_id,username,email,phone_number,DOB,csrfmiddlewaretoken);
    expect($.ajax.call).toBeTruthy();
});
});


describe("update password", function() {
it("should be able to update password", function() {
    var element = document.createElement('div');

    element.id = 'testElement';

    var user_id=1;
    var passwd1= "1234";
    var passwd2 = "1234";
    var csrfmiddlewaretoken = 'ShJlhm6rMtKaJ1dHHJvTfPKAmo0O8BNC';
    update_password(user_id,passwd1,passwd2,csrfmiddlewaretoken);
    expect($.ajax.call).toBeTruthy();
});
});


