import os

# Remove pygame support propmt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
