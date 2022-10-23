name="img2pdf-bin"
version=1.0
release=1
desc="Merge images into one pdf file via command line. "
homepage="https://github.com/Elagoht/img2pdf"
architectures=("amd64")
license="GPLv3"
provides="img2pdf"
sources_amd64="https://github.com/Elagoht/img2pdf/raw/main/img2pdf"
checksums_amd64="c24ae6a3363b1a937a7e31b3431f5b28ac30100ca0ac46cc3899ca652b11b90e"

version() {
    printf "$version"
}
package() {
    install -d "$pkgdir/usr/bin/"
    install -Dm755 "img2pdf" -t "$pkgdir/usr/bin/"
}
