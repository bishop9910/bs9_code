"""Round-trip tests for the bs9 library.

Run with:  python tests/test_roundtrip.py   (from the project root)
"""

from __future__ import annotations

import os
import shutil
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "_selftest")
sys.path.insert(0, ROOT)

import bs9
from bs9 import default_codec


class CodecTests(unittest.TestCase):
    def test_roundtrip(self):
        samples = [
            "Hello, World! 12345",
            "<h1>Test</h1>",
            "中文。",
            "abc XYZ 0987 \n\t",
            '"quote" and backslash \\ and {braces}',
            "chars: ~`!@#$%^&*()_+-=[]{}|;:,.<>?/'",
        ]
        for s in samples:
            with self.subTest(s=s):
                self.assertEqual(default_codec.decode(default_codec.encode(s)), s)

    def test_known_chars_are_two_digit_codes(self):
        encoded = default_codec.encode("Hello")
        self.assertTrue(encoded.isdigit())
        self.assertEqual(len(encoded), 10)


class HeaderTests(unittest.TestCase):
    def test_make_and_parse(self):
        for kind in ("bs9", "bs9pck"):
            for _ in range(50):
                raw = bs9.make_header(kind)
                self.assertEqual(len(raw), bs9.HEADER_SIZE)
                header = bs9.parse_header(raw)
                self.assertEqual(header.file_type, kind)
                self.assertEqual(header.version, bs9.VERSION)
                self.assertGreater(header.xor_key, 0)


class FileRoundtripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.isdir(WORK):
            shutil.rmtree(WORK)
        os.makedirs(WORK)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(WORK, ignore_errors=True)

    def _roundtrip(self, filename, content, suffix):
        path = os.path.join(WORK, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        encoded = bs9.encode_file(path)
        self.assertTrue(encoded.endswith(".bs9"))
        decoded = bs9.decode_file(encoded)
        self.assertTrue(decoded.endswith(suffix))

        with open(decoded, encoding="utf-8") as f:
            self.assertEqual(f.read(), content)

    def test_simple_txt(self):
        self._roundtrip("hello.txt", "Hello bs9! 中文 fallback。\nSecond line.", ".txt")

    def test_multiple_dots(self):
        self._roundtrip("archive.tar.txt", "file with dots in name", ".txt")

    def test_html(self):
        self._roundtrip("index.html", "<!doctype html><h1>Hi</h1>", ".html")


class PackRoundtripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.isdir(WORK):
            shutil.rmtree(WORK)
        os.makedirs(WORK)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(WORK, ignore_errors=True)

    def test_normal_folder(self):
        folder = os.path.join(WORK, "my.site")
        os.makedirs(os.path.join(folder, "sub"))

        # NOTE: no index.html/index.htm here, so this stays a *normal* folder.
        payloads = {
            os.path.join(folder, "about.html"): "<html>about</html>",
            os.path.join(folder, "style.css"): "body { color: red; }",
            os.path.join(folder, "sub", "data.txt"): "nested text 中文。",
        }
        for p, content in payloads.items():
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
        # A binary (non-text) file must pass through unchanged.
        bin_path = os.path.join(folder, "blob.bin")
        with open(bin_path, "wb") as f:
            f.write(bytes(range(256)))

        archive = bs9.pack(folder)  # remove_source=True by default
        self.assertTrue(archive.endswith(".bs9pck"))
        self.assertFalse(os.path.isdir(folder))  # source deleted

        restored = bs9.unpack(archive)  # removes the archive by default
        self.assertTrue(os.path.isdir(restored))

        for p, content in payloads.items():
            rel = os.path.relpath(p, folder)
            with open(os.path.join(restored, rel), encoding="utf-8") as f:
                self.assertEqual(f.read(), content)

        with open(os.path.join(restored, "blob.bin"), "rb") as f:
            self.assertEqual(f.read(), bytes(range(256)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
