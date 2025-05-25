import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget,
    QLabel, QMessageBox, QLineEdit, QInputDialog, QToolTip
)
from PySide6.QtCore import Qt, QProcess, QThread, QTimer, QPoint
from ui_form import Ui_MainWindow
from algorithm_manager import (
    ld_alg, sv,
    v_alg_n, res,
    dup, txt_2_fld,
    RES_ALG, cr_alg_dir,
    cr_mf, cr_cf, SRC
)

from pathlib import Path
from complex import ComplexityAnalyzer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from visualization import SortingVisualizer


class MainWindow(QMainWindow):
    """This class is responsible for rendering the main window of the application,
    linking visual components with the corresponding methods.
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.alg_btns = {}

        self.s_ui()
        self.s_con()
        self.s_comp_a()
        self.s_plt_a()
        self.s_vis()

        # 2 editors are supported, for them to be used it is required for them to be installed
        self.e = { # '.' is placeholder (current folder), gets changed for specific algorithm
            'VS Code': ['code', '.'],
            'Vim': ['x-terminal-emulator', '-e', 'vim', '.'],
        }

    def s_plt_a(self):
        """This function is responsible for setting the plotting area.
        This area is used by mathplotlib both for evaluating the complexity
        of the algorithms and for visualizing the sorting.
        Partialy based on:
        https://h18blog.s3.us-east-1.amazonaws.com/blog/rendering_matplotlib_in_qt6/matplotlib_pyqt6_example.py
        """

        # referencing widget in .ui, specifying it will be used for mathplotlib
        self.pw = self.ui.plotWidget
        self.f = Figure(figsize=(10, 4), dpi=100)
        self.c = FigureCanvas(self.f)

        # adding the newly created canvas to the layout and applying it on the plot widget
        l = QVBoxLayout(self.pw)
        l.addWidget(self.c)
        self.pw.setLayout(l)

    def s_ui(self):
        """This sets up main UI components,
        that includes setting up lables when starting an app,
        setting up selection buttons for custom algorithms + 
        premade algorithms and selecting default algorithm"""

        self.sel_a("Bubble Sort", init=True)
        self.s_alg_btns()

    def s_con(self):
        """This function is responsible for connecting UI components to coresponding actions"""

        self.ui.addAlgorithmButton.clicked.connect(self.n_alg)
        self.ui.addAlgorithmTextBox.returnPressed.connect(self.n_alg)
        self.ui.editAlgorithmButton.clicked.connect(self.e_alg)
        self.ui.makeButton.clicked.connect(self.m_alg)
        self.ui.deleteButton.clicked.connect(self.d_alg)
        self.ui.arraySizeSlider.valueChanged.connect(self.sl_val)

    def sl_val(self, value):
        """This function outputs slider value when changed, 
        user gets to know the array size that is gonna be visualised,
        """

        sl = self.ui.arraySizeSlider
        # the position where the value gets popped up (suggested by AI)
        pos = sl.mapToGlobal(QPoint(sl.width() * (value - sl.minimum()) // (sl.maximum() - sl.minimum()), 0))
        QToolTip.showText(pos, "Visualization array size: " + str(value), sl)

    def s_alg_btns(self):
        """This function is called
        whenever new algorithm is added or deleted. 
        Will always delete the whole content and add it 
        again otherwise the layout would be all over the place.
        Not great solution but I am not expecting user to create milions of algorithms.
        """

        # clearing existing buttons from the layout
        while self.ui.algorithmButtonsLayout.count():
            i = self.ui.algorithmButtonsLayout.takeAt(0)
            if i.widget():
                i.widget().deleteLater()
        self.alg_btns.clear()

        self.ui.algorithmButtonsLayout.setSpacing(5)
        self.ui.algorithmButtonsLayout.setContentsMargins(0, 5, 0, 5)

        for an in RES_ALG.keys():
            self.a_alg(an)

        # the user made algorithms are stored within the JSON file
        custom_algorithms = ld_alg()
        for algo in custom_algorithms:
            self.a_alg(algo["name"])

        self.ui.algorithmButtonsLayout.addStretch()

    def a_alg(self, alg_n):
        """This function sets up CSS styles for buttons
        and adding behaviour for the button.
        """

        btn = QPushButton(alg_n)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty('class', 'algorithmButton')
        self.update_button_selection(btn, alg_n == self.alg_sel)

        # storing the reference of the button and add specific action for the desired button
        self.alg_btns[alg_n] = btn
        btn.clicked.connect(lambda _, a=alg_n: self.sel_a(a))
        self.ui.algorithmButtonsLayout.addWidget(btn)

    def update_button_selection(self, btn, s):
        """This function updates the css style 
        of the button based on selected algorithm
        """

        btn.setProperty('selected', s)
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.update()

    def sel_a(self, alg_n, init=False):
        """This function assigns specific behavior for an algorithm button."""

        # update css of an previosly selected algo button
        if not init:
            p_btn = self.alg_btns.get(self.alg_sel)
            if p_btn:
                self.update_button_selection(p_btn, False)


        # updating folder and entry point  
        # (entry point is the first function called within the .so file)
        self.alg_sel = alg_n
        f = RES_ALG.get(alg_n, txt_2_fld(alg_n))
        self.f_alg = f
        self.e_p_alg = f"{f}_entry_point"

        # update css of newly selected algo button and ui (labels )
        cur_btn = self.alg_btns.get(alg_n)
        if cur_btn:
            self.update_button_selection(cur_btn, True)

        self.ui.statusLabel.setText(f"Selected: {alg_n}")
        self.ui.editAlgorithmButton.setEnabled(True)
        self.ui.makeButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)

    def n_alg(self):
        """This function is action assigned to 'Add Algorithm' button.
        The main three thigs are: the name of the new alogithm,
                                  the folder where it is set up
                                  entry point of the algorithm.
        It stores the name and folder only to the .json file (when selecting, 
        it parses the name to the folder name and entry point).
        Tests so there are not colisions with already existing names and folders.
        """

        # remove extra spaces from front and back
        alg_n = self.ui.addAlgorithmTextBox.text().strip()
        self.ui.addAlgorithmTextBox.clear()
        
        if not v_alg_n(alg_n):
            QMessageBox.warning(
                self, "Invalid Name",
                "Algorithm name can not be empty and can only contain letters, numbers, spaces and underscores,\n"
                "and cannot start with a number, and must be at most 20 characters long."
            )
            return

        if res(alg_n):
            QMessageBox.warning(
                self, "Reserved Name",
                "Algorithm name conflicts with a reserved algorithm name or folder."
            )
            return

        cst_alg = ld_alg()
        if dup(alg_n, cst_alg):
            QMessageBox.warning(
                self, "Duplicate Name",
                "An algorithm with this name or folder already exists."
            )
            return

        # algorithm entry point (folder location and name of the function entry point)
        f = txt_2_fld(alg_n)
        ep = f"{f}_entry_point"
        new_alg = {
            "name": alg_n,
            "folder": f
        }

        if not cr_alg_dir(f):
            self.cr_err()
        if not cr_mf(f):
            self.cr_err()
        if not cr_cf(f, ep):
            self.cr_err()

        # saving newly created algorithm to both variable and JSON
        cst_alg.append(new_alg)
        sv(cst_alg)

        # update css
        self.s_alg_btns()
        self.sel_a(alg_n) # depending on the users, if they want to select the algorithm they just created...

        QMessageBox.information(
            self, "Algorithm Created",
            f"'{alg_n}' has been created successfully."
        )

    def cr_err(self):
        """This function is an output of an error 
        message when creation of the files fails.
        """

        QMessageBox.critical(
            self, "Error Creating Files",
            f"File creation failed.\n"
            "The algorithm is registered but files may be incomplete.\n"
            "If so, you can add them manually. (take Bubble Sort for an example at /src/bubble_sort)"
        )
 
    def e_alg(self):
        """This lets user select editor for configurating algorithm."""

        f = os.path.join(SRC, self.f_alg)

        # user selects the algorithm via Input dialog
        e, ok = QInputDialog.getItem(
            self, 'Select Editor',
            'Available Editors:', list(self.e.keys()), 0, False
        )

        if ok and e:
            self.launch_editor(e, f)

    def launch_editor(self, e, dir):
        """This function is responsible for launching
        the selected editor with the algorithms folder
        """

        # should prevent error if editor does not exist
        cmd = self.e.get(e)
        if not cmd:
            QMessageBox.warning(self, 'Error', f'Editor {e} not configured!')
            return

        # the newly created process that is responsible for opening editor
        # either via terminal or in a folder
        try:
            p = QProcess()
            cmd = [part if part != '.' else dir for part in cmd]
            p.startDetached(cmd[0], cmd[1:])

        except Exception as e:
            QMessageBox.critical(
                self, 'Error',
                f'Failed to launch {e}:\n{str(e)}'
            )

    def m_alg(self):
        """This function executes a makefile for a selected algorithm"""

        f = os.path.join(SRC, self.f_alg)
        if not os.path.exists(f):
            QMessageBox.warning(self, "Error", f"Folder not found: {f}")
            return

        # process that is responsible for executing the makefile
        self.mkp = QProcess(self)
        self.mkp.setWorkingDirectory(f)
        self.mkp.finished.connect(self.mk_r)
        self.mkp.start("make")

    def mk_r(self, ec, es):
        """This function outputs the result of the make"""

        if ec == 0:
            QMessageBox.information(self, "OK", "Build succeeded!")
        else:
            err = self.mkp.readAllStandardError().data().decode()
            QMessageBox.critical(self, "Fail",
                                f"Build failed with error:\n\n{err}")

    def d_alg(self):
        """This function deletes selected algorithm.
        The functions, that are reserved (built-in), cannot be deleted.
        Uses double confirmation (pretty much like deleting github repositary)
        in case of accidental click.
        """

        if self.alg_sel in RES_ALG:
            QMessageBox.warning(self, "Cannot Delete",
                              f"'{self.alg_sel}' is a reserved algorithm and cannot be deleted.")
            return

        # double confirm
        c, ok = QInputDialog.getText(
            self,
            "Confirm Deletion",
            f"Type the algorithm name to confirm deletion:\n'{self.alg_sel}'",
            QLineEdit.Normal
        )

        if not ok or c != self.alg_sel:
            return  # user canceled or did not type correctly
        
        # loading the custom algorithms and deleting the specific one
        cst_alg = ld_alg()
        u_alg = [
            algo for algo in cst_alg
            if algo["name"] != self.alg_sel
        ]

        # delete path and if success, save the updated algorithms to JSON
        f = os.path.join(SRC, self.f_alg)
        try:
            if os.path.exists(f):
                import shutil
                shutil.rmtree(f)
        except Exception as e:
            QMessageBox.critical(
                self, "Deletion Error",
                f"Could not delete folder:\n{f}\nError: {str(e)}"
            )
            return
        sv(u_alg)

        QMessageBox.information(
            self, "Success",
            f"Algorithm '{self.alg_sel}' and its files were deleted."
        )

        # reset ui
        self.s_alg_btns()
        self.alg_sel = "Bubble Sort"  # default selection (since it is reserved and cannot be deleted)
        self.sel_a(self.alg_sel)

    def s_comp_a(self):
        """This function initializes components for
        complexity analysis.
        """

        self.ca = ComplexityAnalyzer()
        self.at = QThread()
        self.ca.moveToThread(self.at)
        
        # connect the signals and start the thread
        self.ca.a_s.connect(self.a_s)
        self.ca.a_f.connect(self.a_f)
        self.ca.e_o.connect(self.a_e)
        self.ui.determineComplexityButton.clicked.connect(self.cmpx)
        self.at.start()

    def clr_op(self):
        """This function terminates all ongoing operations,
        that is: visualization and complexity analysis
        """

        self.sp_vis()
        self.s_cmpx()
        self.clr_pa()
        self.rst_ui()

    def sp_vis(self):
        """This function stops the sorting visualization thread and resources"""

        if hasattr(self, 'vis'):
            if hasattr(self.vis, 'ani') and self.vis.ani:
                if hasattr(self.vis.ani, 'es') and self.vis.ani.es:
                    self.vis.ani.es.stop()
            self.vis.ani = None
            self.vis.fs()

            if hasattr(self, 'vis_t'):
                self.vis_t.quit()

    def s_cmpx(self):
        """This function stops the complexity analysis thread and its resources"""

        if hasattr(self, 'ca') and hasattr(self, 'at'):
            self.at.quit()

         
    def clr_pa(self):
        """This function clears the matplotlib figure"""

        self.f.clear()
        self.c.draw()

    def rst_ui(self):
        """This function clears the status label"""

        self.ui.statusLabel.setText("")

    def cmpx(self):
        """This function is the entry point to the algorithm complexity analysis.
        Before that it terminates already existing threads.
        """

        # .so exists
        if not self.lib_e():
            return

        # clear ongoing visualisation (if exists) and 
        self.clr_op()
        QTimer.singleShot(200, self.s_ca)


    def s_ca(self):
        """This function does the actual complexity analysis."""

        lib_path = os.path.join(SRC, self.f_alg, f"{self.f_alg}.so")

        # analysis start
        self.ca.an_alg(
            lib_path,
            self.e_p_alg,
            self.alg_sel,
            self
        )

    def a_s(self, message):
        """This function updates the UI on start of complexity analalysis"""

        self.ui.statusLabel.setText(f"Analyzing {self.alg_sel}...")

    def a_f(self, results):
        """This function updates the UI on completing the analysis"""

        self.ui.statusLabel.setText(
            f"{self.alg_sel}\n"
            f"Time: {results['time_complexity']}\n"
            f"Space: {results['space_complexity']}"
        )

    def a_e(self, error):
        """This function updates the UI on error during the analysis"""

        QMessageBox.critical(self, "Analysis Error", error)
        self.ui.statusLabel.setText(f"Analysis failed for {self.alg_sel}")

    def s_vis(self):
        """This function initializes components for visualization"""

        self.vis = SortingVisualizer()
        self.vis_t = QThread()
        self.vis.moveToThread(self.vis_t)

        # connect the signals and start the thread
        self.vis.vs.connect(self.ovis_s)
        self.vis.vf.connect(self.ovis_f)
        self.vis.eo.connect(self.ovis_e)
        self.ui.visualizeButton.clicked.connect(self.vis_s)
        self.vis_t.start()

    def lib_e(self):
        """This function checks if .so file exists for selected algorithm"""

        lib_path = Path(os.path.join(SRC, self.f_alg, f"{self.f_alg}.so"))
        if not lib_path.exists():
            QMessageBox.warning(
                self, "Library Not Found",
                f"Shared library not found at:\n{lib_path}\n"
                "Please build the algorithm first using the 'Make' button."
            )
            return False
        return True

    def vis_s(self):
        """This function is the entry point for visualization.
        It passes arguments (path, entry point, 
        and selected array size based on the slider)
        to start the visualization process.
        """

        self.clr_op()
        if not self.lib_e():
            return
        arr_s = self.ui.arraySizeSlider.value()
        p = Path(os.path.join(SRC, self.f_alg, f"{self.f_alg}.so"))

        self.vis.vis(
            p,
            self.e_p_alg,
            arr_s,
            self
        )

    def ovis_s(self, msg):
        """This function updates the UI on start of visualization."""

        self.ui.statusLabel.setText(msg)

    def ovis_f(self):
        """This function updates the UI on completing the visualization."""

        self.ui.statusLabel.setText(f"Visualization for {self.alg_sel}")

    def ovis_e(self, err):
        """This function updates the UI on error during the visualization."""

        QMessageBox.critical(self, "Visualization Error", err)
        self.ui.statusLabel.setText(f"Visualization failed for {self.alg_sel}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())