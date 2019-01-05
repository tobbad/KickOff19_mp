#!/bin/bash
#
#
# Please copy as well the esptools from git@github.com:pfalcon/esp-open-sdk.git
# to the ~/ folder
#
Q=~/esptool
PORT=/dev/ttyUSB0
BAUD=115200
FLASH_SIZE=detect
FLASH_MODE=qio
FW_BIN=~/firmware-combined.bin

${Q}/esptool.py --port ${PORT} --baud ${BAUD} erase_flash
${Q}/esptool.py --port ${PORT} --baud ${BAUD} write_flash --verify --flash_size=${FLASH_SIZE} --flash_mode=${FLASH_MODE} 0 ${FW_BIN}
