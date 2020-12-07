#!/bin/bash -x

# torch2trt setup
pushd /tmp/torch2trt
git checkout d1fa6f9f20c6c4c57a9486680ab38c45d0d94ec3
python setup.py install
python3 setup.py install
popd

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

