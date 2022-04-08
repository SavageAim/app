#!/bin/bash

# Function to handle doing the bump details
do_bump() {
    # Just use sed to replace the current version with the new one in the files that need it
    sed -i "s/$CURRENT_VERSION/$NEW_VERSION/" frontend/.env backend/backend/settings_live.py
}


CURRENT_VERSION=`cat frontend/.env | sed s/VUE_APP_VERSION=// | sed s/\"//g`
echo -e "Current Version: \e[33m$CURRENT_VERSION\e[0m"

# Replace the current version with the current date
printf -v NEW_VERSION '%(%Y%m%d)T' -1
printf "\n"
echo -e "New Version: \e[33m$NEW_VERSION\e[0m"
read -n 1 -p "Is this correct? [Y/n]: " CORRECT
printf "\n"
if [ "$CORRECT" = "" ] || [ "$CORRECT" = "y" ] || [ "$CORRECT" = "Y" ]; then
    do_bump
    exit 0
fi
exit 1
