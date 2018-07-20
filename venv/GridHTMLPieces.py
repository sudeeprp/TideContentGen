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
.nomargins {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
}
.bigborder {
    background: url(imgbackground-sheet0.png);
    background-repeat: no-repeat;
    background-size: 100% 100vh;
    width: 100%;
    height: 100vh;
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
}
.content {
    padding: 50px;
    width: 100%;
    height: 100vh;
    text-align: center;
}
.picture, .done_picture {
    padding: 20px;
    border: 3px solid transparent;
}
.done_picture {
    border: 3px solid green;
    box-shadow: 5px 5px 3px grey;
}
.grid_table {
    width: 100vw;
}
.milestone_head {
    margin-top: 3px;
    font-family: Verdana;
    font-weight: bold;
    background: linear-gradient(to left, #43c6ac, #f8ffae);
}
.activity_list {
    background-color: lightgreen;
    text-align: center;
    background: linear-gradient(to bottom right, lightblue, lightgreen);
}
figure {
    display: inline-block;
    margin: 2px;
}
figure img {
    vertical-align: top;
}
figure figcaption {
    text-align: center;
    font-family: Verdana;
}
</style>
'''

tail = '''\
</html>
'''
