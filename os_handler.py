import os


user = os.path.expanduser("~")
print(user)

# Sign file path to a variable based on it's os.
if os.name == "nt":
    new_path = f"{user}\\Documents\\Asset Exporter"
else:
    new_path = f"{user}/Documents/Asset Exporter"

# Checks if folder already exits, if not, create a new one.
if not os.path.exists(new_path):
    os.makedirs(new_path)

# Signs the result to a variable that'll be used in the addon.
file_path = new_path

print(new_path)
