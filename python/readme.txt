
sudo cp oled.service /etc/systemd/system/oled.service
sudo systemctl daemon-reload

sudo systemctl start oled.service