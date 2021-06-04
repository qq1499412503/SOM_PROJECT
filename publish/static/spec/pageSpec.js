describe("page", function() {
it("should be able to visible button", function() {
    var element = document.createElement('div');

    element.id = 'testElement';

    page(2, element);
    expect(element.getAttribute('style')).toEqual('visibility: visible;');

});
it("should be able to hidden button", function() {
    var element = document.createElement('div');

    element.id = 'testElement';

    page(0, element);
    expect(element.getAttribute('style')).toEqual('visibility: hidden;');

});
});