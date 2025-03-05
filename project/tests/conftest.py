import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

pytest_plugins = [
    "pytest_asyncio",
] 