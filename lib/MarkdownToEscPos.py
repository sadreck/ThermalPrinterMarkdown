import re
from copy import copy


class MarkdownToEscPos:
    __line_width: int = 0

    __valid_effects: list = ['line', 'asteriskline']

    @property
    def valid_effects(self) -> list:
        return self.__valid_effects

    @property
    def line_width(self) -> int:
        return self.__line_width

    @line_width.setter
    def line_width(self, value: int):
        self.__line_width = value

    def __init__(self, line_width: int):
        self.line_width = line_width

    def convert(self, contents: str) -> list:
        data = []
        lines = contents.split("\n")
        for line in lines:
            self.__parse_line(line, data)

        return self.__fix_line_width(data, self.line_width)

    def __fix_line_width(self, data: list, max_line_width: int) -> list:
        # This function will make sure that no line begins with a space and that words
        # don't break across lines.
        lines = self.__split_tokens_to_lines(data)

        new_data = []
        for line in lines:
            if len(line) > max_line_width:
                new_line = []
                while len(line) > 0:
                    word = self.__get_next_word(line)
                    line = line[len(word):]
                    if word[0]['char'] == ' ':
                        continue
                    if len(new_line) + len(word) > max_line_width:
                        new_data = new_data + new_line + [self.__new_line()]
                        new_line = word
                    else:
                        new_line = new_line + word

                if len(new_line) > 0:
                    new_data = new_data + new_line + [self.__new_line()]
            else:
                new_data = new_data + line + [self.__new_line()]

        return new_data

    def __parse_line(self, line: str, data: list):
        default_format = self.__get_default_format()

        # Extract the line's alignment, [align=left|right|center]
        alignment = re.match(r'^\[align=(.*?)]', line)
        if alignment:
            if alignment.group(1) in ['left', 'right', 'center']:
                default_format['align'] = alignment.group(1)
            line = line[len(alignment.group(0)):].strip()

        # Check if the line is a QR code. This check if after the alignment one so that
        # we get the option to align it manually.
        qr = re.match(r'^\[qr=(.*?)]', line)
        if qr:
            data.append({'format': None, 'char': None, 'ln': False, 'qr': qr.group(1)})
            return

        # Now we check for pre-build effects.
        effect = re.match(r'^\[effect=(.*?)]', line)
        if effect and effect.group(1) in self.valid_effects:
            char = ''
            if effect.group(1) == 'line':
                char = '-'
            elif effect.group(1) == 'asteriskline':
                char = '*'
            data.append({'format': default_format, 'char': char * self.line_width, 'ln': False})
            return

        # Parse any heading.
        line = self.__parse_heading(line, default_format)

        self.__parse_formatting(line, data, default_format)

        data.append(self.__new_line())

    def __parse_formatting(self, line: str, data: list, default_format: dict):
        # Split line into single characters.
        line = list(line)
        buffer = ''

        while len(line) > 0:
            c = line.pop(0)
            if c in ['_', '*']:
                buffer += c
                format_property = ''
                if buffer == '__':
                    format_property = 'underline'
                elif buffer == '**':
                    format_property = 'bold'
                elif len(buffer) == 2:
                    buffer = c

                if len(buffer) == 2:
                    buffer = ''
                    if not default_format[format_property]:
                        default_format[format_property] = True
                        data.append({'format': copy(default_format), 'char': None, 'ln': False})
                    else:
                        default_format[format_property] = False
                        data.append({'format': copy(default_format), 'char': None, 'ln': False})
            else:
                # No formatting here, just add the character to the list.
                if len(buffer) > 0:
                    # Add the previous character into the print list.
                    data.append({'format': copy(default_format), 'char': buffer, 'ln': False})
                    buffer = ''
                data.append({'format': copy(default_format), 'char': c, 'ln': False})

    def __parse_heading(self, line: str, default_format: dict) -> str:
        if line.startswith('##'):
            line = line[2:].strip()
            default_format['height'] = 2
            default_format['width'] = 2
            default_format['custom_size'] = True
        elif line.startswith('#'):
            line = line[1:].strip()
            default_format['height'] = 3
            default_format['width'] = 3
            default_format['custom_size'] = True
        return line

    def __get_default_format(self) -> dict:
        return {
                'align': 'left',
                'underline': False,
                'bold': False,
                'normal_textsize': True,
                'custom_size': False,
                'height': 1,
                'width': 1,
            }

    def __new_line(self):
        return {'format': None, 'char': None, 'ln': True}

    def __split_tokens_to_lines(self, data):
        lines = []
        line = []
        for letter in data:
            if letter['ln']:
                lines.append(line)
                line = []
                continue
            line.append(letter)

        return lines

    def __get_next_word(self, line):
        word = []
        for letter in line:
            word.append(letter)
            if letter['char'] in [' ']:
                break
        return word

    def __get_string_from_tokens(self, line):
        text = ''
        for letter in line:
            if letter['ln']:
                text += "\n"
            else:
                text += letter['char']
        return text
