# IMG2PDF

![Shell](https://shields.io/badge/Terminal-Tool-A42E2B?logo=gnubash&logoColor=white&style=for-the-badge)

This program uses FPDF python module to bring image files together. I created a
command line utility to automatically do it with lots of option. The help
document explain everything about itself:

```
This program merges image files in a directory and creates a PDF file. Every
image get put to a page that exact same size as itself.

        Usage:
            img2pdf [OPTIONS] [OUTPUT FILE]

        Parameters:
            -h, --help             : Print this help document and exit.
            -d, --dir [DIRECTORY]  : Set directory to work on. Default is
                                     working directory.
            -q, --quiet            : Do not print process details.
            -r, --reverse          : Reverse image order.
            -n, --negative         : Invert colors of images. May be useful to
                                     make black & white documents dark.
            -g, --grayscale        : Make colors shades of gray.
            -f, --force            : Overwrite to existing PDF file.
            -i, --interactive      : Prompt before overwrite.
            -D, --decline          : Do not let overwrite. Ignores --force and
                                     --interactive parameter. This option does
                                     not return any error if file already exists.
            -e, --except           : Do not include images that have no read
                                     permission.
            -s, --selective        : Let selecting which image will be
                                     included.
            -S, --sort-by [METHOD] : Set sorting method. available methods are:
                                     name (default), m_time (modification time),
                                     c_time (change time).
            -p, --page-size [SIZE] : Fixed page size, strech photos to page.
                                     Options are: A4, A3, A5, Letter, Legal,
                                     WITDHxHEIGHT (in pt).
            -L, --landscape        : Rotate images to landscape. (Do not change if
                                     already is.)
            -P, --portrait         : Rotate images to portrait. (Do not change if
                                     already is.)

        Exit Codes:
              0 : Program done it's job successfully.
              1 : An error occurred.
              2 : Parameter fault. Please check your command.
              3 : No valid image file in directory.
              4 : User declined overwrite.
              5 : File exist and overwrite not allowed.
              6 : Directory does not exist.
            126 : File permission denied. Check file permissions.
            130 : Process terminated by user.
```
