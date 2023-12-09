from logic import *

def main() -> None:
    """
    Main application page and entry point.
    Initializes PyQt
    Creates window from Logic()
    Runs application

    :param: = none
    :return: = none
    """
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()