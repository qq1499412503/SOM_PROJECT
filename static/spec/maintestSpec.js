describe("save menu", function() {
it("should be able to visit menu", function() {
    var element = document.createElement('div');

    element.id = 'testElement';
    pre_save(element);

    expect(element.getAttribute('style')).toEqual('visibility: visible;');

});
it("should be able to hidden menu", function() {
    var element = document.createElement('div');

    element.id = 'testElement';
    exit_save(element);
    expect(element.getAttribute('style')).toEqual('visibility: hidden;');

});
});
//

describe("save ajax", function() {
it("should be able to save", function() {
    var element = document.createElement('div');
    var data_id = '6094c9229673590075699bbb';
    element.id = 'testElement';
    vis_name = document.createElement("input");
    vis_name.id = "vis_name";
    vis_name.value = "vis_test";
    author = document.createElement("input");
    author.id = "author";
    author.value = "author_test";
    description = document.createElement("input");
    description.id = "description";
    description.value = "description_test";
    save_map(element,1,data_id,vis_name,author,description);
    expect($.ajax.call).toBeTruthy();
    // expect(element.getAttribute('style')).toEqual('visibility: visible;');

});
it("should be able to save and publish", function() {
     var element = document.createElement('div');
    var data_id = '6094c9229673590075699bbb';
    element.id = 'testElement';
    vis_name = document.createElement("input");
    vis_name.id = "vis_name";
    vis_name.value = "vis_test";
    author = document.createElement("input");
    author.id = "author";
    author.value = "author_test";
    description = document.createElement("input");
    description.id = "description";
    description.value = "description_test";
    save_and_publish(element,1,data_id,vis_name,author,description);
    expect($.ajax.call).toBeTruthy();
});
});
