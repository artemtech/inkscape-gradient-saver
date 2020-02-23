#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# inkscape extension files
import inkex  # required
import simplestyle

# OS modules
import os
import sys
from lxml import etree
__version__ = '0.1'

inkex.localize()

def create_new_file(name,data):
    root = etree.Element("svg", nsmap=inkex.NSS)
    def_tree = etree.SubElement(root, "defs")
    for idx,item in enumerate(data):
        # parse gradient stops
        if idx == len(data) - 1 :
            gradient = etree.SubElement(def_tree, item.tag, attrib=item.attrib, id=name)
        else:
            gradient = etree.SubElement(def_tree, item.tag, attrib=item.attrib)
        for gradient_stop in item:
            new_stop = etree.SubElement(gradient,gradient_stop.tag, attrib=gradient_stop.attrib)
    with open("my-gradients.svg", "w") as f:
        f.write(etree.tostring(
            root, encoding="utf-8", xml_declaration=True))

class SaveGradients(inkex.Effect):
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self)  # initialize the super class
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')
        self.gradients = []
        self.OptionParser.add_option("-n", "--name",
                                     action="store", type="string",
                                     dest="name",
                                     help="Name for this Gradient")

    def save_to_file(self, name, data):
        if os.path.exists("my-gradients.svg"):
            previous_data = self.load_gradients_from_file()
            data = previous_data + data
            create_new_file(name,data)
        else:
            create_new_file(name,data)

    def load_gradients_from_file(self):
        if os.path.exists("my-gradients.svg"):
            with open("my-gradients.svg", "r") as f:
                root = etree.fromstring(f.read())
            linearGradients = root.xpath("//svg:linearGradient",namespaces=inkex.NSS)
            # radialGradients = root.findall("radialGradient")
            mygradients = linearGradients
        else:
            mygradients = []
        return mygradients

    # called when the extension is run.
    def effect(self):
        if len(self.selected) > 1 or len(self.selected) <= 0:
            inkex.debug("Please select only 1 object with gradient")
            return
        else:
            for item in self.selected:
                style = simplestyle.parseStyle(self.selected.get(item).attrib['style'])
                fill = style["fill"][5:-1] if "url" in style["fill"] else "None"
                stroke = style["stroke"][5:-1] if "url" in style["stroke"] else "None"
                if fill == "None" and stroke == "None":
                    inkex.debug("There is no gradient applied in current selected object")
                    return
                # read radialgradient real data:
                if "radialGradient" in fill:
                    real_fill = self.getElementById(fill).attrib["{"+inkex.NSS["xlink"]+"}href"][1:]
                    real_fill_node = self.getElementById(real_fill)
                    if real_fill_node not in self.gradients:
                        self.gradients.append(real_fill_node)
                elif "linearGradient" in fill:
                    fill_node = self.getElementById(fill)
                    if fill_node not in self.gradients:
                        self.gradients.append(fill_node)
                if "radialGradient" in stroke:
                    real_stroke = self.getElementById(stroke).attrib["{"+inkex.NSS["xlink"]+"}href"][1:]
                    real_stroke_node = self.getElementById(real_stroke_node)
                    if real_stroke_node not in self.gradients:
                        self.gradients.append(real_stroke_node)
                elif "linearGradient" in stroke:
                    stroke_node = self.getElementById(stroke)
                    if stroke_node not in self.gradients:
                        self.gradients.append(stroke_node)
            try:
                self.save_to_file(self.options.name, self.gradients)
                inkex.debug("%d gradient saved successfully!" %
                            len(self.gradients))
            except Exception as e:
                inkex.debug(e.with_traceback())


if __name__ == '__main__':
    e = SaveGradients()
    e.affect()
