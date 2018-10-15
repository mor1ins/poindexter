#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from fpdf import FPDF
from Abstructions.Generator import IGenerator
from os.path import isfile, join
import os


class PdfGenerator(IGenerator):
    def generate(self, dir, title):
        photos = [dir % ("%s/%s" % (title, photo))
                  for photo in os.listdir(dir % title)
                  if isfile(join(dir % title, photo))]

        pdf = FPDF()
        for image in photos:
            pdf.add_page()
            file = Image.open(image)
            box = file.getbbox()
            pdf.image(image, x=box[0], y=box[1], w=pdf.w, h=pdf.h)
        pdf.output(dir % ("%s.%s" % (title, "pdf")), "F")
