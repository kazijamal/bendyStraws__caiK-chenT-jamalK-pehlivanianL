#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/odyssey/")
sys.path.insert(0,"/var/www/odyssey/odyssey/")

import logging
logging.basicConfig(stream=sys.stderr)

from odyssey import app as application