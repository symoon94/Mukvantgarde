

// svg box size
var width = 1000,
    height = 600,
    centered;

var categories = ["중식", "카페,디저트", "술집", "분식", "멕시코,남미음식", "인도음식", "일식",
  "양식", "한식", "브런치", "햄버거", "베트남음식", "특급호텔레스토랑", "패밀리레스토랑", "뷔페", "푸드코트",
  "두부요리", "아시아음식", "태국음식", "이탈리아음식", "프랑스음식", "태국음식", "스페인음식",
  "그리스,터키음식", "퓨전음식", "치킨,닭강정", "해물,생선요리", "스테이크,립", "피자", "핫도그", "야식"],

  color = d3.scaleOrdinal()
      .domain(categories)
      .range(["#EE7785", "#574D68", "#a5d296", "#58C9B9", "#BBAEA5", "#00FFD4", "#5F5AFA", "#B496FF", "#467BFF",
      "#F7CDFF", "#00348A", "#FA6A11", "#DBFF76", "#FFAA00", "#12664F", "#8FD175","#402D54",
      "#D18975", "#C6D4FF", "#99FF66", "#D4F5F5", "#F19953", "#2660A4","#FAC8CD", "#0075E2",
      "#FCEC52","#E2DBBE", "#493548", "#BE97C6","#283044", "#C33C54", "#519D9E"]);

function get_category(d) {
var x;

for (x in categories)
    if (d.category.includes(categories[x])) {
    if (categories[x].includes(",")) {
    return categories[x].slice(0, categories[x].indexOf(","))
    } else {
    return categories[x]
    }
    } else {
    if (d.category.includes("돈가스")) {
        return "일식"
    } else if (d.category.includes("고기") || d.category.includes("갈비") || d.category.includes("도시락") || d.category.includes("죽")) {
        return "한식"
    } else if (d.category.includes("킹크랩요리")) {
        return "해물"
    } else if (d.category.includes("샌드위치")) {
        return "양식"
    }
    }

}

var svg = d3.select("#chart")
    .append("div")
    .classed("svg-container", true)
    .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "160 50 600 900")
    .classed("svg-content-responsive", true)


var map = svg.append("g").attr("id", "map")
.attr("width", width)
.attr("height", height),
places = svg.append("g").attr("id", "places")
.attr("width", width)
.attr("height", height);

