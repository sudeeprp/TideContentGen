begin_head = '''\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Sub-grid</title>
<style>
body {
user-select: none;
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
.subactivity_spread {
    background: url("map_paper.png");
}
</style>
</head>

<body class=subactivity_spread>
'''

tail = '''\
</body>
</html>
'''
