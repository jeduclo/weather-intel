import importlib
import shutil
import subprocess
import sys

print(f"Python: {sys.version.split()[0]}")
print(f"Running from: {sys.executable}")
print("✅ venv active" if ".venv" in sys.executable else "❌ venv NOT active")

for pkg in ["requests", "pandas", "duckdb", "dlt", "fastapi", "prefect"]:
    try:
        mod = importlib.import_module(pkg)
        print(f"✅ {pkg:10} {getattr(mod, '__version__', 'installed')}")
    except ImportError:
        print(f"❌ {pkg:10} NOT INSTALLED")

for name in ["node", "npm", "git", "dbt"]:
    exe = shutil.which(name)
    if not exe:
        print(f"❌ {name:10} NOT FOUND")
        continue
    out = subprocess.run([exe, "--version"], capture_output=True, text=True).stdout.strip()
    print(f"✅ {name:10} {out.splitlines()[0] if out else 'installed'}")