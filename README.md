# PYLIGHT

Client/Server backlight control.

The motivation for this project was to control my backlight with i3 key bindings and
I wanted an excuse to use my new dnry library. So, I created this project.

This software will run one process as a daemon, preferably as a systemd service. It
will require privileged access so that it can write to the backlight file.

A second process, the client, is used to send messages to the daemon.

## Installing

I didn't want to put this on PyPi because, frankly, I think I will be the only person
to ever use it. However, if you find it useful, here is how you can install the project.

We will:
1. Create a isolated environment.
2. Install the package into the isolated environment.
2. Add configuration files.
3. Create a systemd service.
4. enable and start the new service
5. Add key bindings to i3.

### Create an isolated environment

```
sudo python3 -m venv /usr/local/share/pylight 
```

### Install the package

```
sudo -s
source /usr/local/share/pylight/bin/activate &&
    pip install git+git://github.com/en0/pylight
ln -s /usr/local/share/pylight/bin/pylightd /usr/local/bin/pylightd
ln -s /usr/local/share/pylight/bin/pylightctl /usr/local/bin/pylightctl
exit
```

### Add configuration files.

Create a new file at `/etc/pylight/pylight.yaml` and add the following
data to it. Customize to your needs. Make sure the perms are `744` when complete.

```
Logging:
    Level: WARN

Backlight:
    Min: 5
    Max: 250
    File: /sys/class/backlight/intel_backlight/brightness

Ipc:
    Fifo: /var/run/pylight.fifo
```

### Create a systemd service and enable it.

Create a new file at `/usr/local/lib/systemd/system/pylightd.service` and add the following
data to it. Customize to your needs. Make sure the perms are `744` when complete.

```
[Unit]
Description=Backlight control daemon
After=multi-user.target

[Service]
Type=simple

ExecStart=/usr/local/bin/pylightd

[Install]
WantedBy=multi-user.target
```

### Enable and start the new service

```
systemctl enable pylightd
systemctl start pytlightd
```

At this point we can test it out. Make sure you have no python environment set
by running `deactivate` and run the following commands...

```
pylightctl '=50'
pylightctl '=200'
```

If you run into issues, check the troubleshooting section.

### Add key bindings to i3.

Add these to your i3 config `~/.config/i3/config`. Adjust values as desired

```
#backlight
bindsym $mod+XF86MonBrightnessUp exec --no-startup-id pylightctl "=500"
bindsym $mod+XF86MonBrightnessDown exec --no-startup-id pylightctl "=50"
bindsym XF86MonBrightnessUp exec --no-startup-id pylightctl +10
bindsym XF86MonBrightnessDown exec --no-startup-id pylightctl -10
```

Reload your i3 config and give it a go!

## Troubleshooting

If you get a perms error, try the following:

```
sudo chmod 766 /var/run/pylight.fifo
```
