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
    background-image: url('1-French.png'), url('1-French.png'), url('1-French.png'), url('1-French.png');
    background-repeat: repeat-x, repeat-y, repeat-x, repeat-y;
    background-attachment: fixed;
    background-position: top, left, bottom, right; 
}
.content {
    padding: 25px;
    width: 100%;
    height: 100vh;
    text-align: center;
}
.picture, .done_picture {
    padding: 2px;
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
.overall_done_hidden, .overall_done_visible, .next_screen_hidden, .next_screen_visible, .prev_screen_hidden, .prev_screen_visible {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    position: fixed;
}
.overall_done_hidden, .overall_done_visible, .next_screen_hidden, .next_screen_visible {
    right: 0; bottom: 0;
}
.prev_screen_hidden, .prev_screen_visible {
    left: 0; bottom: 0;
}
.overall_done_hidden, .next_screen_hidden, .prev_screen_hidden {
    visibility: hidden;
}
.overall_done_visible, .next_screen_visible, prev_screen_visible {
    visibility: visible;
}
</style>
'''

tail = '''\
</html>
'''

content_holder = '''\
<div id='screen'>
<p>No content.</p>
</div>
'''

next_prev = '''\
<a onclick="next_screen()"><img id=next_button class="next_screen_hidden" src="nextsheetsheet-sheet1.png"></a>
<a onclick="prev_screen()"><img id=prev_button class="prev_screen_hidden" src="backarrow1-sheet0.png"></a>
'''
script_to_check_mark_complete = '''\
function check_mark_complete() {
    var all_done = true;
    for(var item_done in screen_state[current_screen]) {
        if(screen_state[current_screen][item_done] == 0) {
            all_done = false;
            break;
        }
    }
    if(all_done == true) {
        if(current_screen < screen_state.length - 1) {
            document.getElementById("next_button").setAttribute("class", "next_screen_visible");
            document.getElementById("bell-sheet0.png.pic").setAttribute("class", "overall_done_hidden");
        } else {
            document.getElementById("bell-sheet0.png.pic").setAttribute("class", "overall_done_visible");
            document.getElementById("next_button").setAttribute("class", "next_screen_hidden");
        }
    }
    else {
        document.getElementById("next_button").setAttribute("class", "next_screen_hidden");
        document.getElementById("bell-sheet0.png.pic").setAttribute("class", "overall_done_hidden");
    }
}
'''

script_to_mark_tap_listen = '''\
function mark_tap(id) {
    if(screen_state[current_screen][id] != null)
    {
        document.getElementById(id).setAttribute("class", "done_picture");
        screen_state[current_screen][id]++;
        check_mark_complete();
    }
}
'''

script_to_switch_next_screen = '''\
function next_screen() {
    if(current_screen < screen_state.length - 1) current_screen++;
    refresh_screen()
}
'''

script_to_switch_prev_screen = '''\
function prev_screen() {
    if(current_screen > 0) current_screen--;
    refresh_screen()
}
'''

script_to_refresh = '''\
function refresh_screen() {
    document.getElementById('screen').innerHTML = screen_html[current_screen];
    if(current_screen > 0) {
        document.getElementById("prev_button").setAttribute("class", "prev_screen_visible");
    }
    else {
        document.getElementById("prev_button").setAttribute("class", "prev_screen_hidden");
    }
    for(var item_done in screen_state[current_screen]) {
        if(screen_state[current_screen][item_done] > 0) {
            document.getElementById(item_done).setAttribute("class", "done_picture");
        }
    }

    check_mark_complete()
}
'''
