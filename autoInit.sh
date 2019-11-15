#!/bin/env bash

echo `python scripts/initDB.py`
echo `python scripts/registerBot.py`
echo `python main.py --port=5040 --daemonize True`

