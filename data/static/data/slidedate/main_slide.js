// url: /data/slidedate/
// 시간 흐름에 따른 맛집 분포 변화 - 한국

// svg box size
var width = 150,
    height = 80,
    margins = {},
    centered;

// Set margins around rendered map
margins.top    = 0,
margins.bottom = 0,
margins.left   = 0,
margins.right  = 0;

// Create a color scale
var categories = ["중식", "카페,디저트", "술집", "분식", "멕시코,남미음식", "인도음식", "일식",
  "양식", "한식", "브런치", "햄버거", "베트남음식", "특급호텔레스토랑", "패밀리레스토랑", "뷔페", "푸드코트",
  "두부요리", "아시아음식", "태국음식", "이탈리아음식", "프랑스음식", "태국음식", "스페인음식",
  "그리스,터키음식", "퓨전음식", "치킨,닭강정", "해물,생선요리", "스테이크,립", "피자", "샌드위치", "핫도그"],

color = d3.scaleOrdinal()
.domain(categories)
.range(["#574D68", "#BD6BFA", "#BBAEA5", "#00FFD4", "#5F5AFA", "#B496FF", "#467BFF",
"#F7CDFF", "#00348A", "#FA6A11", "#DBFF76", "#FFAA00", "#12664F", "#8FD175","#402D54",
"#D18975", "#C6D4FF", "#99FF66", "#D4F5F5", "#F19953", "#2660A4","#FAC8CD", "#0075E2",
"#FCEC52","#E2DBBE", "#493548", "#BE97C6","#283044", "#C33C54", "#3E1929", "#2F0722"]);

var projection = d3.geo.mercator()
    .center([126.9895, 37.5651])
    .scale(500)
    .translate([width/1.5, height/6]);

var path = d3.geo.path().projection(projection);

d3.queue()
    .defer(d3.json, topourl)
    .defer(d3.csv, dataurl)
    .awaitAll(render_map);


function render_map(error, result_data){
	if (error) { console.error(error) };

	var topology  = result_data[0],
		locations = result_data[1];

    var id = 0

    locations.forEach(function(d){
        d.id = id
        id = id + 1
    })

    var features = topojson.feature(topology, topology.objects.skorea_provinces_2018_geo).features;

    var sliderTime = d3
        .sliderBottom()
        .min(new Date(2010, 10))
        .max(new Date(2019, 05))
        .step(1000 * 60 * 60 * 24)
        .width(800)
        .tickFormat(d3.timeFormat('%Y %m'))
        .default(new Date(2010, 11))
        .on("onchange", function input(val) {
            update();
            d3.select('p#value-time').text(d3.timeFormat('%Y %m')(val));
        });

    var gTime = d3
        .select('div#slider-time')
        .append('svg')
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox","-12 -10 900 100")
        .attr('class', "slider-map")
        .append('g');

    gTime.call(sliderTime);

    d3.select('p#value-time')
        .text(d3.timeFormat('%Y %m')(sliderTime.value()));

    var svg = d3.select("#slidecontainer")
        .append("svg")
        .attr("viewBox",margins.top+" "+margins.left+" "+(width-margins.right)+" "+(height-margins.bottom))
        .attr("preserveAspectRatio", "xMidYMid meet")
        .append('g')
        .attr('class', "slidecontainer_group");

    var map = svg.append("g").attr("id", "map");

    map.selectAll("path")
        .data(features)
      .enter().append("path")
        .attr("class", function(d) { console.log(); return "municipality c" + d.properties.code; })
        .attr("d", path)
        .on("click", clicked);

    map.selectAll("text")
        .data(features)
      .enter().append("text")
        .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
        .attr("dy", ".35em")
        .attr("class", "municipality-label")
        .text(function(d) { return d.properties.name; })

    var loc = svg.append("g")
        .attr("class", "slidecontainer_locations");

    function update() {

        var slider_year = d3.timeFormat('%Y %m')(sliderTime.value())
        var new_data = locations.filter(function filter_by_year(d){ if (d["yr_mo"] == slider_year ) { return true; }});


        document.querySelectorAll(".slidecontaine_location_markers").forEach(function(d) {
            d.setAttribute("r",0);
        })

        new_data.forEach(function(d) {
            // console.log(d)
            var circle = loc.append("circle")
                .datum(d)
                .html(d)
                .attr('class', "slidecontaine_location_markers")
                .attr("cx", function(d) { return Number(projection([d.lon,d.lat])[0]); })
                .attr("cy", function(d) { return Number(projection([d.lon,d.lat])[1]); })
                .attr("r", function(d) { return d.post/600; })
                .style("fill", function(d) { return color(d.categ) })
                .style("opacity", 0.7)
                .append("title")
                .text(function(d) { return d.naver_title; });
        })




        // var places = loc.selectAll("circle")

        // var join = places.data(new_data)

        // var enter = join.enter()
        // var exit = join.exit()

        // enter.append("circle")
        //     .attr('class', "slidecontaine_location_markers")
        //     .attr("cx", function(d) { return Number(projection([d.lon,d.lat])[0]); })
        //     .attr("cy", function(d) { return Number(projection([d.lon,d.lat])[1]); })
        //     .attr("r", function(d) { return d.post/5; })
        //     .style("fill", function(d) { return color(d.categ) })
        //     .style("opacity", 0.7)
            // .append("title")
            // .text(function(d) { return d.naver_title; });

        // exit.remove();
    }

    update();

    function clicked(d) {
        var x, y, k;

        if (d && centered !== d) {
            var centroid = path.centroid(d);
            x = centroid[0];
            y = centroid[1];
            k = 10;
            centered = d;
        } else {
            x = width / 2;
            y = height / 2;
            k = 1;
            centered = null;
        }

        map.selectAll("path")
            .classed("active", centered && function(d) { return d === centered; });

        map.transition()
            .duration(750)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
            .style("stroke-width", 1 / k + "px");

        loc.selectAll("path")
            .classed("active", centered && function(d) { return d === centered; });

        loc.transition()
            .duration(750)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
            .style("stroke-width", 0.5 / k + "px");
    };
};

// dragElement(document.getElementById("Image"));

// function dragElement(elmnt) {
//     var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
//     document.getElementById("Style").onmousedown = dragMouseDown;

//     function dragMouseDown(e) {
//         e = e || window.event;
//         e.preventDefault();
//         // get the mouse cursor position at startup:
//         pos3 = e.clientX;
//         pos4 = e.clientY;
//         document.onmouseup = closeDragElement;
//         // call a function whenever the cursor moves:
//         document.onmousemove = elementDrag;
//     }

//     function elementDrag(e) {
//         e = e || window.event;
//         e.preventDefault();
//         // calculate the new cursor position:
//         pos1 = pos3 - e.clientX;
//         pos2 = pos4 - e.clientY;
//         pos3 = e.clientX;
//         pos4 = e.clientY;
//         // set the element's new position:
//         elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
//         elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
//         document.getElementById("Style").style.cursor = "grabbing";
//     }

//     function closeDragElement() {
//       // stop moving when mouse button is released:
//       document.onmouseup = null;
//       document.onmousemove = null;
//       document.getElementById("Style").style.cursor = "grab";
//     }
// }