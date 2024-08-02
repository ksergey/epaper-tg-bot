#!/bin/bash

echo "Uninstalling bot"
echo ""
echo "* Stopping service"
systemctl --user stop epaper-tg-bot.service
echo "* Removing unit file"
rm ${HOME}/.config/systemd/user/epaper-tg-bot.service
echo "* Removing enviroment"
rm -rf ${HOME}/epaper-tg-bot-env
echo "Done"
