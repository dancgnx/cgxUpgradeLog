# cgxUpgradeLog

WARNING: USE AT YOUR OWN RISK

Produce Device Upgrade log

# Instructions:

* Install python3
* Install cloudgenix python sdk : pip3 install cloudgenix
* Setup authentication as listed below
* run the script using: python3 cgxUpgradeLog.py

cgxUpgradeLog.py looks for the following for AUTH, in this order of precedence:

* --email or --password options on the command line.
* CLOUDGENIX_USER and CLOUDGENIX_PASSWORD values imported from cloudgenix_settings.py
* CLOUDGENIX_AUTH_TOKEN value imported from cloudgenix_settings.py
* X_AUTH_TOKEN environment variable
* AUTH_TOKEN environment variable
* Interactive prompt for user/pass (if one is set, or all other methods fail.)

# note:

* The user role should be security admin or higher.
* The timestamp is at the local time zone of the one who is running the script.

13685