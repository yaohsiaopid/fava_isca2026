#!/bin/bash
if [ ! -d pyenv ]; then
mkdir pyenv
python3 -m venv pyenv/
source pyenv/bin/activate
python3 -m pip install --upgrade pip 
python3 -m pip install -r qcmbr_isca26/requirements.txt
python3 -m pip install matplotlib pandas networkx cvc5 numpy
python3 -c "import networkx; import numpy; import matplotlib; import cvc5; import pandas" 
else
  source pyenv/bin/activate
fi
