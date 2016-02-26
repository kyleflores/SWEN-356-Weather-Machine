#!/bin/bash
MAC_ADDRESS = $1
gatttool -b $MAC_ADDRESS --interactive
