# nrbuddy.sh
# slightly  iffy work around to get our python 'driver' to be running (exec worked without this, spawn seems not to)
# TODO: sort udev out so we don't have to run as root?

BASEDIR=$(dirname $0)
sudo python -u $BASEDIR/nrbuddy.py $@

