#!/usr/bin/env python3

import os
import sys
import struct
from datetime import datetime
import tempfile

# Constants
MAGIC = 0x8BADF00D
VERSION = 1

WORD_SIZE = 4
DWORD_SIZE = 8
DOUBLE_SIZE = 8

# Exit on failure conditions
def fail(msg):
    sys.exit(msg)

def remove_padding(s):
    try:
        null_idx = s.index('\0')
    except ValueError:
        return s

    num_null = len(s) - null_idx
    if s.endswith(num_null * '\0'):
        return s[0:null_idx]
    else:
        raise ValueError

class FPFF_Section:

    def _parse_ascii(data, length):
        ascii_bytes = data[0:length]

        try:
            return ascii_bytes.decode('ascii')
        except UnicodeDecodeError:
            fail("Bad section value! Expected ASCII-encoded text")

    def _parse_utf8(data, length):
        utf8_bytes = data[0:length]

        try:
            return utf8_bytes.decode('utf-8')
        except UnicodeDecodeError:
            fail("Bad section value! Expected UTF-8-encoded text")

    def _parse_words(data, length):
        try:
            return [elmt[0] for elmt in struct.iter_unpack('<L', data[0:length])]
        except struct.error:
            fail("Bad section value! Length must be divisible by 4 for WORDS type")

    def _parse_dwords(data, length):
        try:
            return [elmt[0] for elmt in struct.iter_unpack('<Q', data[0:length])]
        except struct.error:
            fail("Bad section value! Length must be divisible by 8 for DWORDS type")

    def _parse_doubles(data, length):
        try:
            return [elmt[0] for elmt in struct.iter_unpack('<d', data[0:length])]
        except struct.error:
            fail("Bad section value! Length must be divisible by 8 for DOUBLES type")

    def _parse_coord(data, length):
        try:
            return struct.unpack('<dd', data[0:length])
        except struct.error:
            fail("Bad section value! Length must be 16 for COORD type")

    def _parse_reference(data, length):
        try:
            struct.unpack('<L', data[0:length])
        except struct.error:
            fail("Bad section value! Length must be 4 for REFERENCE type")

    def _parse_png(data, length):
        return b'\211PNG\r\n\032\n' + data[0:length]

    def _parse_gif87(data, length):
        return b'GIF87a' + data[0:length]

    def _parse_gif89(data, length):
        return b'GIF89a' + data[0:length]

    SECTION_ASCII = 0x1     # ASCII-encoded text (https://en.wikipedia.org/wiki/ASCII)
    SECTION_UTF8 = 0x2      # UTF-8-encoded text (https://en.wikipedia.org/wiki/UTF-8)
    SECTION_WORDS = 0x3     # Array of words.
    SECTION_DWORDS = 0x4    # Array of dwords.
    SECTION_DOUBLES = 0x5   # Array of doubles.
    SECTION_COORD = 0x6     # (Latitude, longitude) tuple of doubles.
    SECTION_REFERENCE = 0x7 # The index of another section.
    SECTION_PNG = 0x8       # Embedded PNG image.
    SECTION_GIF87 = 0x9     # Embedded GIF87.
    SECTION_GIF89 = 0xA     # Embedded GIF89.

    PARSE_BY_TYPE = {
        SECTION_ASCII: _parse_ascii,
        SECTION_UTF8: _parse_utf8,
        SECTION_WORDS: _parse_words,
        SECTION_DWORDS: _parse_dwords,
        SECTION_DOUBLES: _parse_doubles,
        SECTION_COORD: _parse_coord,
        SECTION_REFERENCE: _parse_reference,
        SECTION_PNG: _parse_png,
        SECTION_GIF87: _parse_gif87,
        SECTION_GIF89: _parse_gif89
    }

    def __init__(self, data, num_sections):

        # Unpack section data
        (self.stype,
         self.slen) = struct.unpack_from("<LL", data)

        # Validate and parse type
        offset = 2 * WORD_SIZE
        try:
            self.svalue = self.PARSE_BY_TYPE[self.stype](data[offset:], self.slen)
        except KeyError:
            fail("Bad section type! Got %s, "
                 "expected value between 0x1 and 0xA, inclusive" % (hex(magic)))

        if self.stype == self.SECTION_REFERENCE and self.svalue >= num_sections:
            fail("Bad section value! Value for REFERENCE must be in the range [0, nsects - 1]")

    def size(self):
        return self.slen + 2 * WORD_SIZE

    def type_str(self):
        name = {
            self.SECTION_ASCII: 'SECTION_ASCII',
            self.SECTION_UTF8: 'SECTION_UTF8',
            self.SECTION_WORDS: 'SECTION_WORDS',
            self.SECTION_DWORDS: 'SECTION_DWORDS',
            self.SECTION_DOUBLES: 'SECTION_DOUBLES',
            self.SECTION_COORD: 'SECTION_COORD',
            self.SECTION_REFERENCE: 'SECTION_REFERENCE',
            self.SECTION_PNG: 'SECTION_PNG',
            self.SECTION_GIF87: 'SECTION_GIF87',
            self.SECTION_GIF89: 'SECTION_GIF89'
        }
        return name[self.stype]

class FPFF:

    HEADER_SIZE = 4 * WORD_SIZE + 8

    def __init__(self, data):

        # Unpack header data
        (self.magic,
         self.version,
         self.timestamp,
         author_bytes,
         self.section_count) = struct.unpack_from("<LLl8sL", data)

        # Validate header
        if self.magic != MAGIC:
            fail("Bad magic! Got %s, expected %s" % (hex(magic), hex(MAGIC)))

        if self.version != VERSION:
            fail("Bad version! Got %d, expected %d" % (int(version), int(VERSION)))

        try:
            self.author = remove_padding(author_bytes.decode('ascii'))
        except UnicodeDecodeError:
            fail("Bad author! Expected ASCII-encoded string")
        except ValueError:
            fail("Bad author! String is not properly padded")

        if self.section_count == 0:
            fail("Bad section count! Got %d, expected value >0" % (int(self.section_count)))

        self.sections = self.section_count * [None]

        offset = self.HEADER_SIZE
        for i in range(0, self.section_count):
            self.sections[i] = FPFF_Section(data[offset:], self.section_count)
            offset += self.sections[i].size()

def write_image(suffix, data):
    with tempfile.NamedTemporaryFile(suffix=suffix,
                                     prefix='image_',
                                     dir=os.getcwd(),
                                     delete=False) as tmpfile:
        tmpfile.file.write(data)
        return tmpfile.name

if len(sys.argv) < 2:
    sys.exit("Usage: python3 fpff.py input_file.fpff")

# Open file to parse
with open(sys.argv[1], 'rb') as file:
    data = file.read()

data = FPFF(data)

print("------- HEADER -------")
print("MAGIC: %s" % hex(data.magic))
print("VERSION: %d" % int(data.version))
utc_time = datetime.utcfromtimestamp(data.timestamp)
print("TIMESTAMP: %s" % utc_time.strftime("%b. %d, %Y %H:%M:%S.%f+00:00 (UTC)"))
print("AUTHOR: %s" % data.author)
print("SECTION COUNT: %d" % int(data.section_count))

print("")
print("-------  BODY  -------")
for i, section in enumerate(data.sections):
    print("Section %d:" % int(i + 1))
    print("Type: %s" % section.type_str())
    print("Data: ", end="")
    if (section.stype == FPFF_Section.SECTION_ASCII or
        section.stype == FPFF_Section.SECTION_UTF8):
        print("'%s'" % section.svalue)
    elif section.stype == FPFF_Section.SECTION_PNG:
        filename = write_image('.png', section.svalue)
        print("Image written to %s" % filename)
    elif section.stype == FPFF_Section.SECTION_GIF87:
        filename = write_image('.gif', section.svalue)
        print("Image written to %s" % filename)
    elif section.stype == FPFF_Section.SECTION_GIF89:
        filename = write_image('.gif', section.svalue)
        print("Image written to %s" % filename)
    else:
        print(section.svalue)
    print("")
