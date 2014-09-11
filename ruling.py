#!/usr/bin/python
# vim: set fileencoding=utf-8 tabstop=4 expandtab listchars=tab\:>- list:

import argparse
import math
import os
import shlex

# We know some glyphs are missing, suppress warnings
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A6, A5, A4, A3, A2, A1, A0, LETTER, LEGAL
from reportlab.lib.colors import toColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont

__VERSION__ = "1.0"

 
page_sizes = {
    "A6" : A6, "a6" : A6,
    "A5" : A5, "a5" : A5,
    "A4" : A4, "a4" : A4,
    "A3" : A3, "a3" : A3,
    "A2" : A2, "a2" : A2,
    "A1" : A1, "a1" : A1,
    "A0" : A0, "a0" : A0,
    "LETTER" : LETTER, "letter" : LETTER,
    "LEGAL"  : LEGAL,  "legal"  : LEGAL,
}

dash_style = {
    "solid"  : [ [], 0 ],
    "dotted" : [ 1, 1 ],
    "dash"   : [ 3, 1 ],
}


def set_dash_style(canvas, spec):
    try:
        args = dash_style[spec]
    except:
        args = map(int, spec.split("-"))

    canvas.setDash(args[0], args[1])


def draw_lines(canvas, opts, pagesize):
    ascenders = max(float(x[0]) for x in opts.rules) * opts.nib_width * mm
    descenders = -min(float(x[0]) for x in opts.rules) * opts.nib_width * mm
    line_height = ascenders + descenders

    if not opts.slants_per_line:
        for param in opts.slants:
            tantheta = math.tan(math.radians(90 - float(param[0])))
            xstep = float(param[1]) * opts.nib_width * mm
            canvas.setLineWidth(float(param[2]))
            try:
                set_dash_style(canvas, param[3])
            except:
                set_dash_style(canvas, 'solid')
            try:
                canvas.setStrokeColor(toColor(param[4]))
            except:
                canvas.setStrokeColor(toColor('black'))

            ystep = xstep * tantheta
            x = xstep
            y = pagesize[1] - ystep
            while x <= pagesize[0] and y >= 0:
                canvas.line(0, y, x, pagesize[1])
                x += xstep
                y -= ystep
            if y > 0:
                h = pagesize[0] * tantheta
                while y >= 0:
                    canvas.line(0, y, pagesize[0], y + h)
                    y -= ystep
                x = 0
                y = pagesize[0] * tantheta
                while x < pagesize[0]:
                    canvas.line(x, 0, pagesize[0], y)
                    x += xstep
                    y -= ystep
            else:
                while x <= pagesize[0]:
                    canvas.line(-y / tantheta, 0, x, pagesize[1])
                    x += xstep
                    y -= ystep
                y = pagesize[1] - (x - pagesize[0]) * tantheta
                while y > 0:
                    canvas.line(pagesize[0], y, pagesize[0] - y / tantheta, 0)
                    y -= ystep

    # Fill the top margin with the interline colour
#   canvas.saveState()
#   canvas.setFillColor(toColor(opts.gap_colour))
#   canvas.rect(0, pagesize[1], pagesize[0], -opts.top_margin * opts.nib_width * mm, stroke = 0, fill = 1)
#   canvas.restoreState()

    position = pagesize[1] - (opts.top_margin * opts.nib_width * mm);
    while position >= line_height:
        position -= ascenders

        if opts.gap_colour and opts.gap > 0:
            canvas.saveState()
            canvas.setFillColor(toColor(opts.gap_colour))
            canvas.rect(0, position - descenders, pagesize[0], -opts.gap * opts.nib_width * mm, stroke = 0, fill = 1)
            canvas.restoreState()

        for param in opts.rules:
            pos = position + float(param[0]) * opts.nib_width * mm
            canvas.setLineWidth(float(param[1]))
            try:
                set_dash_style(canvas, param[2])
            except:
                set_dash_style(canvas, 'solid')
            try:
                canvas.setStrokeColor(toColor(param[3]))
            except:
                canvas.setStrokeColor(toColor('black'))

            canvas.line(0, pos, pagesize[0], pos)

        if opts.slants_per_line:
            for param in opts.slants:
                tantheta = math.tan(math.radians(float(param[0])))
                xstep = float(param[1]) * opts.nib_width * mm
                canvas.setLineWidth(float(param[2]))
                try:
                    set_dash_style(canvas, param[3])
                except:
                    set_dash_style(canvas, 'solid')
                try:
                    canvas.setStrokeColor(toColor(param[4]))
                except:
                    canvas.setStrokeColor(toColor('black'))

                origin = (2 * opts.bar_width + opts.slant_offset * opts.nib_width) * mm
                x1 = origin - descenders * tantheta
                y1 = position - descenders
                x2 = origin + ascenders * tantheta
                y2 = position + ascenders
                while x1 < origin:
                    canvas.line(origin, y1 + (-x1 + origin) / tantheta, x2, y2)
                    x1 += xstep
                    x2 += xstep
                while x2 <= pagesize[0]:
                    canvas.line(x1, y1, x2, y2)
                    x1 += xstep
                    x2 += xstep
                while x1 < pagesize[0]:
                    canvas.line(x1, y1, pagesize[0], y2 - (x2 - pagesize[0]) / tantheta)
                    x1 += xstep
                    x2 += xstep

        canvas.setFillColor(toColor('black'))
        barpos = 0
        pos = position
        while pos < position + ascenders:
            barpos = (barpos + 1) % 2
            canvas.rect(barpos * opts.bar_width * mm, pos, opts.bar_width * mm, opts.nib_width * mm, stroke = 0, fill = 1)
            pos += opts.nib_width * mm

        barpos = 1
        pos = position
        while pos > position - descenders:
            barpos = (barpos + 1) % 2
            canvas.rect(barpos * opts.bar_width * mm, pos, opts.bar_width * mm, -opts.nib_width * mm, stroke = 0, fill = 1)
            pos -= opts.nib_width * mm

        position -= descenders + opts.gap * opts.nib_width * mm

# def draw_radial_width_markers(canvas, center, nib_width):
#     for i in range(0, int(300/nw)):
#         if i%2 == 0:
#             canvas.rect(1*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
#             canvas.rect(A4[0]-4*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
#         else:
#             canvas.rect(3*mm, i*nw*mm ,2*mm, nw*mm, stroke = 0, fill = 1)
#             canvas.rect(A4[0]-2*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)



def draw_circle_set(canvas, x, y, radius, nib_width, rules):
    """
    Draws concentric circles of the given radius. 
    """
    offset = radius
    for spec in rules:
        param = spec.split("/")
        h = float(param[0])
        canvas.circle(x, y, offset, fill = 1)
        offset -= h * nib_width * mm

    return offset

def draw_circles(canvas, nib_width, rules, gap, nrulings, top_margin, center):
    "Draws circles and separators on the page"
    partition_radius = sum((float(x.split("/")[0]) for x in rules),0.0) # Sum of the ascenders, descenders and body
    partition_radius += gap # Add the gap

    offset = nrulings * partition_radius * nib_width * mm
    
    for i in range(nrulings, 1, -1):
        # Draw gap
        canvas.setFillColorRGB(0, 0, 0, 1)
        canvas.circle(center[0], center[1], offset, fill = 1, stroke = 1)
        offset -= gap *nib_width * mm
        # Draw rules
        canvas.setFillColorRGB(1, 1, 1, 1)
        offset = draw_circle_set(canvas, center[0], center[1], offset, nib_width, rules)

    # Draw initial inner margin
    canvas.setFillColorRGB(0.5, 0.5, 0.5, 1)
    canvas.circle(center[0], center[1], offset, fill = 1, stroke = 1)


def write_title_and_credits(canvas, opts, pagesize):
    canvas.saveState()

    if pagesize[0] > pagesize[1]:
        width = pagesize[0]
        height = pagesize[1]
    else:
        width = pagesize[1]
        height = pagesize[0]
        canvas.rotate(90)
        canvas.translate(0, -pagesize[0])

    t = canvas.beginText()
    t.setFont("Times-Roman", 10)
    l = stringWidth("© Eris Associates Ltd", "Times-Roman", 10)
    t.setTextOrigin(width - l - 5*mm, height+5*mm)
    t.textOut("© Eris Associates Ltd")
    canvas.setFillColorRGB(0, 0, 0, 0.2)
    canvas.drawText(t)

    canvas.setFillColorRGB(0, 0, 0, 1)

    if opts.title:
        t = canvas.beginText()
        t.setTextOrigin(5*mm, height+5*mm)
        t.setFont("Times-Italic", 20)
        t.textOut(opts.title)
        canvas.drawText(t)

    t = canvas.beginText()
    t.setTextOrigin(5*mm, -5*mm)
    t.setFont("Times-Italic", 8)
    t.textOut(opts.subject)
    canvas.drawText(t)

    canvas.restoreState()


def main(opts):
    if opts.font and opts.font_size:
        try:
            pdfmetrics.registerFont(TTFont('myfont', opts.font))
        except:
            pdfmetrics.registerFont(TTFont('myfont', opts.font + '.ttf'))

    if opts.landscape and opts.radial:
        print("Ignoring radial for landscape mode")
        opts.radial = False

    pagesize = page_sizes[opts.pagesize]
    if opts.landscape:
        pagesize = pagesize[1], pagesize[0]

    opts.rules = [ x.split() for x in opts.rules ]
    opts.slants = [ x.split() for x in opts.slants ] if opts.slants else []

    c = canvas.Canvas(opts.output, bottomup = 1, pagesize = pagesize, cropMarks = True)
    c.setAuthor("Eris Associates Ltd")
    if opts.title:
        opts.title += " - "
    opts.title += "%smm nib"%(opts.nib_width)
    c.setTitle(opts.title)

    def subj_quote(x): return '[' + x + ']'
    opts.subject = "rules: %s"%(", ".join(map(subj_quote, (", ".join(x) for x in opts.rules))))
    if opts.slants:
        opts.subject += "  slants: %s"%(", ".join(map(subj_quote, (", ".join(x) for x in opts.slants))))
    c.setSubject(opts.subject)

    ink = toColor("black")
    c.setFillColor(ink)
    c.setStrokeColor(ink)

    if opts.font and opts.font_size:
        c.setFont('myfont', opts.font_size)

    while True:
        write_title_and_credits(c, opts, pagesize)

        if not opts.radial:
            draw_lines(c, opts, pagesize)
        else:
            x, y = pagesize
            center = (x/2.0, y/2.0)
            # draw_radial_width_markers(canvas, center, opts.nib_width)
            draw_circles(c, opts.nib_width, opts.rules, opts.gap, opts.rulings, opts.top_margin, center)

        c.showPage()

        if len(opts.letters) == 0:
            break

    c.save()


class MyArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(MyArgumentParser, self).__init__(*args, **kwargs)

    def convert_arg_line_to_args(self, line):
        for arg in shlex.split(line, comments = True):
            arg = arg.strip()
            if arg:
                yield arg


def parse_options():
    parser = MyArgumentParser(fromfile_prefix_chars = '@')

    parser.add_argument("-o", "--output", nargs = '?', type = argparse.FileType('wb'), default = sys.stdout,
                      help = "The file to write the output to. Default is stdout.")

    parser.add_argument("-t", "--title",
                      help = "A title for this ruling (usually the font name)")

    parser.add_argument("-P", "--pagesize", default = "A4",
                      help = "Size of sheet")
    parser.add_argument("-l", "--landscape", action="store_true", default = False,
                      help = "Create landscape instead of the default portrait sheet")

    parser.add_argument("-w", "--nib-width", type = float,
                      help = "Width of the nib in millimeters. Other measurements in nw are multiples of this.")
    parser.add_argument("--top-margin", default = 2, type = int,
                      help = "Top margin (in nib widths). Default is 2")

    parser.add_argument("-b", "--bar-width", type = float, default = 1,
                      help = "Width of the bar markings to be drawn on the left and right (in mm). Default 1.")

    parser.add_argument("--font",
                      help = "Font to use for example letters.")
    parser.add_argument("--font-size", type = float,
                      help = "Size of font to use for example letters.")
    parser.add_argument("--letters", default = "",
                      help = "Letters to place at the start of lines (one per line).")

    parser.add_argument("-r", "--rules", nargs= '+',
                      help = "List of partition specifications in each line of the form: <height in nw> <line width in mm>[ <style>[ <colour>]]")
    parser.add_argument("--rule", dest = "rules", action = 'append',
                      help = "Like --rules but only a single rule may be given (although --rule may be repeated as necessary).")
    parser.add_argument("-g", "--gap", type = float,
                      help = "Gap between lines (in nib widths)")
    parser.add_argument("-G", "--gap-colour",
                      help = "Colour of gap between lines. No default (i.e. transparent).")

    parser.add_argument("--slants-per-line", action="store_true", default = False,
                      help = "Whether slants are drawn within each line independently or across the entire page.")
    parser.add_argument("-S", "--slant-offset", type = float, default = 1,
                      help = "Offset of first slant lines from start of line or bar markings. Default is 1 nib width.")
    parser.add_argument("-s", "--slants", nargs = '+',
                      help = "list of slanted line specifications of the form: <deg from vert> <x separation in nw> <line width in mm>[ <style>[ <colour>]]")
    parser.add_argument("--slant", dest = "slants", action='append',
                      help = "Like --slants but only a single slant may be given (although --slant may be repeated as necessary).")

    parser.add_argument("-R", "--radial", action="store_true", default = False,
                      help = "Draw circles instead of straight lines")
    parser.add_argument("-n", "--rulings", default = 10, type=int,
                      help = "How many rulings to draw. Default is 10")

    parser.add_argument("--version", action = 'version', version = __VERSION__)
    opts = parser.parse_args()
    return (opts)

if __name__ == "__main__":
    if 'GATEWAY_INTERFACE' in os.environ:
        import cgi
#       import cgitb
#       cgitb.enable(display=0, logdir="/tmp/ruling.log")
        form = cgi.FieldStorage()
        for field in sorted(form.keys()):
            print("key ", field, ", value ", form.getvalue(field))
            try:
                opts[field].append(form.getvalue(field))
            except:
                try:
                    opts[field] = [ opts[field], form.getvalue(field) ]
                except:
                    opts[field] = form.getvalue(field)
    else:
        import sys
        opts = parse_options()
        main(opts)
