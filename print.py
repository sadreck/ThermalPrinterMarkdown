from lib.Config import Config
from lib.InputData import InputData
from lib.MarkdownToEscPos import MarkdownToEscPos
from lib.ThermalPrinter import ThermalPrinter
import sys

__version__ = '1.0.0'

try:
    config = Config()
    config.validate()

    # The first argument is the filename.
    sys.argv.pop(0)
    if len(sys.argv) == 0:
        raise Exception("ThermalPrinterMarkdown v{0}\n\nUsage: print.py file-to-print.md".format(__version__))

    contents = InputData().load(sys.argv[0], 'file')

    markdown = MarkdownToEscPos(config.printer_line_width).convert(contents)

    ThermalPrinter(config).print(markdown)

except Exception as e:
    print(e)
    exit(1)
