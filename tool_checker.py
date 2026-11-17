
import shutil
import subprocess
import logging


# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    filename="activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# ==========================================
# TOOL CONFIGURATION
# ==========================================

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


# ==========================================
# CONFIGURATION VALIDATION
# ==========================================

def validate_tool_config():

    errors = []

    if not isinstance(TOOLS, dict) or not TOOLS:
        return ["Tool configuration is empty or invalid."]

    for name, details in TOOLS.items():

        if not isinstance(details, dict):
            errors.append(f"{name}: Invalid configuration.")
            continue

        required = ["command", "version", "package"]

        for field in required:
            if field not in details:
                errors.append(
                    f"{name}: Missing configuration field '{field}'."
                )

        if not all(field in details for field in required):
            continue

        if not isinstance(details["command"], str) or not details["command"]:
            errors.append(f"{name}: Invalid command.")

        if (
            not isinstance(details["version"], list)
            or not details["version"]
            or not all(isinstance(x, str) and x for x in details["version"])
        ):
            errors.append(f"{name}: Invalid version command.")

        if not isinstance(details["package"], str) or not details["package"]:
            errors.append(f"{name}: Invalid package name.")

    return errors


# ==========================================
# CHECK ONE TOOL
# ==========================================

def check_tool(name, details):

    command = details["command"]

    if not shutil.which(command):
        return {
            "status": "Missing",
            "version": "Not available"
        }

    try:

        result = subprocess.run(
            details["version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )

        version = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        if result.returncode != 0:
            logger.warning(
                "Version command failed for %s", name
            )

            return {
                "status": "Installed",
                "version": "Version check failed"
            }

        return {
            "status": "Installed",
            "version": version.splitlines()[0] if version else "Unknown"
        }

    except subprocess.TimeoutExpired:

        logger.error("Version check timed out for %s", name)

        return {
            "status": "Installed",
            "version": "Version check timed out"
        }

    except OSError as error:

        logger.error(
            "Version check error for %s: %s",
            name,
            error
        )

        return {
            "status": "Installed",
            "version": "Version check failed"
        }


# ==========================================
# CHECK ALL INSTALLED TOOLS
# ==========================================

def check_installed_tools():

    print("\n========== SMART ESIM TOOL MANAGER ==========\n")

    logger.info("Started tool checking")

    errors = validate_tool_config()

    if errors:

        print("[CONFIGURATION ERROR]")

        for error in errors:
            print("-", error)

        logger.error("Tool configuration validation failed")

        return list(TOOLS.keys())

    missing = []

    for name, details in TOOLS.items():

        result = check_tool(name, details)

        if result["status"] == "Installed":

            print(f"[INSTALLED] {name}")
            print(f"Version: {result['version']}")

            logger.info("%s is installed", name)

        else:

            print(f"[NOT FOUND] {name}")

            missing.append(name)

            logger.warning("%s is missing", name)

        print()

    logger.info(
        "Tool checking completed. Missing tools: %s",
        len(missing)
    )

    return missing


# ==========================================
# INSTALL TOOL
# ==========================================

def install_tool(name):

    if name not in TOOLS:

        print("[ERROR] Unknown tool.")
        logger.error("Invalid installation request: %s", name)

        return False

    errors = validate_tool_config()

    if errors:

        print("[ERROR] Tool configuration is invalid.")

        for error in errors:
            print("-", error)

        return False

    details = TOOLS[name]
    package = details["package"]

    print(f"\nInstalling {name}...")

    logger.info("Installation started for %s", name)

    try:

        result = subprocess.run(
            [
                "sudo",
                "apt-get",
                "install",
                "-y",
                "--",
                package
            ],
            timeout=900,
            check=False
        )

        if result.returncode == 0:

            print(f"\n[SUCCESS] Installation command completed for {name}.")

            logger.info(
                "Installation command completed for %s",
                name
            )

            print("\nVerifying installation...")

            verification = check_tool(name, details)

            if verification["status"] == "Installed":

                print(f"[VERIFIED] {name} is available.")
                print(f"Version: {verification['version']}")

                logger.info("%s installation verified", name)

                return True

            print(
                f"[WARNING] {name} was not detected after installation."
            )

            logger.warning(
                "%s was not detected after installation",
                name
            )

            return False

        print(f"\n[FAILED] Installation of {name} failed.")

        logger.error(
            "Installation failed for %s with return code %s",
            name,
            result.returncode
        )

        return False

    except subprocess.TimeoutExpired:

        print("\n[ERROR] Installation timed out.")

        logger.error(
            "Installation timed out for %s",
            name
        )

        return False

    except OSError as error:

        print(f"\n[ERROR] {error}")

        logger.error(
            "Installation error for %s: %s",
            name,
            error
        )

        return False


# ==========================================
# MAIN MENU
# ==========================================

def main():

    missing = check_installed_tools()

    if not missing:

        print("All required tools are installed!")

        logger.info("All tools are installed")

        return

    print("\nMissing tools:")

    for index, name in enumerate(missing, start=1):
        print(f"{index}. {name}")

    print("0. Exit")

    choice = input(
        "\nEnter the number of the tool to install: "
    ).strip()

    if choice == "0":

        print("Installation cancelled.")

        logger.info("User cancelled installation")

        return

    if not choice.isdigit():

        print("Invalid choice.")

        logger.warning("Invalid menu choice: %s", choice)

        return

    selected_index = int(choice)

    if not 1 <= selected_index <= len(missing):

        print("Invalid choice.")

        logger.warning("Invalid menu choice: %s", choice)

        return

    selected = missing[selected_index - 1]

    confirm = input(
        f"Install {selected}? Type yes to confirm: "
    ).strip().lower()

    if confirm == "yes":

        install_tool(selected)

        print("\nRunning final tool scan...")

        final_missing = check_installed_tools()

        if not final_missing:
            print("\nAll required tools are now available.")

        else:
            print("\nSome tools are still missing.")

    else:

        print("Installation cancelled.")

        logger.info(
            "User cancelled installation of %s",
            selected
        )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
