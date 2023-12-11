from lib.Config import Config
from lib.InputData import InputData
from lib.MarkdownToEscPos import MarkdownToEscPos
from lib.ThermalPrinter import ThermalPrinter
import sys

__version__ = '1.0.0'

try:
    config = Config()
    config.validate()

    # contents = InputData().load(sys.argv[0], 'file')
    contents = InputData().load()
    if not contents or len(contents) == 0:
        raise Exception("ThermalPrinterMarkdown v{0}\n\nUsage: print.py file-to-print.md".format(__version__))

    markdown = MarkdownToEscPos(config.printer_line_width).convert(contents)

    ThermalPrinter(config).print(markdown)

except Exception as e:
    print(e)
    exit(1)
