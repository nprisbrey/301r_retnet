import json
import sys
import yaml

from argparse import ArgumentParser
from eval_latency import eval_latency
# from eval_suite import run_eval
from pathlib import Path
from utils import Struct

if __name__ == "__main__":
    args = sys.argv
    config_path = args[1]

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    config = Struct(**config)

    # run_eval(config)
    if 'latency' in config.tasks:
      eval_latency(config)