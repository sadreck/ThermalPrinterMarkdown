from dotenv import load_dotenv
import os


class Config:
    __valid_printer_types: list = ['network']

    __printer_ip: str = ''

    __printer_port: int = 9100

    __printer_max_lines: int = 0

    __printer_line_width: int = 48

    __printer_type: str = 'network'

    @property
    def valid_printer_types(self) -> list:
        return self.__valid_printer_types

    @property
    def printer_ip(self) -> str:
        return self.__printer_ip

    @printer_ip.setter
    def printer_ip(self, value: str):
        self.__printer_ip = value

    @property
    def printer_port(self) -> int:
        return self.__printer_port

    @printer_port.setter
    def printer_port(self, value: int):
        self.__printer_port = value

    @property
    def printer_max_lines(self) -> int:
        return self.__printer_max_lines

    @printer_max_lines.setter
    def printer_max_lines(self, value: int):
        self.__printer_max_lines = value

    @property
    def printer_line_width(self) -> int:
        return self.__printer_line_width

    @printer_line_width.setter
    def printer_line_width(self, value: int):
        self.__printer_line_width = value

    @property
    def printer_type(self) -> str:
        return self.__printer_type

    @printer_type.setter
    def printer_type(self, value: str):
        self.__printer_type = value

    def __init__(self):
        load_dotenv()

        self.__load()

    def __load(self):
        ip = os.getenv('PRINTER_IP')
        port = os.getenv('PRINTER_PORT')
        max_lines = os.getenv('PRINTER_MAX_LINES')
        line_width = os.getenv('PRINTER_LINE_WIDTH')
        ptype = os.getenv('PRINTER_TYPE')

        if ip is not None:
            self.printer_ip = ip.strip()

        if port is not None and port.isnumeric():
            port = int(port)
            if 0 < port < 65535:
                self.printer_port = port

        if max_lines is not None and max_lines.isnumeric():
            max_lines = int(max_lines)
            if max_lines >= 0:
                self.printer_max_lines = max_lines

        if line_width is not None and line_width.isnumeric():
            line_width = int(line_width)
            if line_width > 0:
                self.printer_line_width = line_width

        if ptype is not None and ptype.lower() in self.valid_printer_types:
            self.printer_type = ptype.lower()

    def validate(self):
        if self.printer_type not in self.valid_printer_types:
            raise Exception('Printer type must be one of: {0}'.format(', '.join(self.valid_printer_types)))

        if self.printer_port == 'network':
            if len(self.printer_ip) == 0:
                raise Exception('Printer IP is empty')
            elif self.printer_port <= 0 or self.printer_port > 65535:
                raise Exception('Printer port must be between 1 and 65535')

        if self.printer_max_lines < 0:
            raise Exception('Printer max lines must be >= 0')
        elif self.printer_line_width <= 0:
            raise Exception('Printer line width must be > 0')
