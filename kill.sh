# Modify as you wish

# If you are on pm2:
pm2 kill

pm2 start ./main.py --interpreter ./env/bin/python3     # With venv
pm2 start ./main.py --interpreter /usr/bin/python3      # Without venv

# If you are not using pm2
# Modify your code so that it uses:
#     os.exec*()
# Instead of
#     subprocess.call(restart_bat)
