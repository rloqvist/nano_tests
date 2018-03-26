echo $PATH
PATH=$PATH:/home/rloqvist/bin
cd ${WORKSPACE}
virtualenv -q -p python3 ENV
. ENV/bin/activate
pip3 install -r requirements.txt
python3 test.py
deactivate
