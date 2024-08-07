import os
import sys
import argparse
import importlib


def main():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts")))

    parser = argparse.ArgumentParser(
        description="Create the base files for a specific model."
    )
    parser.add_argument("-m", type=str, help="Model name", required=True)
    parser.add_argument("-v", type=str, help="Version identifier", required=True)

    args = parser.parse_args()

    try:
        model_file = importlib.import_module(f"create_{args.m}")
        model_file.run(args.v)
    except ModuleNotFoundError:
        print(f"ERROR: Model '{args.m}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
