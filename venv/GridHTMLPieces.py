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
    max-width: 100px;
}
figure figcaption {
    text-align: center;
    font-family: Verdana;
    font-size: medium;
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
</style>
</head>
'''
tail = '''\
</html>
'''
