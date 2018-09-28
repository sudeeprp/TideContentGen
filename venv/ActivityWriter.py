import os
import shutil
import json
import ActivityHTMLPieces
import pandas as pd
from urllib.parse import quote

common_files = ['bell-sheet0.png', 'img_speakerbtn-sheet0.png', 'nextsheetsheet-sheet1.png',
                'backarrow1-sheet0.png', 'done-sheet0.png', 'clap1.ogg', 'MyDearWatson-Regular.woff']

def copy_common_resources(source_dir, destination_dir):
    for file in common_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(destination_dir, file))

def file2id(filename, id_extension = ''):
    if filename == '':
        return ''
    else:
        return quote(filename.replace(' ', '_') + id_extension)

def image_html_line(imagefile, class_name, attrs = ''):
    return '<img id=' + file2id(imagefile, '.id') + ' class="' + class_name + '" ' + attrs + \
           ' src="' + quote(imagefile) + '" alt="' + imagefile + '">\n'

def text_html_para(cell_text, class_name, attrs = ''):
    return '<p id=' + file2id(cell_text,'.id') + ' class="' + class_name + '" ' + attrs + '>' + cell_text + '</p>\n'

class ActivityWriter:
    def __init__(self, pics_to_sounds):
        self.pics_sounds_map = pics_to_sounds
        return

    def create_html(self, activity_dir):
        self.activity_dir = activity_dir
        os.makedirs(self.activity_dir, exist_ok=True)
        copy_common_resources('.', self.activity_dir)
        html_file = open(os.path.join(self.activity_dir, 'index.html'), "w")
        return html_file

    def write_content_start(self, html_file):
        html_file.write('<body class="nomargins" onload="refresh_screen()">\n')

    def write_instruction(self, html_file, layout):
        instruction_pic = 'img_speakerbtn-sheet0.png'
        instruction_sound = layout['instruction.sound']
        shutil.copy(instruction_sound, os.path.join(self.activity_dir, instruction_sound))
        html_file.write('<audio autoplay id=' + file2id(instruction_sound) + '> <source src="' + quote(instruction_sound) +\
                        '" type="audio/' + instruction_sound.split('.')[-1] + '"></audio>\n')
        html_file.write('<a onclick="document.getElementById(\'' + file2id(instruction_sound) + '\').play();">\n')
        html_file.write(image_html_line(instruction_pic, 'instruction'))
        html_file.write('</a>\n')

    def write_content_holder(self, html_file):
        html_file.write(ActivityHTMLPieces.content_holder)

    def audio_source_and_play_instruction(self, imagename, image_ident):
        audio_source = None
        play_instruction = None
        if imagename in self.pics_sounds_map:
            audio = self.pics_sounds_map[imagename]
            audio_source = '<audio id=' + file2id(audio) + '> <source src="' + quote(audio) + \
                           '" type="audio/' + audio.split('.')[-1] + '"></audio>\n'
            play_instruction = "play_and_mark('" + file2id(audio) + "', '" + image_ident + "');"
            shutil.copy(audio, os.path.join(self.activity_dir, audio))
        else:
            print(imagename + ': no sound')
        return audio_source, play_instruction

    def compute_rowspan(self, images_layout, row_number, column_number):
        i = row_number + 1
        while i < len(images_layout) and \
                images_layout[i][column_number] is not None and 'merge_above' in images_layout[i][column_number]:
            i += 1
        rowspan = i - row_number
        return rowspan

    def rowspan_html(self, rowspan):
        if rowspan > 1:
            return ' rowspan=' + str(rowspan)
        else:
            return ''

    def get_rows_cols(self, images_layout):
        df = pd.DataFrame(images_layout)
        rows = df.count(axis=1).astype(bool).sum()
        cols = df.count(axis=0).astype(bool).sum()
        return rows, cols

    def write_screen_table(self, html_file, images_layout):
        html_file.write('<table class="content">\n')
        rows, cols = self.get_rows_cols(images_layout)
        for row_number in range(0, len(images_layout)):
            html_file.write('<tr>\n')
            for column_number in range (0, len(images_layout[row_number])):
                rowspan = self.compute_rowspan(images_layout, row_number, column_number)
                image_layout = images_layout[row_number][column_number]
                picture = html_line = initial_display_style = attr = None
                if image_layout is not None:
                    if 'image' in image_layout:
                        picture = image_layout['image']
                        attr = 'style="max-height:' + str(80 // rows * rowspan) + 'vh;max-width:' + \
                                    str(90 // cols) + 'vw;" '
                        html_line = image_html_line
                        shutil.copy(picture, self.activity_dir + '/' + picture)
                    if 'text' in image_layout:
                        picture = image_layout['text']
                        attr = 'style="font-size:500%"'
                        html_line = text_html_para
                    if 'merge_above' in image_layout: continue

                html_file.write('<td' + self.rowspan_html(rowspan) + '>\n')
                if picture is not None:
                    picture_id = file2id(picture, '.id')
                    audio_source, play_instruction = self.audio_source_and_play_instruction(picture, picture_id)
                    if audio_source is not None:
                        html_file.write(audio_source)
                    if play_instruction is not None:
                        html_file.write('<a onclick="' + play_instruction + 'mark_tap(\'' + picture_id + '\');">\n')
                        html_file.write(html_line(picture, "hidden_picture", attr))
                        html_file.write('</a>')
                    else:
                        html_file.write(html_line(picture, "picture", attr))
                html_file.write('</td>\n')
            html_file.write('</tr>\n')
        html_file.write('</table>\n')

    def write_content_end(self, html_file):
        html_file.write(ActivityHTMLPieces.next_prev)
        html_file.write(ActivityHTMLPieces.overall_done)

    def close_html(self, html_file):
        html_file.write('</body>\n')
        html_file.write(ActivityHTMLPieces.tail)
        html_file.close()

    def write_screens_html_array(self, html_file, layout):
        is_first_screen = True
        for screen in layout['images.layout']:
            if not is_first_screen:
                html_file.write(',\n')
            html_file.write('`\n')
            self.write_screen_table(html_file, screen)
            html_file.write('`')
            is_first_screen = False

    def write_screen_status(self, html_file, layout):
        screen_state = []
        for screen in layout['images.layout']:
            one_screen_state = {}
            for image_layout in sum(screen, []):
                if image_layout is not None:
                    picture = None
                    if 'image' in image_layout and image_layout['image'] is not None and \
                            image_layout['image'] in self.pics_sounds_map:
                        picture = image_layout['image']
                    if 'text' in image_layout and image_layout['text'] is not None and \
                            image_layout['text'] in self.pics_sounds_map:
                        picture = image_layout['text']
                    if picture is not None:
                        one_screen_state[file2id(picture,'.id')] = {"hitcount": 0, "after": file2id(image_layout['after'],'.id')}
            screen_state.append(one_screen_state)
        s = json.dumps(screen_state)
        html_file.write(s)

    def write_tap_listen_script(self, html_file, layout):
        html_file.write('<script>\n')
        html_file.write('var screen_state = ')
        self.write_screen_status(html_file, layout)
        html_file.write(';\n')
        html_file.write('var current_screen = 0;\n')
        html_file.write('var screen_html = [\n')
        self.write_screens_html_array(html_file, layout)
        html_file.write('\n]\n')
        html_file.write(ActivityHTMLPieces.script_to_play_and_mark)
        html_file.write(ActivityHTMLPieces.script_to_refresh_next_and_prev)
        html_file.write(ActivityHTMLPieces.script_to_mark_tap_listen)
        html_file.write(ActivityHTMLPieces.script_to_next_and_prev)
        html_file.write(ActivityHTMLPieces.script_to_refresh_image_states)
        html_file.write(ActivityHTMLPieces.script_to_refresh)
        html_file.write('</script>\n')

    def write_title(self, html_file, layout):
        html_file.write('<p class=title_text>')
        html_title = layout['title'].encode('ascii', 'xmlcharrefreplace')
        html_file.write(html_title.decode("utf-8"))
        html_file.write('</p>\n')

    def write_tap_listen(self, activity_dir, layout):
        html_file = self.create_html(activity_dir)
        html_file.write(ActivityHTMLPieces.begin_head)
        self.write_tap_listen_script(html_file, layout)
        html_file.write('</head>\n')
        self.write_content_start(html_file)
        self.write_instruction(html_file, layout)
        self.write_title(html_file, layout)
        self.write_content_holder(html_file)
        self.write_content_end(html_file)
        self.close_html(html_file)
