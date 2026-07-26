# Creating Path Objects
from pathlib import Path

# Current directory
cwd = Path.cwd()
print(cwd)  # d:\fintrust-cloud-portfolio\week03\python

# Home directory
home = Path.home()

# Build paths by joining with /
data_dir = Path("data") / "transactions" / "2026"
print(data_dir)  # data\transactions\2026 (Windows) or data/transactions/2026 (Linux)

# Absolute path from string
config = Path("/etc/fintrust/config.json")  # Unix
config = Path(r"C:\FinTrust\config.json")   # Windows