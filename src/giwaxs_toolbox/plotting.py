import logging
import os
from pathlib import Path

import h5py
import ipywidgets as wg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# from matplotlib import cm as mpl_cm
from IPython.display import display
from ipywidgets import fixed, interact
from matplotlib.colors import LogNorm, Normalize

from giwaxs_toolbox.processing import data_loader, result1d, result2d

# logger = logging.getLogger(__name__)
# logpath = Path("/dls/science/users/rpy65944/I07_work/MINERVA_analysis/")
# logging.basicConfig(
#     filename=str(logpath / "testlog.log"), encoding="utf-8", level=logging.DEBUG
# )
# logging.getLogger("matplotlib").disabled = True


def get_logger(folderpath, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:  # <- prevents duplicate handlers
        file_handler = logging.FileHandler(folderpath / f"{name}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)
    # --- Silence third‑party libraries ---
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("h5py").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    return logger


def plot_2d_map(loaded_data, loaded_axis, filename, fig, ax, logscale, axlabels):
    map2d = loaded_data
    q_para, q_perp = loaded_axis
    cm = "viridis"
    vmax, vmin = None, None
    limits = None
    extent = [q_para.min(), q_para.max(), q_perp.min(), q_perp.max()]
    if vmax is None:
        vmax = np.mean(map2d) + 2 * np.std(map2d)
    if vmin is None:
        vmin = np.max(np.array([map2d.min(), 0.01]))
    if logscale:
        normvals = LogNorm(vmin=vmin, vmax=vmax)
    else:
        normvals = Normalize(vmin=vmin, vmax=vmax)
    im = ax.imshow(
        map2d,
        cmap=cm,
        extent=extent,
        norm=normvals,
        aspect=1,
    )
    if limits is not None:
        ax.set_xlim(limits[0], limits[1])
        ax.set_ylim(limits[2], limits[3])
    ax.set_title(filename)
    ax.set_xlabel(axlabels[0])
    ax.set_ylabel(axlabels[1])
    fig.colorbar(im, ax=ax, location="right")
    ax.set_aspect("auto")
    return fig


def plot_1d_profile(
    loaded_data, loaded_axis, filename, fig, ax, logscale, axlabels, label=None
):
    """
    Plot a 1D intensity profile.
    """
    y_data = loaded_data
    x_data = loaded_axis
    ax.plot(x_data, y_data, label=label)
    ax.set_xlabel(axlabels[1])
    ax.set_ylabel(axlabels[0])
    ax.set_title(filename)

    qmin, qmax = None, None
    if logscale:
        ax.set_yscale("log")
    if qmin is not None and qmax is not None:
        ax.set_xlim(qmin, qmax)
    if label:
        ax.set_title("")
        ax.legend(loc="upper left", bbox_to_anchor=(0.1, 1.15))
    return fig


# ===needed to refresh interactive plots when switching between plotters
def reset_plots():
    plt.close("all")
    wg.Widget.close_all()


# === note this extra wrapper class is needed to allow the plotting to refesh properly when switching between different active plots
class individual_plotter:
    def __init__(self, datafolder: str):
        reset_plots()
        self.datafolder = Path(datafolder)
        self.plot_list_data()

    def plot_list_data(self):
        list_plotter_multi = ind_list_plotter(self.datafolder)
        list_plotter_multi.create_plot()


class ind_list_plotter:
    def __init__(self, folderpath):
        reset_plots()
        self._updating = False
        self.folderpath = folderpath
        self.loader = data_loader(folderpath)

        # self.logger = self.logger = get_logger(
        #     self.folderpath, name=f"ind_list_plotter_{id(self)}"
        # )

    def get_files(self):
        return [
            f
            for f in os.listdir(self.folderpath)
            if (self.scantype in f) and (f.endswith(".hdf5"))
        ]

    def set_plot_callback(self):
        callback_dict = {
            "IvsQ": self._plot_ivsq,
            "IvsQ_heatmap": self._plot_ivsq_heatmap,
            "Qmap": self._plot_qmap,
            "exitmap": self._plot_exitmap,
            "Chimap": self._plot_chimap,
            "IvsChi": self._plot_ivschi,
        }
        self._plot_callback = callback_dict[self.scantype]

    def set_dataloader(self):
        loaders_dict = {
            "IvsQ": self.loader.get_ivsq,
            "IvsQ_heatmap": self.loader.get_ivsq_heatmap,
            "Qmap": self.loader.get_qmap,
            "exitmap": self.loader.get_exitmap,
            "Chimap": self.loader.get_chimap,
            "IvsChi": self.loader.get_ivschi,
        }
        self._dataloader = loaders_dict[self.scantype]

    def set_scantype(self, scantype, heatmap):

        self.scantype = scantype
        self.filelist = self.get_files()

        types1d = ["IvsQ"]  # ,"IvsChi"]
        if heatmap and (scantype in types1d):
            self.scantype = f"{scantype}_heatmap"
        self.set_plot_callback()
        self.set_dataloader()

    def _plot_chimap(
        self, data_result: result2d, filename: str, fig, ax, logscale: bool
    ):
        axlabelx = data_result.x_unit or "$q_{total}$  [Å⁻¹]"
        axlabely = data_result.y_unit or "$Chi$  [deg]"
        axlabels = [axlabelx, axlabely]
        return plot_2d_map(
            data_result.data,
            [data_result.x_axis, data_result.y_axis],
            filename,
            fig,
            ax,
            logscale,
            axlabels,
        )

    def _plot_qmap(self, data_result: result2d, filename: str, fig, ax, logscale: bool):
        axlabelx = data_result.x_unit or "$q_{para}$  [Å⁻¹]"
        axlabely = data_result.y_unit or "$q_{perp}$  [Å⁻¹]"
        axlabels = [axlabelx, axlabely]
        return plot_2d_map(
            data_result.data,
            [data_result.x_axis, data_result.y_axis],
            filename,
            fig,
            ax,
            logscale,
            axlabels,
        )

    def _plot_exitmap(
        self, data_result: result2d, filename: str, fig, ax, logscale: bool
    ):
        axlabelx = data_result.x_unit or "$exitangle_{para}$  [deg]"
        axlabely = data_result.y_unit or "$exitangle_{perp}$  [deg]"
        axlabels = [axlabelx, axlabely]
        return plot_2d_map(
            data_result.data,
            [data_result.x_axis, data_result.y_axis],
            filename,
            fig,
            ax,
            logscale,
            axlabels,
        )

    def _plot_ivsq(self, data_result: result1d, filename, fig, ax, logscale):
        axlabels = ["Intensity", "Q (A^-1)"]
        return plot_1d_profile(
            data_result.data,
            data_result.x_axis,
            filename,
            fig,
            ax,
            logscale,
            axlabels,
        )

    def _plot_ivsq_heatmap(self, data_result: result1d, filename, fig, ax, logscale):
        axlabels = ["Q (A^-1)", "index1"]
        datashape = np.shape(data_result.data)
        return plot_2d_map(
            data_result.data,
            [data_result.x_axis, np.arange(datashape[0])],
            filename,
            fig,
            ax,
            logscale,
            axlabels,
        )

    def _plot_ivschi(self, data_result: result1d, filename, fig, ax, logscale):
        axlabels = ["Intensity", "Chi [Deg]"]
        return plot_1d_profile(
            data_result.data,
            data_result.x_axis,
            filename,
            fig,
            ax,
            logscale,
            axlabels,
        )

    def create_plot(self):
        # out = Output()  # persistent output area
        fig, ax = plt.subplots()
        self.heatmap1 = wg.Checkbox(
            value=False, description="heatmap for index1", disabled=False
        )
        self.set_scantype("IvsQ", self.heatmap1)
        files = wg.Dropdown(
            options=self.filelist,
            description=f"{self.scantype} files",
        )
        self.index1 = wg.IntSlider(max=10)
        self.index2 = wg.IntSlider(max=10)
        self.index1.style.handle_color = "lightblue"
        self.index2.style.handle_color = "lightblue"

        @interact(
            scantype=wg.Dropdown(
                options=["IvsQ", "IvsChi", "Qmap", "exitmap", "Chimap"],
                description="scantype",
            ),
            filename=files,
            logscale=wg.Checkbox(value=False),
            heatmap1=self.heatmap1,
            fig=fixed(fig),
            ax=fixed(ax),
            index1=self.index1,
            index2=self.index2,
        )
        def do_plot(scantype, filename, logscale, index1, index2, heatmap1):
            if self._updating:
                return
            # out.clear_output()
            self._updating = True
            self.set_scantype(scantype, heatmap1)
            if len(self.filelist) == 0:
                files.options = ["No files found"]
                fig.clear()
                self._updating = False
                return

            files.options = self.filelist
            self._updating = False
            fig.clear()
            ax = fig.add_subplot(111)
            self.index1.layout.visibility = "hidden"
            self.index2.layout.visibility = "hidden"
            # SKIP invalid combinations when interact misfires
            if filename not in self.filelist:
                filename = files.options[0]
            # h5file = self.folderpath / filename
            # with h5py.File(h5file) as data:
            result, index1, index2, indmax1, indmax2 = self._dataloader(
                filename, index1, index2
            )
            if result == "Not valid for heatmap":
                self.heatmap1.value = False
                self.heatmap1.disabled = True
            else:
                self.index1.max = indmax1
                self.index2.max = indmax2
                self.index1.layout.visibility = "hidden" if indmax1 == 0 else "visible"
                self.index2.layout.visibility = "hidden" if indmax2 == 0 else "visible"
                self.heatmap1.disabled = True if indmax1 == 0 else False
                # your existing plot functions already draw correctly
                self._plot_callback(result, filename, fig, ax, logscale)

        # display(VBox([out]))


# === note this extra wrapper class is needed to allow the plotting to refesh properly when switching between different active plots
class comparison_plotter:
    def __init__(
        self,
        datafolder: str,
    ):
        reset_plots()
        self.datafolder = Path(datafolder)

    def plot_files(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale=False,
    ):
        combo_file_plotter = combo_plotter(self.datafolder)
        combo_file_plotter.plot_files(filenames, index1vals, index2vals, logscale)


class combo_plotter:
    def __init__(
        self,
        datafolder: str,
    ):
        reset_plots()
        self.datafolder = Path(datafolder)
        self.loader = data_loader(datafolder)

    def plot_files(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale=False,
    ):
        reset_plots()
        if all(["IvsQ" in file for file in filenames]):
            self.plot_ivsq(filenames, index1vals, index2vals, logscale)
        elif all(["IvsChi" in file for file in filenames]):
            self.plot_ivschi(filenames, index1vals, index2vals, logscale)
        elif all(["Qmap" in file for file in filenames]):
            self.plot_qmap(filenames, index1vals, index2vals, logscale)
        elif all(["exitmap" in file for file in filenames]):
            self.plot_exitmap(filenames, index1vals, index2vals, logscale)
        elif all(["Chimap" in file for file in filenames]):
            self.plot_chimap(filenames, index1vals, index2vals, logscale)
        print(
            "Could not match all file types - ensure all files in the file list are of the same type, and one of the following: \n\t[IvsQ , IvsChi, Qmap, exitmap, Chimap]"
        )

    def plot_ivsq(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale: bool = False,
    ):
        # plotpaths = [self.datafolder / name for name in filenames]
        axlabels = ["Intensity", "Q (A^-1)"]
        if index1vals is None:
            index1vals = np.zeros(len(filenames)).astype(np.int32)
        if index2vals is None:
            index2vals = np.zeros(len(filenames)).astype(np.int32)

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        for file_num, file in enumerate(filenames):
            index1 = index1vals[file_num]
            index2 = index2vals[file_num]
            result, *_ = self.loader.get_ivsq(file, index1, index2)

            plot_1d_profile(
                result.data,
                result.x_axis,
                file,
                self.fig,
                self.ax,
                logscale,
                axlabels,
                label=f"{filenames[file_num]} {index1} {index2}",
            )

    def plot_ivschi(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale: bool = False,
    ):
        # plotpaths = [self.datafolder / name for name in filenames]
        axlabels = ["Intensity", "Chi [Deg]"]
        if index1vals is None:
            index1vals = np.zeros(len(filenames)).astype(np.int32)
        if index2vals is None:
            index2vals = np.zeros(len(filenames)).astype(np.int32)
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        for file_num, file in enumerate(filenames):
            index1 = index1vals[file_num]
            index2 = index2vals[file_num]
            result, *_ = self.loader.get_ivschi(file, index1, index2)

            plot_1d_profile(
                result.data,
                result.x_axis,
                file,
                self.fig,
                self.ax,
                logscale,
                axlabels,
                label=f"{filenames[file_num]} {index1} {index2}",
            )
        # fig.canvas.draw_idle()

    def plot_exitmap(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale: bool = False,
    ):
        axlabels = ["$exitangle_{para}$  [deg]", "$exitangle_{perp}$  [deg]"]
        if index1vals is None:
            index1vals = np.zeros(len(filenames)).astype(np.int32)
        if index2vals is None:
            index2vals = np.zeros(len(filenames)).astype(np.int32)
        fig, ax = plt.subplots(figsize=(10, 5))
        for file_num, filename in enumerate(filenames):
            index1 = index1vals[file_num]
            index2 = index2vals[file_num]

            result, *_ = self.loader.get_exitmap(filename, index1, index2)
            plot_2d_map(
                result.data,
                [result.x_axis, result.y_axis],
                filename,
                fig,
                ax,
                logscale,
                axlabels,
            )
        plt.tight_layout()

    def plot_qmap(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale: bool = False,
    ):

        if index1vals is None:
            index1vals = np.zeros(len(filenames)).astype(np.int32)
        if index2vals is None:
            index2vals = np.zeros(len(filenames)).astype(np.int32)
        row_num = int(np.ceil(len(filenames) / 2))
        fig, axs = plt.subplots(row_num, 2, figsize=(10, 5 * row_num))
        axlist = axs.flatten()
        for file_num, filename in enumerate(filenames):
            index1 = index1vals[file_num]
            index2 = index2vals[file_num]

            result, *_ = self.loader.get_qmap(filename, index1, index2)
            axlabelx = result.x_unit or "$q_{para}$  [Å⁻¹]"
            axlabely = result.y_unit or "$q_{perp}$  [Å⁻¹]"
            axlabels = [axlabelx, axlabely]
            plot_2d_map(
                result.data,
                [result.x_axis, result.y_axis],
                filename,
                fig,
                axlist[file_num],
                logscale,
                axlabels,
            )
        fig.tight_layout()

    def plot_chimap(
        self,
        filenames: list,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
        logscale: bool = False,
    ):

        axlabels = ["$q_{para}$  [Å⁻¹]", "$q_{perp}$  [Å⁻¹]"]
        if index1vals is None:
            index1vals = np.zeros(len(filenames)).astype(np.int32)
        if index2vals is None:
            index2vals = np.zeros(len(filenames)).astype(np.int32)
        row_num = int(np.ceil(len(filenames) / 2))
        fig, axs = plt.subplots(row_num, 2, figsize=(10, 5 * row_num))
        axlist = axs.flatten()
        for file_num, filename in enumerate(filenames):
            index1 = index1vals[file_num]
            index2 = index2vals[file_num]

            result, *_ = self.loader.get_chimap(filename, index1, index2)
            axlabelx = result.x_unit or "$q_{total}$  [Å⁻¹]"
            axlabely = result.y_unit or "$Chi$  [deg]"
            axlabels = [axlabelx, axlabely]
            plot_2d_map(
                result.data,
                [result.x_axis, result.y_axis],
                filename,
                fig,
                axlist[file_num],
                logscale,
                axlabels,
            )
        plt.tight_layout()


def plot_i07_list(dirpath: Path, scantype: str, title=None):

    folder_text = wg.Text(value=str(dirpath), layout=wg.Layout(width="100%"))

    file_list = wg.Dropdown(
        options=get_files(folder_text.value, scantype), description=f"{scantype} files"
    )

    def update_list(folder):
        if not os.path.exists(folder):
            file_list.options = ["folder not found"]
            return
        try:
            files = get_files(folder, scantype)
            file_list.options = files

            if files:
                file_list.value = None  # force trait change event
                file_list.value = files[0]

        except FileNotFoundError:
            file_list.options = []

    folder_interact = wg.interactive_output(update_list, {"folder": folder_text})

    def update_plot(filename, logscale):

        if filename in (None, "", "folder not found"):
            return

        fig, ax = plt.subplots()

        h5file = Path(folder_text.value) / filename

        with h5py.File(h5file) as data:
            outfunc, title = parse_i07_giwaxs(data, h5file.stem)
            fig, ax = outfunc(data, title, figax=[fig, ax], log=logscale)
        return fig

    log_box = wg.Checkbox(value=False, description="Log y-scale")
    plot_interact = wg.interactive_output(
        update_plot, {"filename": file_list, "logscale": log_box}
    )

    ui = wg.VBox([folder_interact, file_list, log_box, plot_interact])

    display(ui)


def plot_chi_profile(
    chi,
    intensity,
    chi_min=None,
    chi_max=None,
    logscale=False,
    title="Chi Profile",
    label=None,
):
    """
    Plot a 1D intensity profile versus chi.
    """
    plt.figure(figsize=(10, 10))
    plt.plot(chi, intensity, label=label)
    plt.xlabel("Chi (degrees)")
    plt.ylabel("Intensity")
    plt.title(title)
    if chi_min is not None and chi_max is not None:
        plt.xlim(chi_min, chi_max)
    if label:
        plt.legend()
    plt.show()


def plot_contour(csv_file, outfile, cmap="viridis", levels=100, figsize=(10, 6)):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Extract q and intensity values
    q = df.iloc[:, 0].values
    intensity = df.iloc[:, 1:].values  # shape: (n_q, n_columns)
    num_columns = intensity.shape[1]

    # X-axis: column indices
    x = np.arange(num_columns)
    y = q

    # Create meshgrid
    X, Y = np.meshgrid(x, y)

    # Plot contour
    plt.figure(figsize=figsize)
    contour = plt.contourf(X, Y, intensity, levels=levels, cmap=cmap)
    plt.xlabel("Column index")
    plt.ylabel("q [Å⁻¹]")
    # cbar = plt.colorbar(contour, label="Intensity")

    # Save figure
    plt.savefig(outfile + ".png", bbox_inches="tight")
    plt.savefig(outfile + ".pdf", bbox_inches="tight")
    plt.show()

    #     folder_text=wg.Text(value='/dls/science/groups/das/ExampleData/i07/fast_rsm_example_data/dev_2026-01-23')


def plot_i07_list_colab(dirpath: Path, scantype: str, title=None):
    """
    Colab-friendly version:
    - Avoids %matplotlib widget/ipympl
    - Uses ipywidgets.Output() for reliable redraws
    - Avoids wg.interact auto-display (returns a VBox you can display())
    - Observes changes from Text/Dropdown/Checkbox instead of using interact
    """

    # --- Controls ---
    folder_text = wg.Text(
        value=str(dirpath), description="Folder", layout=wg.Layout(width="100%")
    )

    # initial file list
    try:
        initial_options = get_files(folder_text.value, scantype)
        if not initial_options:
            initial_options = ["<no files>"]
    except FileNotFoundError:
        initial_options = ["<folder not found>"]

    file_list = wg.Dropdown(
        options=initial_options,
        description=f"{scantype} files",
        layout=wg.Layout(width="60%"),
    )
    log_box = wg.Checkbox(value=False, description="Log y-scale")

    # Where plots go
    out = wg.Output(layout=wg.Layout(border="1px solid #ddd"))

    # --- Helpers ---
    def _safe_files(folder_str: str):
        """Refresh the file dropdown safely for a new folder."""
        if not os.path.exists(folder_str):
            return ["<folder not found>"]
        try:
            files = get_files(folder_str, scantype)
            return files if files else ["<no files>"]
        except FileNotFoundError:
            return ["<no files>"]

    # --- Observers / Callbacks ---
    def on_folder_change(change):
        new_folder = change["new"]
        file_list.options = _safe_files(new_folder)
        # If the new options are non-empty strings, set value to first
        if isinstance(file_list.options, (list, tuple)) and file_list.options:
            file_list.value = file_list.options[0]

    folder_text.observe(on_folder_change, names="value")

    def draw_plot():
        """(Re)draw the plot for current selections inside Output()."""
        filename = file_list.value
        if filename in ("<no files>", "<folder not found>", None):
            with out:
                out.clear_output(wait=True)
                print("No valid file to display.")
            return

        folder_path = Path(folder_text.value)
        h5file = folder_path / filename

        with out:
            out.clear_output(wait=True)
            # fresh figure for each draw (most reliable in Colab)
            fig, ax = plt.subplots(1, 1, figsize=(6, 3), dpi=100)
            try:
                with h5py.File(h5file, "r") as data:
                    outfunc, the_title = parse_i07_giwaxs(data, h5file.stem)
                    outfunc(
                        data,
                        the_title if title is None else title,
                        figax=[fig, ax],
                        log=log_box.value,
                    )
                plt.tight_layout()
                plt.show()
            except FileNotFoundError:
                print(f"File not found: {h5file}")
            except Exception as e:
                # Don't crash the widget; show the error in the output pane
                print(f"Error while plotting {h5file}:\n{e}")

    def on_file_change(change):
        draw_plot()

    def on_log_change(change):
        draw_plot()

    file_list.observe(on_file_change, names="value")
    log_box.observe(on_log_change, names="value")

    # Initial draw (if possible)
    draw_plot()

    # --- Layout ---
    controls = wg.HBox([file_list, log_box])
    ui = wg.VBox([folder_text, controls, out])
    return ui


def view_2D_image(img_data, cmap="viridis", flip_vertical=False, flip_horizontal=False):
    # Load Fabio image
    data = np.flipud(img_data.astype(float))

    # Optional flipping
    if flip_vertical:
        data = np.flipud(data)
    if flip_horizontal:
        data = np.fliplr(data)

    # Basic stats
    dmin, dmax = np.nanmin(data), np.nanmax(data)

    # Widgets -------------------------------------------------------------------

    vmin_slider = wg.FloatSlider(
        min=dmin,
        max=dmax,
        value=dmin,
        description="Min",
        continuous_update=False,
        readout=False,
    )
    vmax_slider = wg.FloatSlider(
        min=dmin,
        max=dmax,
        value=dmax,
        description="Max",
        continuous_update=False,
        readout=False,
    )

    vmin_text = wg.FloatText(value=dmin)
    vmax_text = wg.FloatText(value=dmax)

    log_box = wg.Checkbox(value=False, description="Log scale")

    # Sync slider <->  text ------------------------------------------------------

    def sync_vmin_slider(change):
        vmin_text.value = change["new"]

    vmin_slider.observe(sync_vmin_slider, names="value")

    def sync_vmin_text(change):
        if change["new"] <= vmax_slider.value:
            vmin_slider.value = change["new"]

    vmin_text.observe(sync_vmin_text, names="value")

    def sync_vmax_slider(change):
        vmax_text.value = change["new"]

    vmax_slider.observe(sync_vmax_slider, names="value")

    def sync_vmax_text(change):
        if change["new"] >= vmin_slider.value:
            vmax_slider.value = change["new"]

    vmax_text.observe(sync_vmax_text, names="value")

    # Update function -----------------------------------------------------------

    def update(vmin, vmax, logscale):
        plt.figure(figsize=(7, 7))

        if logscale:
            # Avoid non-positive values for LogNorm
            safe_data = np.clip(data, a_min=1e-12, a_max=None)
            norm = LogNorm(vmin=max(vmin, 1e-12), vmax=vmax)
            plt.imshow(safe_data, cmap=cmap, norm=norm)
        else:
            plt.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)

        plt.colorbar(label="Intensity")
        plt.axis("off")
        plt.show()

    # Connect widgets  to updater
    out = wg.interactive_output(
        update, {"vmin": vmin_slider, "vmax": vmax_slider, "logscale": log_box}
    )

    # Layout --------------------------------------------------------------------

    layout = wg.VBox(
        [
            wg.HBox([wg.Label(""), vmin_slider, vmin_text]),
            wg.HBox([wg.Label(""), vmax_slider, vmax_text]),
            log_box,
            out,
        ]
    )

    display(layout)


def remove_colorbars(fig):
    for ax in fig.axes:
        if ax.get_label() == "colorbar":
            ax.remove()


def remove_axes(fig):
    for ax in fig.axes:
        fig.delaxes(ax)


if __name__ == "__main__":
    ind_plotter = individual_plotter(
        datafolder="/dls/science/users/rpy65944/I07_work/MINERVA_analysis/MINERVA_training/example_data"
    )
    ind_plotter.plot_qmap()
