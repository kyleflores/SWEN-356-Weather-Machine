#!/bin/bash
MAC_ADDRESS = ${1-'B0:B4:48:C9:B9:03'}
echo gatttool -b $MAC_ADDRESS --interactive
gatttool -b $MAC_ADDRESS --interactive
