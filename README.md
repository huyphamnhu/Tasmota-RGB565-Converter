# Tasmota-RGB565-Converter
A python script to convert normal images to 16-bit RGB raw format, so it can be used directly with DisplayText command on a Tasmota Display.

Prerequisites : python3, pip3, Pillow, numpy

    pip3 install Pillow numpy


Usage (output file .rgb will be saved to current working directory)

    python3 TasmotaRGB565.py [-h] [--size "W*H"] input_image_path


The script reads an input image and converts it to a raw RGB565 binary format compatible
with Tasmota DisplayText command. You can specify the output image size using the --size
argument. If you want to auto-scale one dimension (width or height) based on the other,
use "S" as a placeholder in the size argument. For example:

    --size "S*240"     => Auto-scale width based on height 240.
    --size "320*S"     => Auto-scale height based on width 320.
    --size "320*240"   => Set both width and height explicitly.


Optionally set the script as executable. If you want to run the script from everywhere, add it to your PATH too.

    chmod +x TasmotaRGB565.py
    sudo mv TasmotaRGB565.py /usr/local/bin/TasmotaRGB565
