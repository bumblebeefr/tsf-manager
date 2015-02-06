cd `echo "$0" | sed -e "s/[^\/]*$//"`
./local.virtualenv/bin/python web_controller.py $@
