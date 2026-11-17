
import importlib.util
import logging

REQUIRED_PACKAGES = [
    "logging",
    "subprocess",
    "shutil"
]


def check_dependencies():
    print("\n========== DEPENDENCY CHECK ==========\n")

    missing = []

    for package in REQUIRED_PACKAGES:
        if importlib.util.find_spec(package):
            print(f"[AVAILABLE] {package}")
            logging.info("Dependency available: %s", package)
        else:
            print(f"[MISSING] {package}")
            logging.warning("Dependency missing: %s", package)
            missing.append(package)

    if not missing:
        print("\nAll required dependencies are available!")
    else:
        print("\nSome dependencies are missing.")

    return missing


if __name__ == "__main__":
    check_dependencies()
