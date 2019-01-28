begin_head = '''\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>The Grid</title>

<style>
html {
height: 100%;
}
body {
overflow-y: hidden;
user-select: none;
}
table { border: none; border-collapse: collapse; }
.nomargins {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
}
.grid_table {
    text-align: center;
    width: auto;
    table-layout: fixed;
    background: url("map_paper.png");
}
figure {
    display: inline-block;
    margin: 2px;
}
figure img {
    vertical-align: top;
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-height: 100px;
    max-width: 200px;
}
figure figcaption {
    text-align: center;
    font-family: Verdana;
    font-weight: bold;
    font-size: large;
}
.linkimages {
    max-height:320px;
    max-width:80px;
}
.chapterhead {
    position: fixed;
    top: 0;
    left: 0;
}
.activity_status_pic {
  max-height: 24px;
  display: inline;
}
.refresh_pic {
  max-height: 48px;
  position: absolute;
  right: 8px;
  top: 8px;
}
</style>
<script>
function refresh_screen() {
  refresh();
}
function refresh() {
  var activitiesStatusJSON = Android.getActivitiesStatus();
  var activitiesStatus = JSON.parse(activitiesStatusJSON);
  for(var activityID in activitiesStatus) {
    if(activitiesStatus.hasOwnProperty(activityID)) {
      var activityStatusImgID = activityID.replace(/ /g, "%20") + "_status";
      var status_img = document.getElementById(activityStatusImgID);
      if(status_img != null) {
        status_img.src = "chapter_" + activitiesStatus[activityID] + ".png";
      } else {
        console.log("Ayyo, element " + activityStatusImgID + " not found");
      }
    }
  }
}
</script>
</head>
'''
tail = '''\
</html>
'''
