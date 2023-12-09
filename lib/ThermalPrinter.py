from lib.Config import Config
from typing import Union
from escpos.printer import Network
from datetime import datetime


class ThermalPrinter:
    __config: Config = None

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, value: Config):
        self.__config = value

    def __init__(self, config: Config):
        self.config = config

    def print(self, markdown: list):
        printer = self.__load_printer()
        if printer is None:
            raise Exception('Could not initialise printer')

        max_lines = self.config.printer_max_lines
        line_count = 0
        for letter in markdown:
            if letter['ln']:
                printer.ln()
                line_count += 1
                if 0 < max_lines < line_count:
                    printer.set(custom_size=False, normal_textsize=True, align='center')
                    printer.ln()
                    printer.text('***** TRUNCATED *****')
                    printer.ln()
                    break
                continue
            elif 'qr' in letter:
                printer.set(align='center')
                printer.qr(letter['qr'], size=8, center=True)
                continue

            printer.set(
                underline=letter['format']['underline'],
                bold=letter['format']['bold'],
                custom_size=letter['format']['custom_size'],
                normal_textsize=letter['format']['normal_textsize'],
                width=letter['format']['width'],
                height=letter['format']['height'],
                align=letter['format']['align']
            )

            if letter['char'] is not None:
                printer.text(letter['char'])

        printer.ln()

        printer.set(normal_textsize=True, align='left', bold=False, underline=False)

        printer.textln('*' * self.config.printer_line_width)
        printer.textln(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        printer.cut()

    def __load_printer(self) -> Union[None, Network]:
        if self.config.printer_type == 'network':
            return Network(self.config.printer_ip, self.config.printer_port)
        return None
