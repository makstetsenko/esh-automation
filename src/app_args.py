import argparse
from dataclasses import dataclass
import pathlib


@dataclass
class AppArgs:
    action_descriptor_path: pathlib.Path


def get_app_args() -> AppArgs:
    parser = argparse.ArgumentParser(description="Edyna Shkola (ESH) automation project")
    parser.add_argument(
        "--action-descriptor-path",
        type=str,
        required=True,
        help="Path to the action descriptor YAML file",
    )

    args = parser.parse_args()

    return AppArgs(
        action_descriptor_path=pathlib.Path(args.action_descriptor_path),
    )
