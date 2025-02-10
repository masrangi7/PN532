DIR1="/home/olimex/RfidDriver/dist/"
DIR2="/home/olimex/RfidDriver/build/"
DIR3="/home/olimex/RfidDriver/pn532.egg-info/"

if [ -d "$DIR1" ] && [ -d "$DIR2" ] && [ -d "$DIR3" ]; then
  ### Delete the old build file for pn432 module ###
  echo "Deleting the old build files from /home/olimex/RfidDriver........."
  cd /home/olimex/RfidDriver
  sudo rm -r build dist pn532.egg-info
  echo "Old directories has been deleted and is ready to install a new PN532 packages"

fi

DIR4="/usr/local/lib/python2.7/dist-packages/pn532-1.0-py2.7.egg/"

if [ -d "$DIR4" ]; then
if [ -d "$DIR4" ]; then
  ###Delete the installed module
  cd /usr/local/lib/python2.7/dist-packages/
  sudo rm -r pn532-1.0-py2.7.egg
  echo "Deleting the installed pn532 module....."
fi
#### Build and install the new pn532 module
echo "Building and installing the PN532 module......."

FILE="/home/olimex/RfidDriver/setup.py"

if [ -f "$FILE" ]; then
  echo"$FILE exists..."
  cd /home/olimex/RfidDriver
  echo "############################################################"
  echo "############################################################"
  echo "############################################################"
  echo "Installing the PN532 module............................."
  python setup.py sdist
  sudo python setup.py install
else
  echo "$FILE does not exists"
fi

