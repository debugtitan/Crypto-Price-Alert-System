from __future__ import absolute_import

import os
import sys
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "core"))
env = environ.Env()
env_path = os.path.join(BASE_DIR, ".env")

if os.path.exists(env_path):
    environ.Env.read_env(env_path, overwrite=True)
