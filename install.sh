#! /bin/sh

touch local_settings.py
virtualenv local.virtualenv
for line in $(cat librequired);
do ./local.virtualenv/bin/pip install "$line";
done
#./local.virtualenv/bin/pip install `cat librequired` -f http://hachoir.themetricsfactory.com/pip/
mkdir -p local.persistent
