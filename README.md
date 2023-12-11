# Thermal Printer Markdown (ESC/POS)

This is a basic script that will allow you to print basic Markdown from your thermal printer.

Has only been tested with [MUNBYN Thermal Printer / ITPP047UE-WH-UK](https://www.amazon.co.uk/Thermal-MUNBYN-Ethernet-Restaurant-Business/dp/B07872SDT9) connected over network.

Its features include:

* Headings, alignment, underline, bold, QR, lines.
* Ensure lines don't begin with a space.
* Ensure words don't break across 2 lines.
* Ability to limit max number of printed lines.

Limitations:

* Currently only supports printing when device is connected on the network.

If you would like to support USB connections, please create an issue.

## Installation

The package `python-escpos` requires the following package:

```
sudo apt install libcups2-dev
```

Afterwards, create the virtual environment and install the project's requirements:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Configuration

At the moment this script only works for network receipt printers and is configured using a `.env` file in the same folder as `print.py`.

```
# Printer's IP address.
PRINTER_IP=192.168.1.10
# Printer's port - this is usually the default.
PRINTER_PORT=9100
# Set the max number of lines to prevent printing 2km of text. Set to zero (0) to print all lines.
PRINTER_MAX_LINES=30
# The width in mm supported by the printer.
PRINTER_LINE_WIDTH=48
# Type of printer, currently only 'network' is supported.
PRINTER_TYPE=network
```

## Usage

```
Usage:

python print.py [filename.md]

or

cat filename.md | python print.py
```

## Supported Features

The only markdown features that are supported are:

| Feature   | Description                                     |
|-----------|-------------------------------------------------|
| Heading 1 | Use '#'                                         |
| Heading 2 | Use '##'                                        |
| Underline | Enclose in double underscores: `__underline__`  |
| Bold | Enclose in double asterisks: `**bold**`         |
| QR | Syntax is`[qr=https://www.example.com]`         |
| Text alignment | Line must begin with `[align=left/right/center]` |
| Horizontal lines | Line must be `[effect=line/asteriskline]` |

The converter will also ensure that lines don't begin with a space and words don't break across two lines.

### Example

```
[align=center]# Hello!

This is an example of a message!

[qr=https://www.example.com]

[effect=asteriskline]

**This will be bold** and __this will be underlined__.
```
