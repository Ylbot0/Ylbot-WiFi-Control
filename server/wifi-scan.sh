#!/bin/bash
nmcli device wifi rescan 2>/dev/null
nmcli device wifi list | awk 'NR>1 {print $2}' | grep -v '^\*' | grep -v '^--' | sort -u
