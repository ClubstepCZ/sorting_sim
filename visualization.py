import ctypes
import numpy as np
from PySide6.QtCore import QObject, Signal
from pathlib import Path
from matplotlib.animation import FuncAnimation

class SortingVisualizer(QObject):
    """This class is responsible for visualisation of a 
    specific sorting algorithm. It opens specific .so file,
    with algorithm binary. The C code uses macros (SWAP and TRACK_CHANGE),
    which are detected and saved within the frames.
    SWAPS are visualized using red color.
    CHANGES are visualized using blue color.
    The frames of the changes are being played via mathplotlib animation.
    The class does not check the correct usage of the macros and if the array is sorted correctly.
    """
    vs = Signal(str)
    vf = Signal()
    eo = Signal(str)

    def __init__(self):
        super().__init__()
        self.s_lib = None
        self.i_r = False
        self.f = []
        self.cf = []
        self.arr = None
        self.ani = None
        self.mw = None

    def ld_lib(self, lp, ep):
        """This function loads the algorithm from the .so file
        and sets up the function prototypes within the .so file
        """
    
        if not Path(lp).exists():
            return False

        self.s_lib = ctypes.CDLL(str(lp))

        getattr(self.s_lib, ep).argtypes = [
            ctypes.POINTER(ctypes.c_int), ctypes.c_int
        ]
        self.s_lib.set_sorting_array.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.swp_c = ctypes.CFUNCTYPE(None, ctypes.c_size_t, ctypes.c_size_t)(self.swp_c)
        self.ch_c = ctypes.CFUNCTYPE(None, ctypes.c_size_t, ctypes.c_int)(self.ch_c)
        self.s_lib.set_swap_callback(self.swp_c)
        self.s_lib.set_change_callback(self.ch_c)

        return True

    def swp_c(self, i, j):
        """This function works as a callback function 
        when detecting SWAPS within the .so file,
        colors all columns gray but those which are part of the swap
        these are colored red.
        """

        if self.i_r: # is running
            self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

            colors = ['gray'] * len(self.arr)
            colors[i] = 'red'
            colors[j] = 'red'

            self.f.append(self.arr.copy())
            self.cf.append(colors)

    def ch_c(self, i, nw):
        """This function works as a callback function 
        when detecting CHAGNES within the .so file,
        colors all columns gray. The color of the column with
        the change is colored blue. 
        (can be used if there are swaps using helping array e.g. merge sort)
        Stores the new value as well.
        """
        if self.i_r: # is running
            self.arr[i] = nw
            colors = ['gray'] * len(self.arr)
            colors[i] = 'blue'

            self.f.append(self.arr.copy())
            self.cf.append(colors)

    def vis(self, lp, ep, arr_s, mw):
        """This function is an entry point of the visualization.
        Sets up the .so library and creates the first frame (all columns being gray).
        Depending on the slider value creates the random array where if sorted all values
        are +1 than the previous starting on 1 (e.g. for array size 100 if sorted
        it is 1, 2, 3, 4, ..., 98, 99, 100)
        """
        self.fs()

        if self.i_r:
            self.eo.emit("Vis running..")
            return

        self.mw = mw
        self.i_r = True
        self.f = []
        self.cf = []
        

        if not self.ld_lib(lp, ep):
            self.eo.emit(f"Lib not found at {lp}\nPlease, make first.")
            return

        # random array with init frame
        self.arr = np.random.permutation(np.arange(1, arr_s + 1)).astype(np.int32)
        arr_ptr = (ctypes.c_int * len(self.arr))(*self.arr)
        self.f.append(self.arr.copy())
        self.cf.append(['gray'] * len(self.arr))
        
        self.ff()
        self.vs.emit(f"Visualizing {ep}")
        getattr(self.s_lib, ep)(arr_ptr, len(self.arr))
        self.anim(arr_s)

    def ff(self):
        """This function inicializes the first frame of the algorithm.
        And prints it out using mathplotlib.
        """
        self.mw.f.clear()
        self.ax = self.mw.f.add_subplot(111)

        self.bar = self.ax.bar(
            range(len(self.f[0])),
            self.f[0],
            color=self.cf[0],
            width=0.8
        )
        self.ax.set_title(f"{self.mw.alg_sel} Visualization")
        self.ax.set_xlim(-0.5, len(self.f[0])-0.5)
        self.ax.set_ylim(0, max(self.f[0]) + 1)
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.mw.c.draw()

    def anim(self, arr_s):
        """This function creates the matplotlib animation,
        uses captured frames via callback functions with changes.
        (each frame of array is one animation frame - obviously)
        """
        if not self.f or not self.cf:
            self.eo.emit("No frames available for animation.")
            self.i_r = False
            return

        def update(fi):
            """Update anim."""

            if fi >= len(self.f):
                return self.bar

            for rect, height, color in zip(
                self.bar,
                self.f[fi],
                self.cf[fi]
            ):
                rect.set_height(height)
                rect.set_color(color)

            self.ax.set_title(
                f"Step {fi + 1} of {len(self.f)}"
            )
            return self.bar

        # calculation for an animation speed
        bi = 150
        min_s = 10
        sf = max(1, (arr_s / min_s))
        di = max(10, bi / sf)

        self.ani = FuncAnimation(
            self.mw.f,
            update,
            frames=len(self.f),
            interval=di,
            blit=False,
            repeat=False
        )
        self.mw.c.draw_idle()
        self.vf.emit()

    def fs(self):
        """This function forces animation to stop and cleans up the resources"""
        if self.i_r:
            self.i_r = False
            if self.ani and hasattr(self.ani, 'es') and self.ani.es:
                self.ani.es.stop()

            # Force unload library
            if hasattr(self, 's_lib') and self.s_lib:
                import _ctypes
                _ctypes.dlclose(self.s_lib._handle)
                self.s_lib = None

            self.f = []
            self.cf = []
            self.ani = None
            self.s_lib = None
            self.arr = None
            self.ax = None
            self.bar = None

            self.vf.emit()
            
