#!/usr/bin/env sh
if [ "$EUID" -ne 0 ]; then 
  echo "Please run under root privileges."
else
  while true; do
    printf "\033[93mWhich version you want to install?\033[00m
\033[96m[1]\033[00m binary package (no dependency)
\033[96m[2]\033[00m source code version (dependencies required)
: "; read
    if [ ${REPLY} == "1" ]; then
      echo Binary package selected.
      chmod +x img2pdf
      cp -v img2pdf /usr/bin/img2pdf
      break
    elif [ ${REPLY} == "2" ]; then
      echo Open source file selected.
      chmod +x img2pdf.py
      cp -v img2pdf.py /usr/bin/img2pdf
      break
    else
      echo Select 1 or 2.
    fi
  done
  if [ -f "/usr/bin/img2pdf" ]; then
    printf "\033[92mInstallation has been completed.\033[00m\n"
  else
    printf "\033[91mCannot complete installation.\033[00m\n"
  fi
fi
