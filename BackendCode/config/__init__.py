import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

print(fr"{__package__}包初始化:{str(project_root)}")
