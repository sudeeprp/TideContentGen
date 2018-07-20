begin_head = '''\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Learn</title>

<style>
html {
height: 100%;
}
body {
overflow: hidden;
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
.instruction {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    position: fixed;
    top:0; left:0;
}
.done_picture {
    border: 3px solid green;
    box-shadow: 5px 5px 3px grey;
}
.overall_done_hidden, .overall_done_visible {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    position: fixed;
    right:0; bottom:0;
}
.overall_done_hidden {
    visibility: hidden;
}
.overall_done_visible {
    visibility: visible;
}
</style>
'''

tail = '''\
</html>
'''

script_head = '''\
<script type="text/javascript">
'''

script_to_check_mark_complete = '''\
function check_mark_complete() {
    var all_done = true;
    for(var item_done in screen_state) {
        if(screen_state[item_done] == 0) {
            all_done = false;
            break;
        }
    }
    if(all_done == true) {
        document.getElementById("bell-sheet0.png.pic").setAttribute("class", "overall_done_visible");
    }
}
'''

script_to_mark_tap_listen = '''\
function mark_tap(id) {
    document.getElementById(id).setAttribute("class", "done_picture");
    screen_state[id]++;
    check_mark_complete();
}
'''

script_tail = '''\
</script>
'''