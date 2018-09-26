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
user-select: none;
}
.nomargins {
    margin-top: 0px;
    margin-left: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
}
.content {
    padding: 25px;
    width: 100%;
    height: 100vh;
    text-align: center;
}
.hidden_picture {
    visibility: hidden;
}
.picture, .done_picture {
    font-family: Arial, Helvetica, sans-serif;
    padding: 2px;
    border: 3px solid transparent;
    visibility: inherit;
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

script_to_play_and_mark = '''\
function play_and_mark(audio, picture) {
    audio_element = document.getElementById(audio);
    audio_element.onended = function() {
        refresh_image_states();
    };
    audio_element.play();
    mark_tap(picture);
}
'''
script_to_refresh_next_and_prev = '''\
function refresh_next(all_done) {
    if(all_done == true) {
        if(current_screen < screen_state.length - 1) {
            document.getElementById("next_button").setAttribute("class", "next_screen_visible");
            document.getElementById("bell-sheet0.png.id").setAttribute("class", "overall_done_hidden");
        } else {
            document.getElementById("bell-sheet0.png.id").setAttribute("class", "overall_done_visible");
            document.getElementById("next_button").setAttribute("class", "next_screen_hidden");
        }
    }
    else {
        document.getElementById("next_button").setAttribute("class", "next_screen_hidden");
        document.getElementById("bell-sheet0.png.id").setAttribute("class", "overall_done_hidden");
    }
}
function refresh_prev() {
    if(current_screen > 0) {
        document.getElementById("prev_button").setAttribute("class", "prev_screen_visible");
    }
    else {
        document.getElementById("prev_button").setAttribute("class", "prev_screen_hidden");
    }
}
'''

script_to_mark_tap_listen = '''\
function mark_tap(id) {
    if(screen_state[current_screen][id] != null) {
        screen_state[current_screen][id].hitcount++;
        document.getElementById(id).setAttribute("class", "done_picture");
    }
}
'''

script_to_next_and_prev = '''\
function next_screen() {
    if(current_screen < screen_state.length - 1) current_screen++;
    refresh_screen()
}
function prev_screen() {
    if(current_screen > 0) current_screen--;
    refresh_screen();
}
'''

script_to_refresh_image_states = '''\
function refresh_image_states() {
    var all_done = true;
    for(var item_done in screen_state[current_screen]) {
        var after = screen_state[current_screen][item_done].after;
        if(after == "" || screen_state[current_screen][after].hitcount > 0) {
            document.getElementById(item_done).setAttribute("class", "picture")
        }
        if(screen_state[current_screen][item_done].hitcount > 0) {
            document.getElementById(item_done).setAttribute("class", "done_picture");
        } else {
            all_done = false;
        }
    }
    refresh_next(all_done)
}
'''

script_to_refresh = '''\
function refresh_screen() {
    document.getElementById('screen').innerHTML = screen_html[current_screen];
    refresh_prev();
    refresh_image_states();
}
'''
