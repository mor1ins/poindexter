#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from fpdf import FPDF
from Abstructions.Generator import IGenerator
from os.path import isfile, join
import os

from dependency import logable


def is_done_for_gen(pdf):
    return pdf is not None


class PdfGenerator(IGenerator):
    @logable(before="PdfGenerator: generating pdf...",
             after="PdfGenerator: generated",
             pred=is_done_for_gen,
             error_message="PdfGenerator: path is not ready for generate")
    def generate(self, dir, title):
        photos = [dir % ("%s/%s" % (title, photo))
                  for photo in os.listdir(dir % title)
                  if isfile(join(dir % title, photo))]

        if len(photos) == 0:
            return None

        pdf = FPDF()
        for image in photos:
            pdf.add_page()
            file = Image.open(image)
            box = file.getbbox()
            pdf.image(image, x=box[0], y=box[1], w=pdf.w, h=pdf.h)
        pdf.output(dir % ("%s.%s" % ("note_pdf", "pdf")), "F")
        return pdf
