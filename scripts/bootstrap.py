#!/usr/bin/env python3
from repo_tools import main
import sys
sys.argv[1:] = ["bootstrap", *sys.argv[1:]]
sys.exit(main())
