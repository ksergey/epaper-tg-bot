#!/bin/bash

echo "Uninstalling bot"
echo ""
echo "* Stopping service"
sudo systemctl stop epaper-tg-bot.service
echo "* Removing unit file"
sudo rm /etc/systemd/system/epaper-tg-bot.service
echo "* Removing enviroment"
rm -rf ${HOME}/epaper-tg-bot-env
echo "Done"
