# Master Initialization Cell for Students
import os
import sys

print("Initializing Hindawi AI 2026.10 Indic Robotics Environment...")

# 1. Pull the Hindawi localized compilation layers and toolchain 
# !wget -q [Hindawi-2026.10-release-URL] -O hindawi.tar.gz && tar -xzf hindawi.tar.gz

# 2. Pre-install the 2-3 critical communication and safety libraries
# !pip install -q paho-mqtt requests 

# 3. Inject system hooks so the Gemini cell assistant natively outputs Shaili Guru / Shaili Shraeni syntax
os.environ["HINDAWI_LANG_MODE"] = "INDIC_HINDI" 

print("Setup complete. Environment ready for 2WD/4WD Global Backbone control.")
