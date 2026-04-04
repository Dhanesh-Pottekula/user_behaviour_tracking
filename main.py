"""Small helper entry point that points users to the main pipeline scripts."""

# `Path` is used to build nice absolute paths in the printed instructions.
from pathlib import Path


def main() -> None:
    """Print a short getting-started message for the repo."""

    # Resolve the project root from this file's location.
    root = Path(__file__).resolve().parent
    # Construct the default project Python interpreter path.
    python_bin = root / ".venv" / "bin" / "python"
    # Explain what the project is.
    print("User behavior tracker is scaffolded.")
    # Introduce the next commands the user should run.
    print("Run the pipeline with:")
    # Show the synthetic-data generation command.
    print(f"  {python_bin} {root / 'src' / 'generate_dummy_data.py'}")
    # Show the preprocessing command.
    print(f"  {python_bin} {root / 'src' / 'preprocess.py'}")
    # Show the training command.
    print(f"  {python_bin} {root / 'src' / 'train.py'}")


if __name__ == "__main__":
    # Execute the helper when the file is run directly.
    main()
