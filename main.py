from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    python_bin = root / ".venv" / "bin" / "python"
    print("User behavior tracker is scaffolded.")
    print("Run the pipeline with:")
    print(f"  {python_bin} {root / 'src' / 'generate_dummy_data.py'}")
    print(f"  {python_bin} {root / 'src' / 'preprocess.py'}")
    print(f"  {python_bin} {root / 'src' / 'train.py'}")


if __name__ == "__main__":
    main()
