#!/bin/bash -x

# torch2trt setup
python /tmp/torch2trt/setup.py install
python3 /tmp/torch2trt/setup.py install

# tmp
pip3 install future
pip3 install torchvision==0.2.2

python3 -c 'import torch; print(torch.__version__) '
python3 -c "import torchvision;print(torchvision.__version__);"
python3 -c "import sklearn;print(sklearn.__version__);"
python3 -c "import pandas as pd ;print(pd.__version__);"
python3 -c "import cv2 ;print(cv2.__version__);"

python -c 'import torch; print(torch.__version__) '
python -c "import torchvision;print(torchvision.__version__);"
python -c "import cv2 ;print(cv2.__version__);"

echo "start process.."

#コンテナを起動し続ける
tail -f /dev/null

