#!/usr/bin/env python3
from os import listdir, access, W_OK, F_OK, R_OK, path, getcwd, remove
from sys import argv, exit
from tempfile import gettempdir
from getopt import getopt, GetoptError
from PIL import Image, ImageChops
from fpdf import FPDF
from magic import Magic

def main():
    try:

        # Define color prints
        def red_text(text): return f"\033[91m{text}\033[00m"
        def green_text(text): return f"\033[92m{text}\033[00m"
        def yellow_text(text): return f"\033[93m{text}\033[00m"
        def blue_text(text): return f"\033[96m{text}\033[00m"

        # Get command line arguments
        try:
            opts, args = getopt(argv[1:], "hd:qrfDiesp:nLPgS:", ["help", "dir=", "quiet", "reverse",
                                "force", "decline", "interactive", "except", "selective",
                                "page-size=", "negative","landscape","portrait","grayscale",
                                "sort-by="])
        except GetoptError as err:
            print(err)
            exit(2)
        opts = dict((opt[0], opt[1]) for opt in opts)
        optk = opts.keys()

        # Print help dialog and exit
        if "-h" in optk or "--help" in optk:
            print("""This program merges image files in a directory and creates a PDF file. Every
image get put to a page that exact same size as itself.

        Usage:
            img2pdf+ [OPTIONS] [OUTPUT FILE]

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
              7 : Undedined parameter argument.
            126 : File permission denied. Check file permissions.
            130 : Process terminated by user.
""")
            exit(0)

        # Check for arguments
        if len(args) == 0:
            print(red_text("img2pdf: Error: Please specify output file."))
            exit(2)

        if len(args) == 1:

            # Required objects and directory
            pdf = FPDF(unit="pt")
            mime = Magic(mime=True)
            directory = opts["-d"] if "-d" in optk else (
                opts["--dir"] if "--dir" in optk else getcwd())
            directory = directory+("" if directory.endswith("/") else "/")

            # Required pre-defined variables
            height = 0
            width = 0

            if len(args) == 1:

                # Get output file name.
                file_name = directory + \
                    args[0]+("" if args[0].endswith(".pdf") else ".pdf")

                # Check for existing files
                if access(file_name, F_OK):

                    # Get Modification time to use in process validation
                    modification_time = path.getmtime(file_name)

                    # Check for file permission
                    if not access(file_name, W_OK):
                        print(red_text( f"img2pdf: Permission Denied: The file '{file_name}' is not writable. Check file permissions."))
                        exit(126)

                    # Check if forced
                    if "-f" not in optk and "--force" not in optk:

                        # Check if declined
                        if "-D" in optk or "--decline" in optk:
                            print(blue_text("img2pdf: Quit: Forced to decline overwrite."))
                            exit(0)

                        # Check if interactive
                        elif "-i" in optk or "--interactive" in optk:
                            if input(yellow_text("img2pdf: Prompt: File is already exists. Do you want to overwrite? [y/N]: ")).lower() not in ("y", "yes"):
                                print(red_text("img2pdf: Quit: User declined overwrite."))
                                exit(4)
                        else:
                            print(red_text("img2pdf: Quit: File already exists. To overwrite add -f or --force parameter."))
                            exit(5)

                # If file not exists create a fake modification time
                else:
                    modification_time = 0

                # Get image Files
                try:
                    all_files = listdir(directory)
                # Exit if directory not found
                except FileNotFoundError:
                    print(red_text("img2pdf: Warning: Directory does not exists."))
                    exit(6)
                all_files.sort()
                images = []

                # Check for selective
                selective = "-s" in optk or "--selective" in optk
                negative = "-n" in optk or "--negative" in optk
                grayscale = "-g" in optk or "--grayscale" in optk

                # Print if negative selected
                if negative:
                    print(blue_text("Color invert mode activated."))

                # Print if graycale selected
                if grayscale:
                    print(blue_text("Grayscale mode activated."))

                # Get image files
                for file in all_files:

                    # Check for read permission
                    if access(directory+file, R_OK):

                        # Be sure element is not directory
                        if path.isfile(directory+file):

                            # Check if file is image by it's mimetype
                            if "image/" in mime.from_file(directory+file):

                                # Invert color if negative
                                if negative:
                                    tmp = gettempdir()+"/negative-{}"
                                    ImageChops.invert(Image.open(directory+file).convert('RGB')).save(tmp.format(file))

                                # Grayscale images if selected
                                if grayscale:
                                    tmpg = gettempdir()+"/grayscale-{}"
                                    Image.open(tmp.format(file) if negative else directory+file).convert('L').save(tmpg.format(file))
                                    tmp=tmpg

                                # Select items if selective
                                if selective:
                                    if input(blue_text(f"Include \"{file}\"? [Y/n]: ")).lower() in ("y", "yes", ""):

                                        images.append(tmp.format(file) if negative or grayscale else (directory+file))
                                        print(green_text(f"  {file} will be add."))
                                    else:
                                        print(red_text(f"  {file} will be pass."))
                                else:
                                    images.append(tmp.format(file) if negative or grayscale else (directory+file))
                        else:
                            continue
                    elif "-e" in optk or "--except" in optk:
                        continue
                    else:
                        print(red_text(f"img2pdf: Permission Denied: The file '{file}' is not readable. Check file permissions or pass -e parameter to not include it."))
                        exit(126)

                # Count images
                image_count = len(images)
                image_count_digits = len(str(image_count))

                # There is no image
                if image_count == 0:
                    print(red_text("img2pdf: Error: There is no valid image file to work with."))
                    exit(3)

                # Check for sort algorythm
                sort_by = ""
                if "-S" in optk:
                    sort_by = opts["-S"].lower()
                if "--sort_by" in optk:
                    sort_by = opts["--sort-by"].lower()

                # Pass default method
                if sort_by == "name":
                    print(blue_text("Using default name methot for sorting."))

                # Sort by modification time
                elif sort_by == "m_time":
                    print(blue_text("Using modification time for sorting."))
                    images.sort(key=path.getmtime)

                # Sort by modification time
                elif sort_by == "c_time":
                    print(blue_text("Using change time for sorting."))
                    images.sort(key=path.getctime)

                # In other cases throw an arror and exit
                elif sort_by:
                    print(red_text(f"img2pdf: {sort_by} is not a valid sorting method."))
                    exit(7)

                # Check for reverse
                if "-r" in optk or "--reverse" in optk:
                    images.reverse()
                    print(blue_text("Image order reversed."))

                # Check for page size
                page_size = ""
                if "-p" in optk:
                    page_size = opts["-p"].lower()
                if "--page-size" in optk:
                    page_size = opts["--page-size"].lower()

                # Check for standard page sizes
                if page_size == "a3":
                    print(blue_text("Page size set to A3."))
                    width, height = 842, 1191
                elif page_size == "a4":
                    print(blue_text("Page size set to A4."))
                    width, height = 595, 842
                elif page_size == "a5":
                    print(blue_text("Page size set to A5."))
                    width, height = 420, 595
                elif page_size == "letter":
                    print(blue_text("Page size set to Letter."))
                    width, height = 612, 792
                elif page_size == "legal":
                    print(blue_text("Page size set to Legal."))
                    width, height = 612, 1008

                # Check manual dimensions
                elif "x" in page_size and not page_size.startswith("x") and not page_size.endswith("x"):
                    dimensions = page_size.split("x")
                    if len(dimensions) == 2:

                        # Get width
                        try:
                            width = int(dimensions[0])
                        except:
                            print(red_text(f"img2pdf: Invalid Argument: Width parameter which is {dimensions[0]} must be an integer."))
                            exit(2)

                        # Get height
                        try:
                            height = int(dimensions[1])
                        except:
                            print(red_text(f"img2pdf: Invalid Argument: Height parameter which is {dimensions[1]} must be an integer."))
                            exit(2)
                    else:
                        print(red_text("img2pdf: Invalid Argument: --page-size parameter must be integers connected with \"x\"."))
                        exit(2)
                    page_size = "user_defined"
                    print(blue_text(f"Page size set to {width}x{height}"))

                # Check for unvalid page sizes.
                elif page_size != "":
                    print(red_text(f"img2pdf: Invalid Argument: --page-size parameter which is \"{page_size}\" can only take this parameters: ") + blue_text(
                        "A3, A4, A5, Letter, Legal, WIDTHxHEIGHT (in pt)."))
                    exit(2)
                else:
                    print(blue_text("Every image will be placed a page that fits their size."))

                # After getting sizes, check for orientation rules
                landscape = "-L" in optk or "--landscape" in optk
                portrait = "-P" in optk or "--portrait" in optk

                # Define a function to change orientation
                def setOrientation():
                    global height, width
                    if landscape and height>width: width,height=height,width
                    if portrait and height<width: height,width=width,height

                # Set once for fixed sizes
                setOrientation()

                # Finally start job
                for number, image in enumerate(images):

                    # Check if user defined fixed size
                    if page_size:
                        pdf.add_page(format=(width, height))

                    # Else use dimensions by image
                    elif not page_size:
                        width, height = Image.open(image).size
                        setOrientation()
                        pdf.add_page(format = (width, height))

                    # Add image to recently created page
                    pdf.image(image, 0, 0, width, height)

                    # Check if quiet
                    if "-q" not in optk and "--quiet" not in optk:
                        print(f"{str(number+1).rjust(image_count_digits)}/{image_count}: Adding image {image}")

                # Write PDF
                pdf.output(file_name)

                # Clear temporary Files
                if negative:
                    for image in images:
                        remove(image)

                # Check if it really done
                if access(file_name, F_OK):
                    if path.getmtime(file_name) != modification_time:
                        print(green_text("img2pdf: Success: PDF file created."))
                        exit(0)
                    else:
                        print(red_text("img2pdf: Error: And error occured. Could not modify the existed file."))
                        exit(1)
                else:
                    print(red_text("img2pdf: Error: An error occurred. Could not create the PDF."))
                    exit(1)

        # Wrong argument count
        else:
            print(red_text("img2pdf: Error: Please give only one parameter to specify output file."))
            exit(2)

        # Unexpected Errors
        print(red_text("img2pdf: Error: An unexpected error occurred. Please contact with developer if you can recognize the problem."))
        exit(1)

    # Handle Control+C interruption
    except KeyboardInterrupt:
        print(red_text('\nimg2pdf: Quit: Process terminated by user.'))
        exit(130)

if __name__ == "__main__":
    main()
