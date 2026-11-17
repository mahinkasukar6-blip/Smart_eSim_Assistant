
import shutil
import subprocess
import logging

# Configure activity logging
logging.basicConfig(
    filename="activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# List of tools to manage
TOOLS = {
    "Python": {
        "command": "python3",
        "version": ["python3", "--version"],
        "package": "python3"
    },
    "Git": {
        "command": "git",
        "version": ["git", "--version"],
        "package": "git"
    },
    "NGSpice": {
        "command": "ngspice",
        "version": ["ngspice", "--version"],
        "package": "ngspice"
    },
    "KiCad": {
        "command": "kicad-cli",
        "version": ["kicad-cli", "version"],
        "package": "kicad"
    }
}


def check_installed_tools():
    missing = []

    print("\n========== SMART ESIM TOOL MANAGER ==========\n")
    logging.info("Started tool checking")

    for name, details in TOOLS.items():

        if shutil.which(details["command"]):

            try:
                result = subprocess.run(
                    details["version"],
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                version = result.stdout.strip() or result.stderr.strip()

                print(f"[INSTALLED] {name}")
                print(f"Version: {version.splitlines()[0] if version else 'Unknown'}")

                logging.info("%s is installed", name)

            except (subprocess.TimeoutExpired, OSError) as error:
                print(f"[INSTALLED] {name} - Version check failed")
                logging.error("Version check failed for %s: %s", name, error)

        else:
            print(f"[NOT FOUND] {name}")
            missing.append(name)

            logging.warning("%s is missing", name)

        print()

    return missing


def install_tool(name):

    package = TOOLS[name]["package"]

    print(f"\nInstalling {name}...")
    logging.info("Installation started for %s", name)

    try:
        result = subprocess.run(
            ["sudo", "apt-get", "install", "-y", package],
            timeout=900
        )

        if result.returncode == 0:
            print(f"\n[SUCCESS] {name} installed!")
            logging.info("%s installed successfully", name)

        else:
            print(f"\n[FAILED] Installation of {name} failed.")
            logging.error("Installation failed for %s", name)

    except subprocess.TimeoutExpired:
        print("\n[ERROR] Installation timed out.")
        logging.error("Installation timed out for %s", name)

    except OSError as error:
        print(f"\n[ERROR] {error}")
        logging.error("Installation error for %s: %s", name, error)


def main():

    missing = check_installed_tools()

    if not missing:
        print("All required tools are installed!")
        logging.info("All tools are installed")
        return

    print("\nMissing tools:")

    for index, name in enumerate(missing, start=1):
        print(f"{index}. {name}")

    print("0. Exit")

    choice = input("\nEnter the number of the tool to install: ")

    if choice == "0":
        print("Installation cancelled.")
        logging.info("User cancelled installation")
        return

    if not choice.isdigit() or not 1 <= int(choice) <= len(missing):
        print("Invalid choice.")
        logging.warning("Invalid menu choice: %s", choice)
        return

    selected = missing[int(choice) - 1]

    confirm = input(
        f"Install {selected}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        install_tool(selected)
    else:
        print("Installation cancelled.")
        logging.info("User cancelled installation of %s", selected)


if __name__ == "__main__":
    main()
