from src.services.inventory import Inventory

inv = Inventory()


def main():
    inv.generate_report_by_console()


if __name__ == "__main__":
    main()
