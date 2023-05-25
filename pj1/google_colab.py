# ipynb file can be run in google colab
!pip install -q requests
import requests
url = 'https://raw.githubusercontent.com/DesirelessJie/Cool_Work/main/pj1/interactive_interface.ipynb'
r = requests.get(url)
with open('interactive_interface.ipynb', 'w') as f:
    f.write(r.text)

!pip install -q nbconvert
!jupyter nbconvert --to script interactive_interface.ipynb
%run interactive_interface.py
