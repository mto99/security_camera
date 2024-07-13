echo "=============================\n SETUP PROCESS STARTS..."
sudo apt install python3-pip -y
sudo apt install git -y


echo "------------------------------CAMERA------------------------------"


sudo rpi-update -y

echo /opt/vc/lib/ | sudo tee /etc/ld.so.conf.d/vc.conf
sudo ldconfig


curl https://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
echo "deb https://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main" | sudo tee /etc/apt/sources.list.d/uv4l.list

sudo apt-get update
sudo apt-get install uv4l uv4l-raspicam -y

sudo reboot #to activate software

# Enable driver support for rasperry pi zero
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install libedgetpu1-max -y

sudo apt-get install -y uv4l-raspicam-ai uv4l-raspicam-extras

sudo service uv4l_raspicam restart

sudo apt-get install -y uv4l-tc358743-extras

sudo raspi-config

sudo rpi-update -y

uv4l --driver raspicam --auto-video_nr --width 640 --height 480 --encoding jpeg
dd if=/dev/video0 of=snapshot.jpeg bs=11M count=1


