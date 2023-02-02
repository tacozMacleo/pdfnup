#!/bin/env/python
# -*- coding: utf-8 -*-

"Tests for pdfnup module."


import os
import math
import unittest
import io

try:
    from pypdf import PdfReader as PdfFileReader
    from pypdf import PdfWriter as PdfFileWriter
except ImportError:
    _MSG = "Please install pyPdf first, see http://pybrary.net/pyPdf"
    raise RuntimeError(_MSG)

from pdfnup import generateNup


def group(seq, groupLen=None):
    """Group a sequence ino a list of seqences of some length".
    
    e.g. group(range(10), 2) -> [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
    """
    
    if groupLen is None:
        groupLen = len(seq)
    
    res = [seq[i:i+groupLen] for i in range(0, len(seq), groupLen)]
    
    return res
    

class LayoutingTests(unittest.TestCase):
    "Test layouting with a square or half square number of pages per sheet."

    # all tests using filename input and output documents
    
    def test0(self):
        "Test generating several 'n-up' docs, n = m**2..."

        for path0 in ("samples/test-a4-l.pdf", "samples/test-a4-p.pdf"):
            for n in (4, 9, 16):
                outName = os.path.splitext(path0)[0] + "-%dup.pdf" % n
                path1 = os.path.join(".", outName)
                generateNup(path0, n, path1, verbose=False)  # , dirs="UL")
    
                # assert output has correct number of pages
                with open(path0, "rb") as file:
                    input = PdfFileReader(file)
                    np0 = len(input.pages)
                with open(path1, "rb") as file:
                    input = PdfFileReader(file)
                    np1 = len(input.pages)
                    self.assertEqual(np1, math.ceil(np0 / float(n)))
        
                    # assert output page(s) has/have correct text content
                    for pn in range(np1):
                        page = input.pages[pn]
                        text = page.extract_text().split()
                        exp = group([str(num) for num in range(np0)], n)[pn]
                        self.assertEqual(text, exp)

    def test1(self):
        "Test generating several 'n-up' docs, n = (m**2) / 2..."

        for path0 in ("samples/test-a4-l.pdf", "samples/test-a4-p.pdf"):
            for n in (2, 8, 18):
                outName = os.path.splitext(path0)[0] + "-%dup.pdf" % n
                path1 = os.path.join(".", outName)
                generateNup(path0, n, path1, verbose=False)  # , dirs="UL")
    
                # assert output has correct number of pages
                with open(path0, "rb") as file:
                    input = PdfFileReader(file)
                    np0 = len(input.pages)
                with open(path1, "rb") as file:
                    input = PdfFileReader(file)
                    np1 = len(input.pages)
                    self.assertEqual(np1, math.ceil(np0 / float(n)))
        
                    # assert output page(s) has/have correct text content
                    for pn in range(np1):
                        page = input.pages[pn]
                        text = page.extract_text().split()
                        exp = group([str(num) for num in range(np0)], n)[pn]
                        self.assertEqual(text, exp)

    def test2(self):
        "Test generating several 'n-up' docs in 'legal' format."
        
        # minipages are squeezed, i.e. they lose their original page ratio...
        # needs to be addressed later...

        for path0 in ("samples/test-legal-p.pdf",):
            for n in (2, 4, 8, 9):
                outName = os.path.splitext(path0)[0] + "-%dup.pdf" % n
                path1 = os.path.join(".", outName)
                generateNup(path0, n, path1, verbose=False)  # , dirs="UL")
    
                # assert output has correct number of pages
                with open(path0, "rb") as file:
                    input = PdfFileReader(file)
                    np0 = len(input.pages)
                with open(path1, "rb") as file:
                    input = PdfFileReader(file)
                    np1 = len(input.pages)
                    self.assertEqual(np1, math.ceil(np0 / float(n)))
        
                    # assert output page(s) has/have correct text content
                    for pn in range(np1):
                        page = input.pages[pn]
                        text = page.extract_text().split()
                        exp = group([str(num) for num in range(np0)], n)[pn]
                        self.assertEqual(text, exp)


class RotationTests(unittest.TestCase):
    "Test input documents with rotated pages."

    def test0(self):
        "Test on rotated pages in portrait format."

        output = PdfFileWriter()
        with open("samples/test-a4-p.pdf", "rb") as file:
            input1 = PdfFileReader(file)
            numPages = len(input1.pages)
            for i in range(numPages):
                p = input1.pages[i]
                p.rotate((i % 4) * 90)
                output.add_page(p)
            outPath = "samples/test-a4-pr.pdf"
            with open(outPath, "wb") as outputStream: 
                output.write(outputStream)
            for j in (2, 4, 8, 9): 
                generateNup(outPath, j, verbose=False)

    def test1(self):
        "Test on rotated pages in landscape format."

        output = PdfFileWriter()
        with open("samples/test-a4-l.pdf", "rb") as file:
            input1 = PdfFileReader(file)
            numPages = len(input1.pages)
            for i in range(numPages):
                p = input1.pages[i]
                p.rotate((i % 4) * 90)
                output.add_page(p)
            outPath = "samples/test-a4-lr.pdf"
            with open(outPath, "wb") as outputStream:
                output.write(outputStream)
            for j in (2, 4, 8, 9): 
                generateNup(outPath, j, verbose=False)


class FileLikeInputTests(unittest.TestCase):
    "Tests with file-like input documents (file or StringIO objects)."

    def test0(self):
        "Test using file input and filename output document."

        n = 4
        path0 = "samples/test-a4-l.pdf"
        with open(path0, "rb") as f:
            outName = os.path.splitext(path0)[0] + "-%dup-fromFileObj.pdf" % n
            path1 = os.path.join(".", outName)
            generateNup(f, n, path1, verbose=False)

    def test1(self):
        "Test using StringIO input and filename output document."

        n = 4
        path0 = "samples/test-a4-l.pdf"
        with open(path0, "rb") as file:
            pdfCode = file.read()
        f = io.BytesIO(pdfCode)
        outName = os.path.splitext(path0)[0] + "-%dup-fromStringIO.pdf" % n
        path1 = os.path.join(".", outName)
        generateNup(f, n, path1, verbose=False)

    def test2(self):
        "Test using StringIO input without defining an output document."

        n = 4
        path0 = "samples/test-a4-l.pdf"
        with open(path0, "rb") as file:
            pdfCode = file.read()
        f = io.BytesIO(pdfCode)
        self.assertRaises(
            AssertionError, 
            generateNup, f, n, None, verbose=False
        )

    def test3(self):
        "Test using file input without defining an output document."

        n = 4
        path0 = "samples/test-a4-l.pdf"
        with open(path0, "rb") as f:
            self.assertRaises(
                AssertionError, 
                generateNup, f, n, None, verbose=False
            )


class FileLikeOutputTests(unittest.TestCase):
    "Tests with file-like output documents (file or StringIO objects)."

    def test0(self):
        "Test using filename input and StringIO output document."

        n = 4
        path0 = "samples/test-a4-l.pdf"
        path1 = "samples/test-a4-l-toStringIO.pdf"
        output = io.BytesIO()
        generateNup(path0, n, output, verbose=False)
        output.seek(0)
        data = output.read()
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertTrue(data.rstrip().endswith(b"%%EOF"))
        with open(path1, "wb") as file:
            file.write(data)

    def test1(self):
        "Test using filename input and file output document."

        n = 4
        path0 = "samples/test-a4-l.pdf"
        path1 = "samples/test-a4-l-toFileObj.pdf"
        with open(path1, "wb") as output: 
            generateNup(path0, n, output, verbose=False)
        with open(path1, 'rb') as file:
            data = file.read()
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertTrue(data.rstrip().endswith(b"%%EOF"))


if __name__ == "__main__":
    unittest.main()
