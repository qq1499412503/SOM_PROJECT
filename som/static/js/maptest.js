

      var data;
      function setValue(val){
          data=val;
      }
      function getValue(){
          return data;
      }

      function cleanValue(){
          data = null;
      }

function col(tag){
        if (parseInt(tag.value) > 0){
          return parseInt(tag.value);
        }else{
          return 30;
        }

}

function row(tag){
        if (parseInt(tag.value) > 0){
          return parseInt(tag.value);
        }else{
          return 20;
        }

}

var svg = d3.select("#m14").append("svg")
                .attr("width", document.querySelector('#m14').offsetWidth)
                .attr("height", document.querySelector('#m14').offsetHeight),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")"),
    // l = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")"),
    a = d3.select("body").append("div").classed('tooltip', true).style("visibility", "hidden");

    var MapColumns = col(),
        MapRows = row();

    var hexRadius = d3.min([width/((MapColumns + 0.5) * Math.sqrt(3)),
                height/((MapRows + 1/3) * 1.5)]);
    width = MapColumns*hexRadius*Math.sqrt(3);
    height = MapRows*1.5*hexRadius+0.5*hexRadius;
    var hexbin = d3.hexbin()
        .radius(hexRadius)



function get_point(){
    var points = [];
    for (var i = 0; i < MapRows; i++) {
        for (var j = 0; j < MapColumns; j++) {
            var x = hexRadius * j * Math.sqrt(3)
            if(i%2 === 1) x += (hexRadius * Math.sqrt(3))/2
            if((i-2)%4===0) x += (hexRadius * Math.sqrt(3))
            var y = hexRadius * i * 1.5
            var color =  getValue()['nodes'][i][j]
            var weights = getValue()['weights'][i][j]
            var label = getValue()['label'][i][j]
            var color_value = getValue()['color_value'][i][j]
            // points.push([x,y,color])
          points.push({"x": x,"y": y,"color": color,"weights":weights,"label":label,"cv":color_value})
        }
    }
    return points;
}


    var _zoom = d3.zoom()
      .scaleExtent([.5, 20])
      .extent([[0, 0], [width, height]])
      .on("zoom", updateChart);

function getTranslation(transform) {
  var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  g.setAttributeNS(null, "transform", transform);
  var matrix = g.transform.baseVal.consolidate().matrix;
  return [matrix.e, matrix.f];
}


    var _drag = d3.drag()
      .on("drag",moveMap);


    g.append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);




function right_r(d){
  // var d = get_point();
  var dm = Math.max.apply(Math, d.map(function(d) { return d.x; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].x !== dm){
      target.push(d[i]);
      // alert(d[i].x);
    }
  }

  return target

}
function left_l(d){
  // var d = get_point();
  var dm = Math.min.apply(Math, d.map(function(d) { return d.x; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].x !== dm){
      target.push(d[i]);
      // alert(d[i].x);
    }
  }

  return target

}
function right_l(d){
  // var d = get_point();
  var dm = Math.max.apply(Math, d.map(function(d) { return d.x; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].x === dm){
      target.push({"x": d[i].x-hexRadius * MapColumns * Math.sqrt(3),"y": d[i].y,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }
  }

  return target

}
function left_r(d){
  // var d = get_point();
  var dm = Math.min.apply(Math, d.map(function(d) { return d.x; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].x === dm){
      target.push({"x": d[i].x+hexRadius * MapColumns * Math.sqrt(3),"y": d[i].y,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }
  }

  return target

}

function up_b(d){
  // var d = get_point();
  var dm = Math.min.apply(Math, d.map(function(d) { return d.y; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].y === dm){
      target.push({"x": d[i].x,"y": d[i].y+hexRadius * MapRows * 1.5,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }
  }

  return target

}

function up_u(d){
  // var d = get_point();
  var dm = Math.min.apply(Math, d.map(function(d) { return d.y; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].y !== dm){
      target.push(d[i]);
      // alert(d[i].x);
    }
  }

  return target

}

function down_u(d){
  // var d = get_point();
  var dm = Math.max.apply(Math, d.map(function(d) { return d.y; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].y === dm){
      target.push({"x": d[i].x,"y": d[i].y-hexRadius * MapRows * 1.5,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }
  }

  return target

}

function down_b(d){
  // var d = get_point();
  var dm = Math.max.apply(Math, d.map(function(d) { return d.y; }));
  var target = [];
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].y !== dm){
      target.push(d[i]);
      // alert(d[i].x);
    }
  }

  return target

}

function update_data(d,ar){
  var target = [];
  if(ar === 'r'){
  var dm = Math.max.apply(Math, d.map(function(d) { return d.x; }));
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].x === dm){
      target.push({"x": d[i].x-hexRadius * MapColumns * Math.sqrt(3),"y": d[i].y,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }else{
      target.push(d[i]);
    }
  }
  }
  else if(ar === 'l'){
  var dm = Math.min.apply(Math, d.map(function(d) { return d.x; }));
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].x === dm){
      target.push({"x": d[i].x+hexRadius * MapColumns * Math.sqrt(3),"y": d[i].y,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }else{
      target.push(d[i]);
    }
  }
  }
    else if(ar === 'u'){
  var dm = Math.min.apply(Math, d.map(function(d) { return d.y; }));
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].y === dm){
      target.push({"x": d[i].x,"y": d[i].y+hexRadius * MapRows * 1.5,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }else{
      target.push(d[i]);
    }
  }
  }
        else if(ar === 'd'){
  var dm = Math.max.apply(Math, d.map(function(d) { return d.y; }));
  for (var i = 0; i < d.length; i++){
    // alert(i);
    if (d[i].y === dm){
      target.push({"x": d[i].x,"y": d[i].y-hexRadius * MapRows * 1.5,"color": d[i].color,"weights":d[i].weights,"label":d[i].label,"cv":d[i].cv});
      // alert(d[i].x);
    }else{
      target.push(d[i]);
    }
  }
  }
  return target
}

var init_dt;




var initx = 34.78;
var w;
var h;
var inity = 31.03;
// var dx =0;
// var lw =1;
function moveMap(d){
  var translate = getTranslation(d3.select(this).attr("transform"));
      x = d3.event.dx+translate[0];
      y = d3.event.dy+translate[1];

      // x = Math.max(Math.min(-w*lw),Math.min(-w*lw),d3.event.dx+translate[0]);
      // x = Math.min(Math.max(w),Math.max(w),x);
      // y = Math.max(Math.min(-h),Math.min(-h),y);
      // y = Math.min(Math.max(h),Math.max(h),y);
      // dx += d3.event.dx

      g.selectAll("path")
      .attr("transform", "translate(" + x + "," + y + ")");
      g.selectAll("text")
      .attr("transform", "translate(" + x + "," + y + ")");
// console.log(dx);
      // ssss
  // while (x-initx>w) {
while (x-initx>=w) {
  console.log(x);
// lw += 1;
//   dx=0;
    initx = x;
    g.selectAll("path").data(right_r(init_dt)).attr("d", function (d) {
      return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
    }).attr("stroke", function (d, i) {
      return "#e5b367";
    })
            .attr("stroke-width", "1px")
            .attr("fill", function (d) {
              return d.color;
            })

            .exit()
            .remove();
    ///

        g.select("g")      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)").selectAll(".hexagon")
                .data(right_l(init_dt))
      .enter().append("path")
      .attr("d", function (d) {
		return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
	})
         .attr("stroke", function (d,i) {
		return "#e5b367";
	})
      .attr("stroke-width", "1px")
      .attr("fill", function(d){ return d.color; })
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
      .call(_drag);
        // .on('mouseover', mouseOver)
        // .on('mouseout', mouseOut)
        // .on('mousemove', mouseMove);
              g.selectAll("text").data(right_r(init_dt))
                            .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central").exit().remove();
          g.append("g")
      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)")
      .selectAll("labels")
      .data(right_l(init_dt))
      .enter()
      .append("text")
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central")
        .style("font-size", 10)
        .style("fill", "black");
  init_dt = update_data(init_dt,'r');

  }
  while (x-initx<-w) {
    initx = x;
    g.selectAll("path").data(left_l(init_dt)).attr("d", function (d) {
      return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
    }).attr("stroke", function (d, i) {
      return "#e5b367";
    })
            .attr("stroke-width", "1px")
            .attr("fill", function (d) {
              return d.color;
            })

            .exit()
            .remove();
    ///

        g.select("g")      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)").selectAll(".hexagon")
                .data(left_r(init_dt))
      .enter().append("path")
      .attr("d", function (d) {
		return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
	})
         .attr("stroke", function (d,i) {
		return "#e5b367";
	})
      .attr("stroke-width", "1px")
      .attr("fill", function(d){ return d.color; })
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
      .call(_drag);
        // .on('mouseover', mouseOver)
        // .on('mouseout', mouseOut)
        // .on('mousemove', mouseMove);

              g.selectAll("text").data(left_l(init_dt))
                            .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central").exit().remove();
          g.append("g")
      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)")
      .selectAll("labels")
      .data(left_r(init_dt))
      .enter()
      .append("text")
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central")
        .style("font-size", 10)
        .style("fill", "black");
  init_dt = update_data(init_dt,'l');

  }
   while (y-inity>h) {
    inity = y;
    g.selectAll("path").data(down_b(init_dt)).attr("d", function (d) {
      return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
    }).attr("stroke", function (d, i) {
      return "#e5b367";
    })
            .attr("stroke-width", "1px")
            .attr("fill", function (d) {
              return d.color;
            })

            .exit()
            .remove();
    ///

        g.select("g")      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)").selectAll(".hexagon")
                .data(down_u(init_dt))
      .enter().append("path")
      .attr("d", function (d) {
		return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
	})
         .attr("stroke", function (d,i) {
		return "#e5b367";
	})
      .attr("stroke-width", "1px")
      .attr("fill", function(d){ return d.color; })
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
      .call(_drag);
        // .on('mouseover', mouseOver)
        // .on('mouseout', mouseOut)
        // .on('mousemove', mouseMove);
              g.selectAll("text").data(down_b(init_dt))
                            .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central").exit().remove();
          g.append("g")
      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)")
      .selectAll("labels")
      .data(down_u(init_dt))
      .enter()
      .append("text")
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central")
        .style("font-size", 10)
        .style("fill", "black");
  init_dt = update_data(init_dt,'d');

  }
      while (y-inity<-h) {
    inity = y;
    g.selectAll("path").data(up_u(init_dt)).attr("d", function (d) {
      return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
    }).attr("stroke", function (d, i) {
      return "#e5b367";
    })
            .attr("stroke-width", "1px")
            .attr("fill", function (d) {
              return d.color;
            })

            .exit()
            .remove();
    ///

        g.select("g")      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)").selectAll(".hexagon")
                .data(up_b(init_dt))
      .enter().append("path")
      .attr("d", function (d) {
		return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
	})
         .attr("stroke", function (d,i) {
		return "#e5b367";
	})
      .attr("stroke-width", "1px")
      .attr("fill", function(d){ return d.color; })
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
      .call(_drag);
        // .on('mouseover', mouseOver)
        // .on('mouseout', mouseOut)
        // .on('mousemove', mouseMove);
              g.selectAll("text").data(up_u(init_dt))
                            .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central").exit().remove();
          g.append("g")
      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)")
      .selectAll("labels")
      .data(up_b(init_dt))
      .enter()
      .append("text")
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central")
        .style("font-size", 10)
        .style("fill", "black");
  init_dt = update_data(init_dt,'u');

  }
}



    function updateChart() {
      // var newX = d3.event.transform.rescaleX(x);
      // var newY = d3.event.transform.rescaleY(y);
      // // var currentZoomScale = d3.event.transform.k;
      // xAxis.call(d3.axisBottom(newX));
      // yAxis.call(d3.axisLeft(newY));
      g.selectAll("path")
      .on('dblclick.zoom', false)
      .attr("d", function (d) {
		return "M" + d.x + "," + (height-d.y) + hexbin.radius(hexRadius).hexagon();
	});
    }

    function mouseOver(d, i) {
    d3.select(this).classed('over', true);
    d3.select("#u62_text").text(d.weights );
    // ' (' + parseInt(d.x) + ',' + parseInt(d.y) + ')'
    // a.style("visibility", "visible");

}
function mouseMove(d, i) {
    a.style('top', (d3.event.pageY - 10) + 'px').style('left', (d3.event.pageX + 10) + 'px');
}
function mouseOut(d, i) {
    d3.select(this).classed('over', false);
    a.style("visibility", "hidden");
}

function continuous(selector_id, colorscale) {
  d3.select('canvas').remove();
  d3.select(selector_id).select('svg').remove();
  var legendheight = 588,
      legendwidth = 50,
      margin = {top: 10, right: 25, bottom: 10, left: 2};

  var canvas = d3.select(selector_id)
    .style("height", legendheight + "px")
    .style("width", legendwidth + "px")
    .append("canvas")
    .attr("height", legendheight - margin.top - margin.bottom)
    .attr("width", 1)
    .style("height", (legendheight - margin.top - margin.bottom) + "px")
    .style("width", (legendwidth - margin.left - margin.right) + "px")
    .style("border", "1px solid #000")
    .style("position", "absolute")
    .style("top", (margin.top) + "px")
    .style("left", (margin.left) + "px")
    .node();

  var ctx = canvas.getContext("2d");

  var legendscale = d3.scaleLinear()
    .range([1, legendheight - margin.top - margin.bottom])
    .domain(colorscale.domain());

  // image data hackery based on http://bl.ocks.org/mbostock/048d21cf747371b11884f75ad896e5a5
  var image = ctx.createImageData(1, legendheight);
  d3.range(legendheight).forEach(function(i) {
    var c = d3.rgb(colorscale(legendscale.invert(i)));
    image.data[4*i] = c.r;
    image.data[4*i + 1] = c.g;
    image.data[4*i + 2] = c.b;
    image.data[4*i + 3] = 255;
  });
  ctx.putImageData(image, 0, 0);

  // A simpler way to do the above, but possibly slower. keep in mind the legend width is stretched because the width attr of the canvas is 1
  // See http://stackoverflow.com/questions/4899799/whats-the-best-way-to-set-a-single-pixel-in-an-html5-canvas
  /*
  d3.range(legendheight).forEach(function(i) {
    ctx.fillStyle = colorscale(legendscale.invert(i));
    ctx.fillRect(0,i,1,1);
  });
  */

  var legendaxis = d3.axisRight()
    .scale(legendscale)
    .tickSize(6)
    .ticks(8);

  var svg = d3.select(selector_id)
    .append("svg")
    .attr("height", (legendheight) + "px")
    .attr("width", (legendwidth) + "px")
    .style("position", "absolute")
    .style("left", "0px")
    .style("top", "0px")

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + (legendwidth - margin.left - margin.right + 3) + "," + (margin.top) + ")")
    .call(legendaxis);

  d3.select('defs').remove();
  return true;
};



      function query(data_id,x,y,len,sigmas,lr,iteration,neighbour,topology,activation,random,tag_color,tag_font,tag_map,tag_legend){

      $.ajax({
      type: "post",
      url: "/som/user_query_info",
      dataType: "json",
      data: JSON.stringify({user_id: "UID",data_id:data_id,
        x:x,
        y:y,
        len:len,
        sigmas:sigmas,
        lr:lr,
        iteration:iteration,
        neighbour:neighbour,
        topology:topology,
        activation:activation,
        random:random
      }),
      beforeSend: function(){

              // $('#m14_img').css('visibility','visible');
              // $('#u60').css('visibility','hidden');
              // $('#u61').css('visibility','hidden');
              // $('#u62').css('visibility','hidden');
              tag_color.value = 'blue'
              tag_font.value = 10
          },
      complete: function(){
              // $('#m14_img').css('visibility','hidden');
              // $('#u60').css('visibility','visible');
              // $('#u61').css('visibility','visible');
              // $('#u62').css('visibility','visible');
          },
      success: function as(raw_data) {

      setValue(raw_data);
      svg.remove();
      svg = d3.select(tag_map).append("svg")
      .attr("width", document.querySelector('#m14').offsetWidth)
      .attr("height", document.querySelector('#m14').offsetHeight);
      g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      // l = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      a = d3.select("body").append("div").classed('tooltip', true).style("visibility", "hidden");










      MapColumns = col()*2;
      MapRows = row()*2;
      hexRadius = d3.min([width/((MapColumns + 0.5) * Math.sqrt(3)),
      height/((MapRows + 1/3) * 1.5)]);
      width1 = MapColumns*hexRadius*Math.sqrt(3);
      height1 = MapRows*1.5*hexRadius+0.5*hexRadius;
      // h = hexRadius  * 1.5;
      h = (height1/(MapRows/2))/2;
      //   h = height/((MapRows + 1/3) * 1.5);
var colorScale1 = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 1]);

continuous(tag_legend, colorScale1);







      a.classed('tooltip', true);
      init_dt = get_point();
      // var point = get_point();
      var point = get_point();
      w = (width/((MapColumns + 0.5) * Math.sqrt(3)))/2;
        // w = width1/MapColumns
      g.append("clipPath")
      .attr("id", "clip")
      .append("rect")
      .attr("width", width1)
      .attr("height", height1);

      g.append("g")
      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)")
      .selectAll(".hexagon")
      .data(point)
      .enter().append("path")
      .attr("d", function (d) {
		return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
	})
         .attr("stroke", function (d,i) {
		return "#e5b367";
	})
      .attr("stroke-width", "1px")
      .attr("fill", function(d){ return d.color; })
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
      .call(_drag)
        .on('mouseover', mouseOver);
        // .on('mouseout', mouseOut)
        // .on('mousemove', mouseMove);

      g.append("g")
      .attr("class", "hexagon")
      .attr("clip-path", "url(#clip)")
      .selectAll("labels")
      .data(point)
      .enter()
      .append("text")
              .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .text(function(d){ return d.label; })
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central")
        .style("font-size", 10)
        .style("fill", "black");



      },
      error: function() {
            alert("Failure to access, please refresh the page");
            }
      })
      ;
      }

      function change_font(tag){
      g.selectAll("text").style("font-size", tag.value);

      }

function change_color(tag,tag2){

      data['color'] = tag.value


      if (tag.value === 'blue'){
        var colorScale1 = d3.scaleSequential(d3.interpolateBlues)
        .domain([0, 1]);
      }else if(tag.value === 'red'){
        var colorScale1 = d3.scaleSequential(d3.interpolateReds)
        .domain([0, 1]);
      }else if(tag.value === 'green'){
        var colorScale1 = d3.scaleSequential(d3.interpolateGreens)
        .domain([0, 1]);
      }else if(tag.value === 'blue to red'){
        var colorScale1 = d3.scaleSequential(t => d3.interpolateRdBu(1-t))
        .domain([0, 1]);
      }


continuous(tag2, colorScale1);


      $.ajax({
      type: "post",
      url: "/som/ChangeColor",
      dataType: "json",
      data: JSON.stringify(getValue()),

      success: function as(raw_data) {
        setValue(raw_data);
        init_dt = get_point();
        point = get_point();
        g.selectAll("path").remove();
        g.selectAll("text").remove();
        g.append("g")
        .attr("class", "hexagon")
        .attr("clip-path", "url(#clip)")
        .selectAll(".hexagon")
        .data(point)
        .enter().append("path")
        .attr("d", function (d) {
          return "M" + d.x + "," + d.y + hexbin.radius(hexRadius).hexagon();
      })
           .attr("stroke", function (d,i) {
          return "#e5b367";
      })
        .attr("stroke-width", "1px")
        .attr("fill", function(d){ return d.color; })
                .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
        .call(_drag)
          .on('mouseover', mouseOver);

        g.append("g")
        .attr("class", "hexagon")
        .attr("clip-path", "url(#clip)")
        .selectAll("labels")
        .data(point)
        .enter()
        .append("text")
                .attr("transform","translate("+(width1)/24+","+(height1)/24+")")
          .attr("x", function(d){return d.x})
          .attr("y", function(d){return d.y})
          .text(function(d){ return d.label; })
          .attr("text-anchor", "middle")
          .attr("alignment-baseline", "central")
          .style("font-size", 10)
          .style("fill", "black");
        // alert(1);
      }
      })
      ;
      }
