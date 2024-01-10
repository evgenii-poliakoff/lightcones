import os
import sys

src_dir = os.path.abspath("./src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

import tools

