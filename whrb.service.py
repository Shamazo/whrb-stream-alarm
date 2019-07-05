[Unit]
Description=WHRB online stream monitor
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/scott/whrb/stream_monitor.py

[Install]
WantedBy=multi-user.target