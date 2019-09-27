// distribution_flag_navi.js navi 만들기

var slides = ["서울 Seoul", "경기 Gyeonggi", "강원 Gangwon", "인천 Incheon", "경상 Gyeongsang", "충청 Chungcheong", "대전 Daejeon",
 "전라 Jeolla", "울산 Ulsan", "광주 Gwangju", "대구 Daegu", "부산 Busan", "제주 Jeju"]
var str = '<ul>'

slides.forEach(function(slide) {
  var kr = slide.split(" ")[0]
  eng = slide.split(" ")[1].toLowerCase();

  str += '<li>'+ '<a class="on" href="/data/bubble/' + eng + '"/><span>'+ kr +'</span></a>' + '</li>';
});

str += '</ul>';
document.getElementById("states-navi").innerHTML = str;