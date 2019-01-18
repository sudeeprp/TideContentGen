begin_head='''\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Chapter Selector</title>

<style>
html {
height: 100%;
}
body {
user-select: none;
}
.nomargins {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
}
.student_status_pic {
    max-height: 24px;
}
.student_thumbnail {
    width:100px;
    height:100px;
    padding-top:3px;
    padding-left:3px;
    padding-bottom:3px;
}
.student_figure {
    display: inline-block;
    border: 1px solid gray;
    border-radius: 5px;
    margin: 2px;
    max-width: 120px;
    vertical-align: top;
}
.student_figcaption, .chapter_figcaption {
    text-align: center;
    font-family: Verdana;
    margin-left: 3px;
    margin-right: 3px;
}
.student_figcaption {
    font-size: small;
    white-space: normal;
}
.chapter_figcaption {
    font-size: medium
}
.chapter_table, .chapter_cell, .chapter_icon {
    border-collapse:collapse; border:1px solid #FF00FF;
}
.chapter_table, .chapter_cell {
    text-align: left;
}
.chapter_table {
    width: 100%;
    table-layout: fixed;
}
.chapter_icon {
    width:8cm;
    text-align: center;
}
figure img {
    vertical-align: middle;
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-height: 64px;
    max-width: 200px;
}
.refresh_pic {
  max-height: 48px;
  position: absolute;
  right: 8px;
  top: 8px;
}
</style>
'''
script_head='''\
<script>
'''
scripts='''\
function refresh_status() {
    var numChapters = chapters.length;
    for(var i = 0; i < numChapters; i++) {
        var status = Android.getChapterStatus(chapters[i]);
        document.getElementById(chapters[i] + '.status').src = 'chapter_' + status + '.png';
    }
}
function set_students_in_chapter(chapter, students_in_chapter) {
    var students_html = ''
    var numStudents = students_in_chapter.length;
    for(var i = 0; i < numStudents; i++) {
        students_html += "<figure class=student_figure><img class=student_thumbnail src='data:image/jpeg;base64, " +
                students_in_chapter[i].thumbnail + "'/>";
        if('status' in students_in_chapter[i]) {
            students_html += "<img class=student_status_pic src='chapter_" + students_in_chapter[i].status + ".png'/>";
        }
        students_html += "<figcaption class=student_figcaption>" + students_in_chapter[i].name + "</figcaption></figure>";
    }
    document.getElementById(chapter + '.students').innerHTML = students_html;
}
function refresh_students() {
    var studentsInSubjectJSON = Android.getStudentsInSubject();
    var students_in_subject = JSON.parse(studentsInSubjectJSON);
    var numChapters = students_in_subject.length;
    for(var i = 0; i < numChapters; i++) {
        var students_in_chapter = students_in_subject[i].students;
        set_students_in_chapter(students_in_subject[i].chapter_name, students_in_chapter);
    }
}
function refresh_heading() {
    document.getElementById('current_grade').innerHTML = Android.getCurrentGrade();
    document.getElementById('current_subject').innerHTML = Android.getCurrentSubject();
}
function refresh_screen() {
    refresh_heading();
    refresh_status();
    refresh_students();
}
function set_active_chapter(chapter) {
    Android.setChapterActive(chapter);
    refresh_screen();
}
</script>
'''
body_table_start='''\
<body onload="Android.selectorEntered(); refresh_screen();">
<h1><span id=current_grade></span>&nbsp;&nbsp;&nbsp;<span id=current_subject></span></h1>
<img class=refresh_pic onclick="refresh_screen();" src="refresh.png">
<table class="chapter_table">
'''
body_table_end='''\
</table>
</body>
'''
end_tail='''\
</html>'''
