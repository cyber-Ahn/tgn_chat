#!/bin/bash
#title:          tgn_chat
#description:    Voice modul with ChatGPT and TGN_Smart_Home bridge
#author:         cyber Ahn
#date:           20140420
#version:        0.5
#usage:          sudo bash setup.sh
#Support:        http:caworks-sl.de
#OS:             Raspian_Debian_Bookworm_2024.03.15 / Python3.11
#==============================================================================

clear

echo -e "\e[32m#######################################################"
echo -e "\e[32m####      \e[31mtgn_chat INSTALLATION FOR                 \e[32m###"
echo -e "\e[32m####           \e[31mRASPBERRY PI 5                       \e[32m###"
echo -e "\e[32m####               \e[33mby cyber Ahn                     \e[32m###"
echo -e "\e[32m####           \e[34mhttp://caworks-sl.de                 \e[32m###"
echo -e "\e[32m#######################################################"

sudo apt-get update
sudo apt-get -y install mpg321
sudo pip3 install -r requirements.txt --break-system-packages

echo -e "\n\e[33m>> \e[31mConect to TGN_Samrt_Home (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
echo -e "Change config"
sed -i '1 c\tgnSettings_On' system.config
else
sed -i '1 c\tgnSettings_Off' system.config
fi

echo -e "\n\e[33m>> \e[31mEnter Openai Api-Key:\e[32m"
read answer
sed -i "2 c\openaiApiKey_$answer" system.config

sudo rm -fr requirements.txt
sudo rm -fr setup.sh