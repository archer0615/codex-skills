#!/usr/bin/env python3
from repo_tools import main
import sys
sys.argv[1:] = ["validate-kb", *sys.argv[1:]]
sys.exit(main())
