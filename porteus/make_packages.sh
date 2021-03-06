#!/bin/bash

SLACKWARE_MIRROR="http://carroll.cac.psu.edu/pub/linux/distributions/slackware/slackware-13.37/"
PACKAGES="/tmp/FILE_LIST"
PATCHES="/tmp/patches"
FAKEROOT="/tmp/fakeroot"

rm -rf $FAKEROOT
mkdir -p $FAKEROOT

# Download file list.
lynx -dump $SLACKWARE_MIRROR/FILE_LIST | grep '.txz$' > $PACKAGES

# Download patch list.
lynx -dump $SLACKWARE_MIRROR/patches/packages | grep '.txz$' > $PACKAGES

# For every file in the list of packages we need, see if it's in the list
# of patches.  If it is, download it.  If not, download it from the Slackware
# repository.
