#! /usr/bin/env python
# -*- coding: utf-8 -*-

# inkscape extension files
import inkex  # required
import simplestyle

# OS modules
import os
import sys
import cairo
from lxml import etree

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import gettext
_ = gettext.gettext

__version__ = '0.1.3'

inkex.localize()

def create_new_file(gradient_data):
    root = etree.Element("svg", nsmap=inkex.NSS)
    def_tree = etree.SubElement(root, "defs")
    for item in gradient_data:
        gradient = etree.SubElement(def_tree, item.tag, attrib=item.attrib)
        for gradient_stop in item:
            new_stop = etree.SubElement(gradient, gradient_stop.tag, attrib=gradient_stop.attrib)
    with open("../my-gradients.svg", "w") as f:
        f.write(etree.tostring(
            root, encoding="utf-8", xml_declaration=True))

def save_to_file(data):
    if os.path.exists("../my-gradients.svg"):
        previous_data = load_gradients_from_file()
        data = previous_data + data
        create_new_file(data)
    else:
        create_new_file(data)

def load_gradients_from_file():
    if os.path.exists("../my-gradients.svg"):
        with open("../my-gradients.svg", "r") as f:
            root = etree.fromstring(f.read())
        linearGradients = root.xpath("//svg:linearGradient",namespaces=inkex.NSS)
        # radialGradients = root.findall("radialGradient")
        mygradients = linearGradients
    else:
        mygradients = []
    return mygradients

class SaveGradientTemplate(Gtk.HBox):
    """
    Template for generating gradient name 
    and preview of selected object in the save page.
    """
    def __init__(self, gradient_data):
        Gtk.HBox.__init__(self)
        self.gradient_data = gradient_data
        self.set_spacing(20)
        preview = Gtk.DrawingArea()
        preview.set_size_request(150,42)
        preview.set_app_paintable(True)
        preview.connect("draw",self.on_draw, gradient_data)
        self.pack_start(preview,False,True,0)
        self.input_entry = Gtk.Entry()
        self.input_entry.set_placeholder_text("e.g Beautiful Color")
        self.input_entry.set_size_request(250,42)
        self.input_entry.set_text(gradient_data.get("id"))
        self.input_entry.set_max_length(25)
        self.pack_start(self.input_entry,False,True,1)

    def on_draw(self, wid, cr, data):
        """
        Calllback for draw signal.
        params:
            - wid :GtkWidget
            - cr :Cairo
            - data :list -> gradient data
        """
        lg = cairo.LinearGradient(0.0, 20.0, 150.0, 20.0)
        for stop in data["stops"]:
            lg.add_color_stop_rgba(stop[0] ,stop[1], stop[2], stop[3], stop[4])
        cr.rectangle(10.0, 0.0, 150.0, 42.0)
        cr.set_source(lg)
        cr.fill()
    
    def get_save_gradient_text(self):
        return self.input_entry.get_text()

    def get_compiled_gradient(self, new_id):
        # compiling gradient stops
        root = etree.Element("linearGradient", id=new_id)
        for idx,stop in enumerate(self.gradient_data["stops"]):
            stop_id = self.get_name() + str(idx)
            offset = stop[0]
            color = simplestyle.formatColor3f(stop[1], stop[2], stop[3])
            opacity = stop[4]
            tmp_stops = {
                "id" : stop_id,
                "offset" : str(offset),
                "style" : simplestyle.formatStyle({
                    "stop-color" : color,
                    "stop-opacity" : str(opacity)
                })
            }
            current_stop = etree.SubElement(root, "stop", attrib=tmp_stops)
        return root

class Handler:
    def __init__(self, gtkbuilder):
        self.builder = gtkbuilder

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onSaveGradientClicked(self, button):
        text = ""
        gradient_to_save = []
        # get all gradient data in save_container
        for item in self.builder.save_container.get_children():
            # get new gradient name
            new_name_gradient = item.get_save_gradient_text()
            # get gradient data
            gradient_data = item.get_compiled_gradient(new_name_gradient)
            text += "{0}\n-----\n".format(etree.tostring(gradient_data))
            self.builder.get_object("debug_text").set_text(text)
            gradient_to_save.append(gradient_data)
        save_to_file(gradient_to_save)

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

    def get_gradients_data(self):
        selected_objects = self.selected
        gradient_list = []
        if len(selected_objects) > 0 :
            for item in selected_objects:
                style = simplestyle.parseStyle(selected_objects.get(item).attrib['style'])
                fill = style["fill"][5:-1] if "url" in style["fill"] else "None"
                stroke = style["stroke"][5:-1] if "url" in style["stroke"] else "None"
                if fill == "None" and stroke == "None":
                    continue
                # read fill data
                if "radialGradient" in fill or "linearGradient" in fill:
                    real_fill = self.getElementById(fill).attrib["{"+inkex.NSS["xlink"]+"}href"][1:]
                    real_fill_node = self.getElementById(real_fill)
                    if real_fill_node not in gradient_list:
                        gradient_list.append(real_fill_node)
                # read stroke data
                if "radialGradient" in stroke or "linearGradient" in stroke:
                    real_stroke = self.getElementById(stroke).attrib["{"+inkex.NSS["xlink"]+"}href"][1:]
                    real_stroke_node = self.getElementById(real_stroke)
                    if real_stroke_node not in gradient_list:
                        gradient_list.append(real_stroke_node)
        data = []
        # read gradients data
        for gradient in gradient_list:
            # parse gradient stops
            stop_data = {
                "id": gradient.attrib.get("id"),
                "stops": []
            }
            for stop in gradient:
                offset = stop.attrib.get("offset")
                style = simplestyle.parseStyle(stop.attrib['style'])
                color = simplestyle.parseColor(style.get("stop-color"))
                opacity = style.get("stop-opacity")
                stop_data.get("stops").append(tuple([float(offset)] + [x/256.0 for x in color] + [float(opacity)]))
            data.append(stop_data)
        return data

    # called when the extension is run.
    def effect(self):
        class MainWindow(Gtk.Builder):
            def __init__(self, gradients):
                Gtk.Builder.__init__(self)
                self.add_from_file("GUI.glade")
                self.window = self.get_object("window")
                # parsing components
                ## save gradient components
                self.save_container = self.get_object("save_gradients_container")
                save_template = self.get_object("save_gradient1")
                self.save_container.remove(save_template)
                for idx,item in enumerate(gradients):
                    new_save_template = SaveGradientTemplate(item)
                    new_save_template.set_name("gradient%d" % idx)
                    self.save_container.add(new_save_template)
                ## - end save gradient components
                # show the GUI
                self.connect_signals(Handler(self))
                self.window.show_all()
        # if len(self.selected) > 5 or len(self.selected) <= 0:
        #     inkex.debug("Please select max 5 objects with gradient")
        #     return
        # else:
        try:
            app = MainWindow(self.get_gradients_data())
            Gtk.main()
        except Exception as e:
            import traceback
            inkex.debug(e)
            inkex.debug(traceback.print_exc())
            # for item in self.selected:
            #     style = simplestyle.parseStyle(self.selected.get(item).attrib['style'])
            #     fill = style["fill"][5:-1] if "url" in style["fill"] else "None"
            #     stroke = style["stroke"][5:-1] if "url" in style["stroke"] else "None"
            #     if fill == "None" and stroke == "None":
            #         inkex.debug("There is no gradient applied in current selected object")
            #         return
            #     # read radialgradient real data:
            #     if "radialGradient" in fill:
            #         real_fill = self.getElementById(fill).attrib["{"+inkex.NSS["xlink"]+"}href"][1:]
            #         real_fill_node = self.getElementById(real_fill)
            #         if real_fill_node not in self.gradients:
            #             self.gradients.append(real_fill_node)
            #     elif "linearGradient" in fill:
            #         fill_node = self.getElementById(fill)
            #         if fill_node not in self.gradients:
            #             self.gradients.append(fill_node)
            #     if "radialGradient" in stroke:
            #         real_stroke = self.getElementById(stroke).attrib["{"+inkex.NSS["xlink"]+"}href"][1:]
            #         real_stroke_node = self.getElementById(real_stroke_node)
            #         if real_stroke_node not in self.gradients:
            #             self.gradients.append(real_stroke_node)
            #     elif "linearGradient" in stroke:
            #         stroke_node = self.getElementById(stroke)
            #         if stroke_node not in self.gradients:
            #             self.gradients.append(stroke_node)
            # try:
            #     self.save_to_file(self.options.name, self.gradients)
            #     inkex.debug("%d gradient saved successfully!" %
            #                 len(self.gradients))
            # except Exception as e:
            #     inkex.debug(e.with_traceback())


if __name__ == '__main__':
    e = SaveGradients()
    e.affect()
