# import pyFAI


# print("Using pyFAI verison: ", pyFAI.version)


from dataclasses import dataclass
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import (
    GaussianModel,
    LinearModel,
    LorentzianModel,
    PseudoVoigtModel,
    SkewedGaussianModel,
    SplitLorentzianModel,
)

# logger = logging.getLogger(__name__)
# logpath = Path("/dls/science/users/rpy65944/I07_work/MINERVA_analysis/")
# logging.basicConfig(
#     filename=str(logpath / "testlog.log"), encoding="utf-8", level=logging.DEBUG
# )

# logging.getLogger("matplotlib").disabled = True


def parse_peak_kwargs(peakinfo, prefix):
    outparams = []
    for k, v in peakinfo.items():
        outparams.append([f"{prefix}{k}", v[0], v[1], v[2]])
    return outparams


def peakfit_and_plot(peaklist, x, y):
    # pars += peak2.guess(y, x=x)

    result, comps, y_fit, xnew = fit_peaks(peaklist, x, y)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(8, 4), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    # ax1.plot(x, y, "k.", ms=3, label="Data")
    # ax1.plot(x, y_fit, "r-", lw=2, label="Total fit")
    result.plot_fit(ax=ax1)

    # individual components
    ax1.plot(
        xnew, comps["bkg_"], color="tab:blue", ls="--", lw=2, label="Background (bkg_)"
    )
    for pnum in np.arange(len(peaklist)) + 1:
        ax1.plot(
            xnew,
            comps[f"p{pnum}_"],
            color="tab:green",
            lw=2,
            label=f"Peak {pnum} (p{pnum}_)",
        )
    ax1.legend()
    result.plot_residuals(ax=ax2)
    plt.tight_layout()
    # plt.show()

    return result


# peak2 = fit_models[fit_type](prefix='p2_')
def fit_peaks(peaklist: list, x: np.ndarray, y: np.ndarray, background=None):

    fit_models = {
        "pvoigt": PseudoVoigtModel,
        "gaussian": GaussianModel,
        "lorentzian": LorentzianModel,
        "split_lorentzian": SplitLorentzianModel,
        "skewed_gaussian": SkewedGaussianModel,
    }
    if background is None:
        background = LinearModel(prefix="bkg_")
    mod = background
    par_settings = []
    for ind, peak in enumerate(peaklist):
        peakprefix = f"p{ind + 1}_"
        mod += fit_models[peak["type"]](prefix=peakprefix)
        par_settings += parse_peak_kwargs(peak["settings"], peakprefix)

    pars = mod.make_params()

    pars["bkg_intercept"].set(y.min())
    pars["bkg_slope"].set(10)
    for par in par_settings:
        pars[par[0]].set(par[1], min=par[2], max=par[3])
    result = mod.fit(y, pars, x=x)
    xnew = np.arange(x.min(), x.max(), 0.001)
    comps = result.eval_components(x=xnew)
    y_fit = result.best_fit

    return result, comps, y_fit, xnew


@dataclass
class result2d:
    data: np.ndarray
    x_axis: np.ndarray
    y_axis: np.ndarray
    x_unit: str | None = None
    y_unit: str | None = None


@dataclass
class result1d:
    data: np.ndarray
    data_name: str
    x_axis: np.ndarray
    x_axis_name: str
    x2_axis: np.ndarray | None = None
    x2_axis_name: str | None = None


def check_shape(inshape, expected_shape, index1, index2):

    if len(inshape) == expected_shape:
        ind0max = np.int32(0)
        ind1max = np.int32(0)
        outind = slice(None)

    if len(inshape) == expected_shape + 1:
        ind0max = inshape[0] - 1
        ind1max = np.int32(0)
        if index1 > ind0max:
            index1 = np.int32(0)
        outind = (index1, slice(None))

    if len(inshape) == expected_shape + 2:
        ind0max = inshape[0] - 1
        ind1max = inshape[1] - 1
        if index1 > ind0max:
            index1 = np.int32(0)
        if index2 > ind1max:
            index2 = np.int32(0)
        outind = (index1, index2, slice(None))

    return outind, index1, index2, ind1max, ind0max


class data_loader:
    def __init__(self, datafolder: str):
        self.datafolder = Path(datafolder)

    def get_1d_data(self, data, paths, dataind, axisind):
        y_out = data[paths[0]][dataind]
        x_out = data[paths[1]][axisind]
        x_out_name = paths[1]
        y_out_name = paths[0]
        return result1d(
            data=y_out, x_axis=x_out, data_name=y_out_name, x_axis_name=x_out_name
        )

    def get_2d_data(self, data, paths, dataind, axisind):
        dataout = data[paths[0]][dataind]
        para_out = data[paths[1]][axisind]
        perp_out = -1 * data[paths[2]][axisind]
        para_unit = data[paths[1] + "_unit"][()].decode("utf-8")
        perp_unit = data[paths[2] + "_unit"][()].decode("utf-8")

        return result2d(
            data=dataout,
            x_axis=para_out,
            y_axis=perp_out,
            x_unit=para_unit,
            y_unit=perp_unit,
        )

    def read_1d_datafile(
        self,
        filepath: Path,
        paths: list,
        index1: np.int32 | tuple,
        index2: np.int32 | tuple,
    ):
        with h5py.File(filepath) as h5data:
            y_shape = np.shape(h5data[paths[0]])
            x_shape = np.shape(h5data[paths[1]])
            expected_shape = np.int32(1)
            dataind, index1, index2, indmax2, indmax1 = check_shape(
                y_shape, expected_shape, index1, index2
            )
            axisind, *_ = check_shape(x_shape, expected_shape, index1, index2)
            result = self.get_1d_data(h5data, paths, dataind, axisind)
        return result, index1, index2, indmax1, indmax2

    def read_1dbatch_datafile(
        self,
        filepath: Path,
        paths: list,
        index1: np.int32 | tuple | None,
        index2: np.int32 | tuple | None,
    ):
        with h5py.File(filepath) as h5data:
            y_shape = np.shape(h5data[paths[0]])
            x_shape = np.shape(h5data[paths[1]])
            expected_shape = np.int32(1)
            dataind, index1, index2, indmax2, indmax1 = check_shape(
                y_shape, expected_shape, 0, index2
            )
            axisind, *_ = check_shape(x_shape, expected_shape, 0, index2)
            if len(y_shape) == 3:
                outslice = (slice(None), index2, slice(None))
            elif len(y_shape) == 2:
                outslice = (slice(None), slice(None))
            elif len(y_shape) == 1:
                return "Not valid for heatmap", index1, index2, indmax1, indmax2
            result = self.get_1d_data(h5data, paths, outslice, ())
        return result, index1, index2, indmax1, indmax2

    def read_2d_datafile(
        self,
        filepath: Path,
        map_namestring: str,
        index1: np.int32 | None,
        index2: np.int32 | None,
    ):
        if index1 is None:
            index1 = np.int32(0)
        if index2 is None:
            index2 = np.int32(0)
        mappath = f"{map_namestring}/{map_namestring}_map"
        para_path = f"{map_namestring}/map_para"
        perp_path = f"{map_namestring}/map_perp"
        with h5py.File(filepath) as h5data:
            map2d_shape = np.shape(h5data[mappath])
            para_shape = np.shape(h5data[para_path])
            perp_shape = np.shape(h5data[perp_path])
            assert len(para_shape) == len(perp_shape)

            dataind, index1, index2, indmax2, indmax1 = check_shape(
                map2d_shape,
                np.int32(2),
                index1,
                index2,
            )

            axisind, *_ = check_shape(
                np.array([para_shape, perp_shape]),
                np.int32(2),
                index1,
                index2,
            )

            result = self.get_2d_data(
                h5data, [mappath, para_path, perp_path], dataind, axisind
            )

        return result, index1, index2, indmax1, indmax2

    def get_ivsq(
        self,
        filename: str,
        index1: np.int32 | None = None,
        index2: np.int32 | None = None,
    ):
        int_path = "integrations/Intensity"
        q_path = "integrations/Q_angstrom^-1"
        paths = [int_path, q_path]
        filepath = self.datafolder / filename
        if index1 is None:
            index1 = np.int32(0)
        if index2 is None:
            index2 = np.int32(0)
        return self.read_1d_datafile(filepath, paths, index1, index2)

    def get_ivsq_heatmap(
        self,
        filename: str,
        index1: np.int32 | None = None,
        index2: np.int32 | None = None,
    ):
        int_path = "integrations/Intensity"
        q_path = "integrations/Q_angstrom^-1"
        paths = [int_path, q_path]
        filepath = self.datafolder / filename
        return self.read_1dbatch_datafile(filepath, paths, index1, index2)

    def get_ivschi(
        self,
        filename: str,
        index1: np.int32 | None = None,
        index2: np.int32 | None = None,
    ):
        int_path = "integrations/Intensity"
        chi_path = "integrations/chigi_deg"
        paths = [int_path, chi_path]
        filepath = self.datafolder / filename
        if index1 is None:
            index1 = np.int32(0)
        if index2 is None:
            index2 = np.int32(0)
        return self.read_1d_datafile(filepath, paths, index1, index2)

    def get_qmap(
        self,
        filename: str,
        index1: np.int32 | None = None,
        index2: np.int32 | None = None,
    ):
        map_namestring = "qpara_qperp"
        filepath = self.datafolder / filename

        return self.read_2d_datafile(filepath, map_namestring, index1, index2)

    def get_chimap(
        self,
        filename: str,
        index1: np.int32 | None = None,
        index2: np.int32 | None = None,
    ):

        map_namestring = "chi_qtotal"
        filepath = self.datafolder / filename
        return self.read_2d_datafile(filepath, map_namestring, index1, index2)

    def get_exitmap(
        self,
        filename: str,
        index1: np.int32 | None = None,
        index2: np.int32 | None = None,
    ):
        map_namestring = "exit_angles"
        filepath = self.datafolder / filename

        return self.read_2d_datafile(filepath, map_namestring, index1, index2)

    def parse_loader(self, filename):
        loaders_dict = {
            "IvsQ": self.get_ivsq,
            "IvsQ_heatmap": self.get_ivsq_heatmap,
            "Qmap": self.get_qmap,
            "exitmap": self.get_exitmap,
            "Chimap": self.get_chimap,
            "IvsChi": self.get_ivschi,
        }
        for k, v in loaders_dict.items():
            if k in filename:
                return v
        print("scan type not found in filename")

    def loadfiles(
        self,
        filenames: str,
        index1vals: np.ndarray | None = None,
        index2vals: np.ndarray | None = None,
    ):
        if index1vals is None:
            index1vals = np.zeros(len(filenames)).astype(np.int32)
        if index2vals is None:
            index2vals = np.zeros(len(filenames)).astype(np.int32)
        results = []
        for file_num, file in enumerate(filenames):
            index1 = index1vals[file_num]
            index2 = index2vals[file_num]
            loader = self.parse_loader(file)
            result, *_ = loader(file, index1, index2)
            results.append(result)
        return results


def main():
    loader = data_loader(
        "/dls/science/groups/das/ExampleData/i07/fast_rsm_example_data/local_2026-04-02/"
    )
    found_loader = loader.get_chimap
    outdata = found_loader("Chimap_561339_2026-04-02_09h58m49s.hdf5", 0, 0)
    print("DEBUG pause point")


if __name__ == "__main__":
    main()

    # def import_poni(ponifile):
#     global ai
#     ai = pyFAI.load(ponifile)


# def update_pg_I07(
#     incident_angle=0.075,
#     maskfile="",
#     mask=True,
#     sample_orientation=3,
#     tilt=False,
#     tilt_angle=0,
# ):
#     global pg
#     pg = pygix.Transform()

#     pg.load(ai)
#     if mask == True:
#         pg.maskfile = maskfile
#     pg.incident_angle = incident_angle
#     pg.sample_orientation = sample_orientation
#     if tilt == True:
#         pg.tilt_angle = tilt_angle


# def integrate1d(img, qbins, qmin, qmax, chi_pos, chi_width):
#     """
#     Integrate 2D image into 1D profile over a chi sector using pygix `pg.profile_sector`.
#     """
#     intensity, q = pg.profile_sector(
#         img,
#         qbins,
#         correctSolidAngle=True,
#         method="splitpix",
#         radial_range=(qmin, qmax),
#         chi_pos=chi_pos,
#         chi_width=chi_width,
#         unit="q_A^-1",
#     )
#     return intensity, q


# def chiintegrate1d(
#     img, radial_pos, radial_width, num_points=180, chi_min=-90, chi_max=90
# ):
#     """
#     Integrate 2D image into 1D chi profile over a radial sector using pygix `pg.profile_chi`.
#     """
#     intensity, chi = pg.profile_chi(
#         img,
#         npt=num_points,
#         correctSolidAngle=True,
#         method="splitBBox",
#         radial_pos=radial_pos,
#         radial_width=radial_width,
#         chi_range=(chi_min, chi_max),
#         unit="q_A^-1",
#     )
#     return intensity, chi


# def pygix_transform_global(
#     img,
#     qbins,
#     default_range=False,
#     qxy_min=0,
#     qxy_max=0,
#     qz_min=0,
#     qz_max=0,
#     polarization_factor=0,
# ):

#     if default_range:
#         intensity, qxy, qz = pg.transform_reciprocal(
#             img,
#             npt=(qbins, qbins),
#             polarization_factor=polarization_factor,
#             method="nearest",
#             unit="A",
#         )
#     else:
#         intensity, qxy, qz = pg.transform_reciprocal(
#             img,
#             npt=(qbins, qbins),
#             ip_range=(qxy_min, qxy_max),
#             op_range=(qz_min, qz_max),
#             polarization_factor=polarization_factor,
#             correctSolidAngle=True,
#             method="nearest",
#             unit="A",
#         )

#     return intensity, qxy, qz
