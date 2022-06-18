# IMG2PDF

This program uses FPDF python module to bring image files together. I created a command line utility to automatically do it with lots of option. The help document explain everything about itself:

```
This program merges image files in a directory and creates a PDF file. Every image get put to a page that exact same size as itself.
        
        Usage:
            img2pdf [OPTIONS] [OUTPUT FILE]
        
        Parameters:
            -h, --help             : Print this help document and exit.
            -d, --dir [DIRECTORY]  : Set directory to work on. Default is working directory.
            -q, --quiet            : Do not print process details.
            -r, --reverse          : Reverse image order.
            -f, --force            : Overwrite to exiting PDF file.
            -i, --interactive      : Promt before overwrite.
            -D, --decline          : Do not let overwrite. Ignores --force and --interactive parameter. 
                                     This option does not return any error if file already exists.
            -e, --except           : Do not include images that have no read permission.
            -s, --selective        : Let selecting which image will be included.
            -p, --page-size [SIZE] : Fixed page size, strech photos to page.
                                     Options are: A4, A3, A5, Letter, Legal, WITDHxHEIGHT (in pt).
        
        Exit Codes:
              0 : Program done it's job successfully.
              1 : An error occurred.
              2 : Parameter fault. Please check your command.
              3 : No valid image file in directory.
              4 : User declined overwrite.
              5 : File exist and overwrite not allowed. 
            126 : File permission denied. Check file permissions.
            130 : Process terminated by user.
```

# Installation

You can install the program via install.sh file. The script will ask you what version you want to install: binary package or source code version. Source code version needs some dependencies. Install modules below to be able to use this version.

**Required packages:**

* fpdf
* magic
* pillow

```sh
pip3 install fpdf pillow python-magic 
```

# Planned Features

* A GTK graphical user interface.

My main reason to made this program to learn how to handle system arguments. I learned how to do. Then I can start to learn GTK over QT.
