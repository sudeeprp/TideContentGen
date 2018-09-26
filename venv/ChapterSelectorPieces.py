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
figure {
    display: inline-block;
    margin: 2px;
}
figure img {
    vertical-align: middle;
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-height: 64px;
    max-width: 200px;
}
figure figcaption {
    text-align: center;
    font-family: Verdana;
    font-size: medium;
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
        students_html += "<figure><img style='width:100px;height:100px;padding-top:3px;padding-left:3px;padding-bottom:3px;' src='data:image/jpeg;base64, " + 
                students_in_chapter[i].thumbnail + "' /><figcaption>" + students_in_chapter[i].name + "</figcaption></figure>";
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
    console.log("done with refresh_students. i is " + i);
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
<table class="chapter_table">
'''
body_table_end='''\
</table>
</body>
'''
end_tail='''\
</html>'''
