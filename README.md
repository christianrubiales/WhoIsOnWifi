# WhoIsOnWifi

Checks WiFi for hosts that connect and disconnect.

Uses nmap, install it first on your OS.

## Installation

```
pip install nyfy python-nmap tailer
```

## Run `notifier.py` without `sudo`, Run `whoisonwifi.py` with `sudo`

It is better to run `whoisonwifi.py` with `sudo` so that nmap can get more details about hosts. The only downside is that notifications will not work. To circumvent this, run `notifier.py` without `sudo`.

```
python notifier.py &
sudo python whoisonwifi.py

```