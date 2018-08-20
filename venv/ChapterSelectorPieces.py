begin_head='''\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>The Grid</title>

<style>
html {
height: 100%;
}
.nomargins {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
}
.chapter_table, .chapter_cell {
    border-collapse:collapse; border:1px solid #FF00FF;
    text-align: left;
}
.chapter_table {
    width: 90%;
    table-layout: fixed;
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
    font-size: small;
}
</style>
'''
script_head='''\
<script>
'''
scripts='''\
function refresh_status() {
    numChapters = chapters.length;
    for(i = 0; i < numChapters; i++) {
        status = Android.getChapterStatus(chapters[i]);
        document.getElementById(chapters[i] + '.status').src = 'chapter_' + status + '.png';
    }
}
function set_students_in_chapter(chapter, students_in_chapter) {
    students_html = ''
    numStudents = students_in_chapter.length;
    for(i = 0; i < numStudents; i++) {
        console.log('got thumbnail:')
        console.log(students_in_chapter[i].thumbnail)
        students_html += "<img style='display:block; width:100px;height:100px;' src='data:image/jpeg;base64, " + students_in_chapter[i].thumbnail + "' />";
    }
    document.getElementById(chapter + '.students').innerHTML = students_html;
}
function refresh_students() {
    numChapters = chapters.length;
    for(i = 0; i < numChapters; i++) {
        var studentsInChapterJSON = Android.getStudentsInChapter(chapters[i])
        console.log("**Got json")
        console.log(studentsInChapterJSON)
        var students_in_chapter = JSON.parse(studentsInChapterJSON);
        console.log("Got students " + students_in_chapter.length);
        if(students_in_chapter.length > 0) {
            set_students_in_chapter(chapters[i], students_in_chapter);
        }
    }
}
function refresh_screen() {
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
<body onload="refresh_screen()">
<table class="chapter_table">
'''
body_table_end='''\
</table>
</body>
'''
end_tail='''\
</html>'''
