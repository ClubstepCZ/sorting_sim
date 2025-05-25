import ctypes
import random
import numpy as np
from sklearn.metrics import r2_score
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QTimer
import _ctypes

class ComplexityAnalyzer(QObject):
    """This class is responsible for determiting complexity.
    Runs total of 10 tests and based on results 
    (which basicily are points in a plane, where x is input size
    and y is number of elementary operations). Then it compares to existing
    models and projects the best result (models being functions).
    The class does not check the correct usage of the macros and if the array is sorted correctly.
    """
    # signaling progess
    a_s = Signal(str)
    a_f = Signal(dict)
    e_o = Signal(str)

    def __init__(self):
        super().__init__()
        self.s_lib = None 
        self.i_r = False

    def o_1(self, n):
        return np.ones_like(n)

    def o_log_n(self, n):
        return np.log2(n)

    def o_n(self, n):
        return n

    def o_n_log_n(self, n):
        return n * np.log2(n)
    
    def o_n2(self, n):
        return n**2

    def o_n3(self, n):
        return n**3

    def comp_mods(self):
        """This function asigns for specific time / space complexity
        their coresponding functions.
        """

        return {
            "O(1)": self.o_1,
            "O(log n)": self.o_log_n,
            "O(n)": self.o_n,
            "O(n log n)": self.o_n_log_n,
            "O(n^2)": self.o_n2,
            "O(n^3)": self.o_n3,
        }

    def ld_lib(self, lp, ep):
        """This function loads the algorithm from the .so file
        and sets up the function prototypes within the .so file
        """

        if not Path(lp).exists():
            return False

        self.s_lib = ctypes.CDLL(lp)

        getattr(self.s_lib, ep).argtypes = [
            ctypes.POINTER(ctypes.c_int), ctypes.c_int
        ]
        self.s_lib.set_sorting_array.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.s_lib.get_peak_memory_usage.restype = ctypes.c_size_t
        self.s_lib.get_peak_stack_usage.restype = ctypes.c_size_t
        self.s_lib.reset_peak_memory_usage.argtypes = []
        self.s_lib.reset_peak_stack_usage.argtypes = []
        self.s_lib.reset_operation_count.argtypes = []
        self.s_lib.get_operation_count.restype = ctypes.c_size_t
        return True

    def cmp_a(self, ep, ss=50, st=50, t=10):
        """This function is responsible 
        for running the compelxity analysis. 
        For each testing size computes the number 
        of elementary operations
        """

        if not self.s_lib:
            self.e_o.emit("Library not loaded")
            return None

        sz = []
        el_op = []
        hu = []
        su = []

        for i in range(t):
            s = ss + i * st
            ta = [random.randint(0, 1000) for _ in range(s)]
            act = (ctypes.c_int * len(ta))(*ta) # python arr to c like arr 

            # res cnt, run sort 
            self.s_lib.set_sorting_array(act)
            self.s_lib.reset_peak_memory_usage()
            self.s_lib.reset_peak_stack_usage()
            self.s_lib.reset_operation_count()
            getattr(self.s_lib, ep)(act, len(ta))

            sz.append(s)
            el_op.append(self.s_lib.get_operation_count())
            hu.append(self.s_lib.get_peak_memory_usage())
            su.append(self.s_lib.get_peak_stack_usage())

        return (
            np.array(sz),
            np.array(el_op),
            np.array(hu),
            np.array(su)
        )

    def ev_m(self, s, m):
        """This function evaluates which model 
        fits the best for the test set.
        """
    
        cm = self.comp_mods()
        bm = None
        br2 = -np.inf

        # had issues when all results were 0  
        # (for space complex mainly since it is nearly impossible to sort array in 0 steps 10 times in a row)
        if np.all(m == 0):
            return "O(1)", 1.0 # 1.0 being perfect fit

        vm = (m >= 0) & np.isfinite(m)
        if not np.any(vm): # all results are bad somehow (did not happen for me)
            return "O(1)", -np.inf

        s = s[vm]
        m = m[vm]

        for nm, md in cm.items():
            X = md(s)
            X_n = X / X.max()
            mn = m / m.max()

            # least squares method and prediction
            c = np.linalg.lstsq(
                X_n[:, np.newaxis], 
                mn, 
                rcond=None
            )[0]
            pred = c * X_n

            r2 = r2_score(mn, pred)
            if r2 > br2: # new model fits better
                br2 = r2
                bm = nm

        if bm is None:
            return "O(1)", -np.inf

        return bm, br2

    def dsm(self, hm, sm):
        """This funciton determines whether stack size model 
        has higher rank or heap size (peak malloc)
        """

        ord = {
            "O(1)": 0,
            "O(log n)": 1,
            "O(n)": 2,
            "O(n log n)": 3,
            "O(n^2)": 4,
            "O(n^3)": 5
        }
        hr = ord.get(hm, 0)
        sr = ord.get(sm, 0)
        return hm if hr > sr else sm

    def plt(self, sz, ops,
            tm, sm, sl, sd,
            alg, mw):
        """This function plots the results using the widget on the main window"""

        mw.f.clear()

        # time
        ax1 = mw.f.add_subplot(121)
        ax1.plot(sz, ops, 'bo-', markersize=5, label=f"Operations (Best fit: {tm})")
        ax1.set_title(f"Time complexity - {alg}")
        ax1.set_xlabel("Array Size")
        ax1.set_ylabel("Elementary Operations")
        ax1.grid(True)
        ax1.legend()

        # space
        ax2 = mw.f.add_subplot(122)

        col = 'go-' if sl == "Heap" else 'ro-'
        yl = "Heap Memory (bytes)" if sl == "Heap" else "Func. Call Stack Depth"

        ax2.plot(sz, sd, col, markersize=5,
                 label=f"{sl} Usage (Best Fit: {sm})")
        ax2.set_title(f"Space Complexity - {alg}")
        ax2.set_xlabel("Array Size")
        ax2.set_ylabel(yl)
        ax2.grid(True)
        ax2.legend()

        mw.f.tight_layout()
        mw.c.draw()

    def an_alg(self, lp, ep, alg_n, mw):
        """This function is an entry point of the algorithm analysis.
        In case already running analysis, it gets stopped. 
        """
        if self.i_r:
            self.e_o.emit("Stop prev...")
            self.i_r = False
        if hasattr(mw, 'vis') and mw.vis.i_r: 
            mw.vis.fs()

        self.i_r = True
        self.a_s.emit(f"Start new...")

        if not self.ld_lib(lp, ep):
            self.e_o.emit(f".so not found at {lp}\nPlease use Make.")
            return

        # tests with res
        res = self.cmp_a(ep)
        if not res:
            return

        sz, ops, heap, stack = res

        tm, tr2 = self.ev_m(sz, ops)
        hm, hr2 = self.ev_m(sz, heap)
        skm, sr2 = self.ev_m(sz, stack)
        sem = self.dsm(hm, skm)

        if sem == skm:
            sdata = stack
            slbl = "Stack"

        else:
            sdata = heap
            slbl = "Heap"

        self.plt(sz, ops,
                 tm, sem, slbl, sdata,
                 alg_n, mw)

        self.a_f.emit({
            'time_complexity': tm,
            'heap_complexity': hm,
            'stack_complexity': skm,
            'space_complexity': sem,
            'time_r2': tr2,
            'heap_r2': hr2,
            'stack_r2': sr2
        })
        self.i_r = False
        self.unload_lib()

    def unload_lib(self):
        """This function unloads the shared library from memory."""
        if self.s_lib:
            _ctypes.dlclose(self.s_lib._handle)
            self.s_lib = None
