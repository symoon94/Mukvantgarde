// 지도그리기 + 지도 위 점찍기

var projection = d3.geo.mercator()
    .center([126.9541, 35.3564])
    .scale(14000)
    .translate([width/2, height/2]);

var path = d3.geo.path().projection(projection);

d3.json("/static/topojson/Jeolla.json", function(error, data) {
    var features = topojson.feature(data, data.objects["Jeolla"]).features;

      map.selectAll("path")
          .data(features)
        .enter().append("path")
          .attr("class", function(d) { console.log(); return "municipality c" + d.properties.adm_cd })
          .attr("d", path)
          .on("click", clicked);

      map.selectAll("text")
          .data(features)
        .enter().append("text")
          .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
          .attr("dy", ".35em")
          .attr("class", "municipality-label")
          .text(function(d) { return d.properties.adm_nm.split(" ").splice(2,).join(" "); })
          .style("fill", "#444444");
});

d3.csv("/static/data/instadata/states/Jeolla.csv", function(data) {
  console.log(data);
  places.selectAll("circle")
    .data(data)
  .enter().append("circle")
    .attr('class', function(d) { return get_category(d) })
    .attr("cx", function(d) { return Number(projection(d.geo.replace("[","").replace("]","").split(", "))[0]); })
    .attr("cy", function(d) { return Number(projection(d.geo.replace("[","").replace("]","").split(", "))[1]); })
    .attr("r", function(d) { return d.post/2000; })
    .style("fill", function(d) { return color( get_category(d)) })
    .style("opacity", 0.7)
    .on("click", function(d, i) {window.open('https://www.instagram.com/explore/locations/'+d.loc_id)})
    .on("mouseover", function(d) {
        if (d.thumUrl != "") {
            return ShowPicture("Style", 1, d)
        }else{
            return ShowPicture("Style", 0, d)
        }})
    .append("title")
    .text(function(d) { return d.naver_title + "\n" + d.naver_address; })
    .style("fill","black")

  function get_category(d) {
    var x;

    for (x in categories)
      if (d.category.includes(categories[x])) {
        if (categories[x].includes(",")) {
        return categories[x].slice(0, categories[x].indexOf(","))
        }else{
        return categories[x]
        }
      } else {
        if (d.category.includes("돈가스")) {
          return "일식"
        } else {
          if (d.category.includes("고기") || d.category.includes("갈비") || d.category.includes("도시락") || d.category.includes("죽")) {
          return "한식"
          }
        }
      }

  }

  function update() {
    // For each check box:
    d3.selectAll(".checkbox").each(function(d){
      cb = d3.select(this);
      grp = cb.property("value")

      // If the box is check, I show the group
    if(cb.property("checked") && grp !== "all"){
      places.selectAll("."+grp).transition().duration(1000).style("opacity", 0.7).attr("r", function(d){ return d.post/2000 })
    }else{
      places.selectAll("."+grp).transition().duration(1000).style("opacity", 0).attr("r", 0)
    }
    })
  }

    // When a button change, I run the update function
    d3.selectAll(".checkbox").on("change",update);

    // And I initialize it at the beginning
    update()

  function ShowPicture(id, show, d) {
    var img = d.thumUrl,
    title = d.naver_title
    address = d.naver_address
    link = 'https://www.instagram.com/explore/locations/'+d.loc_id
    searchKey = d.naver_title + " " + d.naver_address
    adresslink = "https://m.map.naver.com/search2/search.nhn?query="+ searchKey +"&style=v4#/map/"

    if (img.includes("#") || img.includes("http://blogfiles.naver")) {
      show = "0"
    }

    if (show=="1"){
      document.getElementById(id).childNodes[1].style.visibility = "visible"
      document.getElementById(id).childNodes[1].src = img
    }
    else if (show=="0"){
      document.getElementById(id).childNodes[1].style.visibility = "hidden"
    }

    document.getElementById(id).childNodes[3].style.visibility = "visible"
    document.getElementById(id).childNodes[3].childNodes[1].childNodes[0].href = link
    document.getElementById(id).childNodes[3].childNodes[1].childNodes[0].innerHTML = "#" + title
    document.getElementById(id).childNodes[3].childNodes[3].childNodes[0].href = adresslink
    document.getElementById(id).childNodes[3].childNodes[3].childNodes[0].innerHTML = address;
  }


});

function CheckUncheckAll(){
    var  selectAllCheckbox=document.getElementById("checkUncheckAll");
      if (selectAllCheckbox.checked==true){
        var checkboxes =  document.getElementsByName("checkbox") ;
        for(var i=0, n=checkboxes.length;i<n;i++) {
          checkboxes[i].checked = true;
        }
      }else {
        var checkboxes =  document.getElementsByName("checkbox");
        for(var i=0, n=checkboxes.length;i<n;i++) {
          checkboxes[i].checked = false;
        }
      }
      }

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
      .style("stroke-width", 1.5 / k + "px");

  places.selectAll("path")
      .classed("active", centered && function(d) { return d === centered; });

  places.transition()
      .duration(750)
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
      .style("stroke-width", 1 / k + "px");
}


dragElement(document.getElementById("Image"));

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  document.getElementById("Style").onmousedown = dragMouseDown;

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    document.getElementById("Style").style.cursor = "grabbing";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
    document.getElementById("Style").style.cursor = "grab";
  }
}
