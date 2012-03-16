#!/bin/bash
# our builder bits
echo $VIRTUAL_ENV
pip install fabric path.py
fab devinstall