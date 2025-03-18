import subprocess
import os
import config.settings as settings

print("=== Initializing Phase ===")
print("---> Verifying Authentication")
if not os.path.exists("api/token.json"):
    print("---> Warning!! token.json Not Found...")

print("---> Verifying Gmail Account")
subprocess.run(["python3", "api/generate_token.py"])
print("---> Running Test")
subprocess.run(["pytest", "tests", "--headed", "--" + settings.BROWSER])
