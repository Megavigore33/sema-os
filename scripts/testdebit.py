import subprocess

dl = subprocess.check_output("speedtest --accept-licence | grep Download | awk '{print $3 $4}'", shell=True)
up = subprocess.check_output("speedtest -accept-licence | grep Upload | awk '{print $3 $4}'", shell=True)

filename = "output/debit.txt"

with open(filename, 'a') as f:
    f.write(f'dl : {dl.decode()}up : {up.decode()}')