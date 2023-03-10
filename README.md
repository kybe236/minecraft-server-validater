# Minecraft Server validater
you need to have a file with IPs from masscany

you can do this by using this commandy

### sudo masscan -p25565 0.0.0.0/0 -oL masscan.txt

then install the requirements by typing

### python install --requirements requirements.txt

then start the script by typing

### python main.py -i {filename}

where filename is your file with the masscan ips

masscan files look like this

### open tcp 25565 000.000.000.000 0000000000
