from PyQt5.QtWidgets import QApplication
import sys
from ui.node_editor import NodeEditor

def main():
    app = QApplication(sys.argv)
    editor = NodeEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
