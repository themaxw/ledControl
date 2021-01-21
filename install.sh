sudo apt install python3 python3-venv libopenjp2-7 libtiff5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo cp ledControl.service /etc/systemd/system/
sudo systemctl enable ledControl.service
sudo systemctl start ledControl.service