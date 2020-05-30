var xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET', '/reviews.json', true);
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      var obj = JSON.parse(xmlhttp.responseText);
      var reviews = obj.reviews;
      var refElem = document.getElementById("reviews");
      var newcontent = "<br><br><br><br><br>";
      for (i = 0; i < obj.reviews.length; i++) {
        var r = obj.reviews[i];
        newcontent += insert_review(r["rating"], r["review"], r["suggestion"]);
      }
      refElem.innerHTML = newcontent;
    }
};
xmlhttp.send(null);

var scale = ["", "😕  Bad", "😐  Okay", "🙂  Good", "😃  Great", "🤩  Excellent"];
var div1 = "<div class=\"row\">";
var div2 = "<div class=\"col s8 offset-s2\">";
var div3 = "<div class=\"card-panel white\">";
var div4 = "<span class=\"card-title\">";
var div5 = "</div></div></div>";

function insert_review(rating, rev, suggestion) {
  var review = div1 + div2 + div3 + div4 + scale[rating] + "</span><p>";
  return review + rev + "</p>" + "<p>" + suggestion + "</p>" + div5;
  // return review;
}