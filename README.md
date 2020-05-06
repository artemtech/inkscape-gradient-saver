<p align="center" class="has-mb-6">
<img class="not-gallery-item" height="128" src="/gradient_saver/icon.svg" alt="logo">
<br><b>Gradient Saver</b></br>
<br>
Inkscape Gradient Manager for Your Next Project!
<br>

# Gradient Saver

An extension that will help you to organize your gradient on Inkscape. By using Gradient Saver you have ability to save your favorite gradient and reuse it on your next project. Hope it will help much Inkscpae user out there.

## BIG DISCLAIMER

This version only works on Inkscape 1.0 and later. Previous version of Inkscape (< 1.0) please use inkscape-0.9x branch

## Dependencies

(Tested in Inkscape 1.0 - ArchLinux)

- ArchLinux  
  `pacman -S python3-lxml python3-gobject python3-cairo`
- Debian/Ubuntu  
  `apt install python-lxml python-gi python-cairo python-gi-cairo`
  for some case you should use python3-* instead python-* 
- openSUSE (tested in Tumbleweed)  
  `zypper in python2-lxml python2-gobject-Gdk python2-gobject-cairo python2-gobject python2-pycairo typelib-1_0-Gtk-3_0`  

Inkscape 1.0 is using python3 libs. So, please install python3 version of libraries listed above.

## How to Install

Copy `gradient_saver.inx` and `gradient_saver` folder into Inkscape `extensions` folder,  
usually in `$HOME/.config/inkscape/extensions` for linux.

Unable to find where is the `extensions` folder for your Inkscape installation?  
you can check it from `Edit > Preferences > System` menu, then look at `User extensions` path in `System Info` section.

## How to Use

- Open Inkscape
- Go to `Extension > Gradient Saver` menu
- Follow the instructions on `Hints`

## Status

- [x] Saving Gradient
- [x] Load Gradient 
- [x] Remove Gradient

## Contributor

- [Sofyan Sugianto - sofyan@artemtech.id](mailto://sofyan@artemtech.id) (Programmer)
- [Rania Amina - me@raniaamina.id ](https://raniaamina.id) (UI Designer)
- [Hadiid Pratama - hddpratama@gmail.com](mailto://hddpratama@gmail.com) (Logo Contributor)

This project fully supported by Gimpscape Indoensia (The Biggest Indonesia F/LOSS Design Community)

## Disclaimer & Donation

This is early development extension. We don't guarantee anything about this extension so please use at your own risk. If you feel helped by this extension, of course you can give us a cup of coffee :")
