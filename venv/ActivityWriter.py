import os
import shutil
import ActivityHTMLPieces
import pandas as pd

common_files = ['imgbackground-sheet0.png', 'bell-sheet0.png', 'img_speakerbtn-sheet0.png', 'tap_learn_instruction.ogg']

def copy_common_resources(source_dir, destination_dir):
    for file in common_files:
        shutil.copy(source_dir + '/' + file, destination_dir + '/' + file)

def image_html_line(imagefile, class_name, attrs = ''):
    return '<img id=' + imagefile + '.pic class="' + class_name + '" ' + attrs + ' src="' + imagefile + '" alt="' + imagefile + '">\n'

class ActivityWriter:
    def __init__(self):
        self.picmap = pd.read_csv('pics and sounds.csv', index_col='Picture')
        return

    def create_html(self, activity_dir):
        self.activity_dir = activity_dir
        os.makedirs(self.activity_dir, exist_ok=True)
        copy_common_resources('.', self.activity_dir)
        html_file = open(self.activity_dir + '/index.html', "w")
        return html_file

    def write_content_start(self, html_file, layout):
        html_file.write('<body class="nomargins">\n')
        html_file.write('<div class="bigborder">\n')
        self.write_instructions(html_file, 'img_speakerbtn-sheet0.png', layout['instruction.sound'])
        html_file.write('<table class="content">\n')

    def write_instructions(self, html_file, instruction_pic, instruction_sound):
        html_file.write('<audio id=' + instruction_sound + '> <source src="' + instruction_sound +\
                        '" type="audio/ogg"></audio>\n')
        html_file.write('<a onclick="document.getElementById(\'' + instruction_sound + '\').play();">\n')
        html_file.write(image_html_line(instruction_pic, 'instruction'))
        html_file.write('</a>\n')

    def audio_source_and_play_instruction(self, imagename):
        audio_source = ''
        play_instruction = ''
        audio = self.picmap.get('Sound').get(imagename)
        if audio is not None:
            audio_source = '<audio id=' + audio + '> <source src="' + audio + '" type="audio/ogg"></audio>\n'
            play_instruction = 'document.getElementById(\'' + audio + '\').play();'
            shutil.copy(audio, self.activity_dir + '/' + audio)
        return audio_source, play_instruction

    def compute_rowspan(self, images_layout, row_number, column_number):
        i = row_number + 1
        while i < len(images_layout) and images_layout[i][column_number]['image'] == '|':
            i += 1
        rowspan = i - row_number
        if rowspan > 1:
            return ' rowspan=' + str(rowspan)
        else:
            return ''

    def form_image_attr_tags(self, image_layout):
        attr_tags_string = ''
        if 'attrs' in image_layout:
            for attr in image_layout['attrs']:
                attr_tags_string += (attr + ' ')
        return attr_tags_string

    def write_content_rows(self, html_file, images_layout):
        for row_number in range(0, len(images_layout)):
            html_file.write('<tr>\n')
            for column_number in range (0, len(images_layout[row_number])):
                image_layout = images_layout[row_number][column_number]
                image_file = image_layout['image']
                if image_file == '|':
                    continue
                html_file.write('<td' + self.compute_rowspan(images_layout, row_number, column_number) + '>\n')
                if image_file is not None:
                    audio_source, play_instruction = self.audio_source_and_play_instruction(image_file)
                    html_file.write(audio_source)
                    html_file.write('<a onclick="' + play_instruction + 'mark_tap(\'' +image_file+ '.pic\');">\n')
                    html_file.write(image_html_line(image_file, 'picture', self.form_image_attr_tags(image_layout)))
                    html_file.write('</a>')
                    shutil.copy(image_file, self.activity_dir + '/' + image_file)
                html_file.write('</td>\n')
            html_file.write('</tr>\n')

    def write_content_end(self, html_file):
        html_file.write('</table>\n')
        html_file.write('<a onclick="Android.activityResult(\'Done!\')">')
        html_file.write(image_html_line('bell-sheet0.png', 'overall_done_hidden'))
        html_file.write('</a>')
        html_file.write('</div>\n')

    def close_html(self, html_file):
        html_file.write('</body>\n')
        html_file.write(ActivityHTMLPieces.tail)
        html_file.close()

    def write_tap_listen_script(self, html_file, layout):
        html_file.write('<script>\n')

        html_file.write('var screen_state = {')
        for image_layout in sum(layout['images.layout'], []):
            if image_layout['image'] is not None:
                html_file.write('\'' + image_layout['image'] + '.pic\': 0, ')
        html_file.write('};\n')

        html_file.write(ActivityHTMLPieces.script_to_check_mark_complete)
        html_file.write(ActivityHTMLPieces.script_to_mark_tap_listen)
        html_file.write('</script>\n')

    def write_tap_listen(self, activity_dir, layout):
        html_file = self.create_html(activity_dir)
        html_file.write(ActivityHTMLPieces.begin_head)
        self.write_tap_listen_script(html_file, layout)
        html_file.write('</head>\n')
        self.write_content_start(html_file, layout)
        self.write_content_rows(html_file, layout['images.layout'])
        self.write_content_end(html_file)
        self.close_html(html_file)
        shutil.copy(layout['logo'], activity_dir + '/' + layout['logo'])

