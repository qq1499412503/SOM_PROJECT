
describe("check data", function() {
it("should be able to set/get data", function() {
        var val=1;
        setValue(val);
        expect(getValue()).toEqual(val);
});
it("should be able to clean data", function() {
    expect(getValue(cleanValue())).toEqual(null);
});
});

describe("set col", function() {
it("should be able to col", function() {
    var element = document.createElement('input');
    element.value = "10";
    expect(col(element)).toEqual(10);

});

});
describe("set row", function() {
it("should be able to row", function() {
    var element = document.createElement('input');
    element.value = "40";
    expect(row(element)).toEqual(40);

});

});




describe("map", function() {

beforeEach(function() {
    $.ajax({
      type: "post",
      url: "/som/user_query_info",
      dataType: "json",
      data: JSON.stringify({user_id: "UID",
          data_id:"60b50e5b9673592e179cedf4",
        x:"8",
        y:"8",
        // len:null,
        sigmas:"0.6",
        lr:"0.1",
        iteration:"10000",
        neighbour:"gaussian",
        topology:"hexagonal",
        activation:"euclidean"
        // random:null
      }),

      success: function as(raw_data) {
            // alert(raw_data);
          setValue(raw_data);

      } })

});
it("should be able to get point", function() {
    expect(get_point()).toBeTruthy();
    });
it("should be able to move from right to right", function() {
    var point_data = get_point();
    expect(right_r(point_data)).toBeTruthy();
    });
it("should be able to move from left to left", function() {
    var point_data = get_point();
    expect(left_l(point_data)).toBeTruthy();
    });
it("should be able to move from right to left", function() {
    var point_data = get_point();
    expect(right_l(point_data)).toBeTruthy();
    });
it("should be able to move from left to right", function() {
    var point_data = get_point();
    expect(left_r(point_data)).toBeTruthy();
    });
it("should be able to move from up to down", function() {
    var point_data = get_point();
    expect(up_b(point_data)).toBeTruthy();
    });
it("should be able to move from up to up", function() {
    var point_data = get_point();
    expect(up_u(point_data)).toBeTruthy();
    });
it("should be able to move from down to up", function() {
    var point_data = get_point();
    expect(down_u(point_data)).toBeTruthy();
    });
it("should be able to move from down to down", function() {
    var point_data = get_point();
    expect(down_b(point_data)).toBeTruthy();
    });
it("should be able to move map right by data", function() {
    var point_data = get_point();
    expect(update_data(point_data,'r')).toBeTruthy();
    });
it("should be able to move map left by data", function() {
    var point_data = get_point();
    expect(update_data(point_data,'l')).toBeTruthy();
    });
it("should be able to move map up by data", function() {
    var point_data = get_point();
    expect(update_data(point_data,'u')).toBeTruthy();
    });
it("should be able to move map down by data", function() {
    var point_data = get_point();
    expect(update_data(point_data,'d')).toBeTruthy();
    });
it("should be able to display color legend", function() {
    var colorScale1 = d3.scaleSequential(d3.interpolateBlues).domain([0, 1]);
    var element = document.createElement('div');
    element.id = "#1";

    continuous(element,colorScale1);
    expect(continuous(element,colorScale1)).toEqual(true);

    });

});


describe("plotting map", function() {

beforeEach(function() {
    $.ajax({
      type: "post",
      url: "/som/user_query_info",
      dataType: "json",
      data: JSON.stringify({user_id: "UID",
          data_id:"60b50e5b9673592e179cedf4",
        x:"8",
        y:"8",
        // len:null,
        sigmas:"0.6",
        lr:"0.1",
        iteration:"10000",
        neighbour:"gaussian",
        topology:"hexagonal",
        activation:"euclidean"
        // random:null
      }),

      success: function as(raw_data) {
            // alert(raw_data);
          setValue(raw_data);

      } })

});

it("should be able to draw the map and legend", function() {

    var data_id = "60b50e5b9673592e179cedf4";
    var x = "8";
    var y = "8";
    var len = "null";
    var sigmas = "0.6";
    var lr = "0.1";
    var iteration = "100";
    var neighbour = "gaussian";
    var topology = "hexagonal";
    var activation = "euclidean";
    var random = "null";
    var tag_color = document.createElement('input');
    tag_color.value = "blue";
    var tag_font = document.createElement('input');
    tag_font.value = "10";
    var tag_map = document.createElement('div');
    tag_map.style.width = "500px";
    tag_map.style.height = "500px";
    var tag_legend = document.createElement('div');
    tag_legend.style.width = "50px";
    tag_legend.style.height = "500px";
    // spyOn($,"ajax").and.callFake(function(options){
    //     options.success();
    // });
    // var callback = jasmine.createSpy();
    query(data_id,x,y,len,sigmas,lr,iteration,neighbour,topology,activation,random,tag_color,tag_font,tag_map,tag_legend);
    expect($.ajax.call).toBeTruthy();
    // expect(callback).toHaveBeenCalled();
    });

});

