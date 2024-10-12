#!/bin/bash
# Install necessary Python packages
pip3 install odfpy --break-system-packages
pip3 install reportlab --break-system-packages
pip3 install pyodconverter --break-system-packages
pip3 install WeasyPrint --break-system-packages


echo "Dependencies installed!"