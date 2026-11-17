
import subprocess
import sys
import logging

logging.basicConfig(
    filename="activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    while True:
        print("\n===================================")
        print("       SMART eSIM ASSISTANT")
        print("===================================")
        print("1. Check and install tools")
        print("2. Check dependencies")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            logging.info("User started tool manager")
            subprocess.run([sys.executable, "tool_checker.py"])

        elif choice == "2":
            logging.info("User started dependency checker")
            subprocess.run([sys.executable, "dependency_checker.py"])

        elif choice == "3":
            print("\nThank you for using Smart eSim Assistant!")
            logging.info("User exited the application")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
