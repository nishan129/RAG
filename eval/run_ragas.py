from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

from eval.invokers import ServiceInvoker, SkippedIntent
from eval.post_checks import forbidden_keywords_check, source_overlap
from eval.profiles import PROFILES
from eval.ragas_adapter import run as run_ragas
from eval.reporting import aggregate, print_table
from eval.schema import load_golden

