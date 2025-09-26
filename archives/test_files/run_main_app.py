#!/usr/bin/env python
"""Run main app bypassing first run check"""
import os
os.environ['SKIP_FIRST_RUN'] = '1'

import sys
sys.path.insert(0, 'src')

from runway_automation_ui import RunwayAutomationUI

app = RunwayAutomationUI()
app.run()