#!/bin/bash
# Exit if no argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 [VI|...]"
    echo "Error: No protocol specified."
    exit 1
fi

V=$1

# Remove existing symbolic links to ensure a clean state
echo "Removing old symbolic links (if they exist)..."
rm -f build
rm -f src/gconst.py

if [ "${V}" == "VI" ]; then
    export TARDIR=vi_build
    echo "Switching to VI protocol configuration..."

    # Create symlink for the build directory
    # ln -s past_builds/VI_build2 build
    ln -s past_builds/VI_build build
    echo "  Created symlink: build -> past_builds/VI_build"

    # Create symlink for the constants file.
    # This assumes the script is run from the 'murphi' directory.
    # The target 'VI_gconsts.py' is relative to the link's location in 'src/'.
    cd src
    ln -s VI_gconsts.py gconst.py
    cd ..
    echo "  Created symlink: src/gconst.py -> VI_gconsts.py"

    echo "Switch complete."

elif [ "${V}" == "VI_BUGGY" ]; then
    # export TARDIR=vi_build
    echo "Switching to BUGGY VI protocol configuration..."

    # Create symlink for the build directory
    # ln -s past_builds/VI_build2 build
    ln -s past_builds/VI_buggy_build build
    echo "  Created symlink: build -> past_builds/VI_buggy_build"

    # Create symlink for the constants file.
    # This assumes the script is run from the 'murphi' directory.
    # The target 'VI_gconsts.py' is relative to the link's location in 'src/'.
    cd src
    ln -s VI_buggy_gconsts.py gconst.py
    cd ..
    echo "  Created symlink: src/gconst.py -> VI_buggy_gconsts.py"

    echo "Switch complete."

elif [ "${V}" == "MSI" ]; then
    export TARDIR=msi_build
    # Create symlink for the build directory
    ln -s past_builds/MSI_build2 build
    echo "  Created symlink: build -> past_builds/MSI_build"

    # Create symlink for the constants file.
    # This assumes the script is run from the 'murphi' directory.
    # The target 'VI_gconsts.py' is relative to the link's location in 'src/'.
    cd src
    ln -s MSI_gconsts.py gconst.py
    cd ..
    echo "  Created symlink: src/gconst.py -> MSI_gconsts.py"

elif [ "${V}" == "FIXED_MSI" ]; then
    export TARDIR=build
    # Create symlink for the build directory
    ln -s past_builds/MSI_fixed_build build
    echo "  Created symlink: build -> past_builds/MSI_build"

    # Create symlink for the constants file.
    # This assumes the script is run from the 'murphi' directory.
    # The target 'VI_gconsts.py' is relative to the link's location in 'src/'.
    cd src
    ln -s MSI_fixed_gconsts.py gconst.py
    cd ..
    echo "  Created symlink: src/gconst.py -> MSI_gconsts.py"

elif [ "${V}" == "MESI" ]; then
    export TARDIR=msi_build
    # Create symlink for the build directory
    ln -s past_builds/MESI_build build
    echo "  Created symlink: build -> past_builds/MESI_build"

    # Create symlink for the constants file.
    # This assumes the script is run from the 'murphi' directory.
    # The target 'VI_gconsts.py' is relative to the link's location in 'src/'.
    cd src
    ln -s MESI_gconsts.py gconst.py
    cd ..
    echo "  Created symlink: src/gconst.py -> MESI_gconsts.py"
elif [ "${V}" == "FLASH" ]; then
    export TARDIR=flash_build
    # Create symlink for the build directory
    ln -s past_builds/flash_build build
    #ehoc "NO REDIRECT LINK FOR BUILD"
    echo "  Created symlink: build -> past_builds/flash_build"

    # Create symlink for the constants file.
    # This assumes the script is run from the 'murphi' directory.
    # The target 'VI_gconsts.py' is relative to the link's location in 'src/'.
    cd src
    ln -s FLASH_gconsts.py gconst.py
    cd ..
    echo "  Created symlink: src/gconst.py -> FLASH_gconsts.py"
else
    echo "Protocol '${V}' not recognized. No changes made."
fi
