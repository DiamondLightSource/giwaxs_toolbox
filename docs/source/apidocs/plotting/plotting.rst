:py:mod:`plotting`
==================

.. py:module:: plotting

.. autodoc2-docstring:: plotting
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`individual_plotter <plotting.individual_plotter>`
     - .. autodoc2-docstring:: plotting.individual_plotter
          :summary:
   * - :py:obj:`ind_list_plotter <plotting.ind_list_plotter>`
     - .. autodoc2-docstring:: plotting.ind_list_plotter
          :summary:
   * - :py:obj:`comparison_plotter <plotting.comparison_plotter>`
     - .. autodoc2-docstring:: plotting.comparison_plotter
          :summary:
   * - :py:obj:`combo_plotter <plotting.combo_plotter>`
     - .. autodoc2-docstring:: plotting.combo_plotter
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_logger <plotting.get_logger>`
     - .. autodoc2-docstring:: plotting.get_logger
          :summary:
   * - :py:obj:`plot_2d_map <plotting.plot_2d_map>`
     - .. autodoc2-docstring:: plotting.plot_2d_map
          :summary:
   * - :py:obj:`plot_1d_profile <plotting.plot_1d_profile>`
     - .. autodoc2-docstring:: plotting.plot_1d_profile
          :summary:
   * - :py:obj:`reset_plots <plotting.reset_plots>`
     - .. autodoc2-docstring:: plotting.reset_plots
          :summary:
   * - :py:obj:`plot_i07_list <plotting.plot_i07_list>`
     - .. autodoc2-docstring:: plotting.plot_i07_list
          :summary:
   * - :py:obj:`plot_chi_profile <plotting.plot_chi_profile>`
     - .. autodoc2-docstring:: plotting.plot_chi_profile
          :summary:
   * - :py:obj:`plot_contour <plotting.plot_contour>`
     - .. autodoc2-docstring:: plotting.plot_contour
          :summary:
   * - :py:obj:`plot_i07_list_colab <plotting.plot_i07_list_colab>`
     - .. autodoc2-docstring:: plotting.plot_i07_list_colab
          :summary:
   * - :py:obj:`view_2D_image <plotting.view_2D_image>`
     - .. autodoc2-docstring:: plotting.view_2D_image
          :summary:
   * - :py:obj:`remove_colorbars <plotting.remove_colorbars>`
     - .. autodoc2-docstring:: plotting.remove_colorbars
          :summary:
   * - :py:obj:`remove_axes <plotting.remove_axes>`
     - .. autodoc2-docstring:: plotting.remove_axes
          :summary:

API
~~~

.. py:function:: get_logger(folderpath, name)
   :canonical: plotting.get_logger

   .. autodoc2-docstring:: plotting.get_logger

.. py:function:: plot_2d_map(loaded_data, loaded_axis, filename, fig, ax, logscale, axlabels)
   :canonical: plotting.plot_2d_map

   .. autodoc2-docstring:: plotting.plot_2d_map

.. py:function:: plot_1d_profile(loaded_data, loaded_axis, filename, fig, ax, logscale, axlabels, label=None)
   :canonical: plotting.plot_1d_profile

   .. autodoc2-docstring:: plotting.plot_1d_profile

.. py:function:: reset_plots()
   :canonical: plotting.reset_plots

   .. autodoc2-docstring:: plotting.reset_plots

.. py:class:: individual_plotter(datafolder: str)
   :canonical: plotting.individual_plotter

   .. autodoc2-docstring:: plotting.individual_plotter

   .. rubric:: Initialization

   .. autodoc2-docstring:: plotting.individual_plotter.__init__

   .. py:method:: plot_list_data()
      :canonical: plotting.individual_plotter.plot_list_data

      .. autodoc2-docstring:: plotting.individual_plotter.plot_list_data

.. py:class:: ind_list_plotter(folderpath)
   :canonical: plotting.ind_list_plotter

   .. autodoc2-docstring:: plotting.ind_list_plotter

   .. rubric:: Initialization

   .. autodoc2-docstring:: plotting.ind_list_plotter.__init__

   .. py:method:: get_files()
      :canonical: plotting.ind_list_plotter.get_files

      .. autodoc2-docstring:: plotting.ind_list_plotter.get_files

   .. py:method:: set_plot_callback()
      :canonical: plotting.ind_list_plotter.set_plot_callback

      .. autodoc2-docstring:: plotting.ind_list_plotter.set_plot_callback

   .. py:method:: set_dataloader()
      :canonical: plotting.ind_list_plotter.set_dataloader

      .. autodoc2-docstring:: plotting.ind_list_plotter.set_dataloader

   .. py:method:: set_scantype(scantype, heatmap)
      :canonical: plotting.ind_list_plotter.set_scantype

      .. autodoc2-docstring:: plotting.ind_list_plotter.set_scantype

   .. py:method:: _plot_chimap(data_result: giwaxs_toolbox.processing.result2d, filename: str, fig, ax, logscale: bool)
      :canonical: plotting.ind_list_plotter._plot_chimap

      .. autodoc2-docstring:: plotting.ind_list_plotter._plot_chimap

   .. py:method:: _plot_qmap(data_result: giwaxs_toolbox.processing.result2d, filename: str, fig, ax, logscale: bool)
      :canonical: plotting.ind_list_plotter._plot_qmap

      .. autodoc2-docstring:: plotting.ind_list_plotter._plot_qmap

   .. py:method:: _plot_exitmap(data_result: giwaxs_toolbox.processing.result2d, filename: str, fig, ax, logscale: bool)
      :canonical: plotting.ind_list_plotter._plot_exitmap

      .. autodoc2-docstring:: plotting.ind_list_plotter._plot_exitmap

   .. py:method:: _plot_ivsq(data_result: giwaxs_toolbox.processing.result1d, filename, fig, ax, logscale)
      :canonical: plotting.ind_list_plotter._plot_ivsq

      .. autodoc2-docstring:: plotting.ind_list_plotter._plot_ivsq

   .. py:method:: _plot_ivsq_heatmap(data_result: giwaxs_toolbox.processing.result1d, filename, fig, ax, logscale)
      :canonical: plotting.ind_list_plotter._plot_ivsq_heatmap

      .. autodoc2-docstring:: plotting.ind_list_plotter._plot_ivsq_heatmap

   .. py:method:: _plot_ivschi(data_result: giwaxs_toolbox.processing.result1d, filename, fig, ax, logscale)
      :canonical: plotting.ind_list_plotter._plot_ivschi

      .. autodoc2-docstring:: plotting.ind_list_plotter._plot_ivschi

   .. py:method:: create_plot()
      :canonical: plotting.ind_list_plotter.create_plot

      .. autodoc2-docstring:: plotting.ind_list_plotter.create_plot

.. py:class:: comparison_plotter(datafolder: str)
   :canonical: plotting.comparison_plotter

   .. autodoc2-docstring:: plotting.comparison_plotter

   .. rubric:: Initialization

   .. autodoc2-docstring:: plotting.comparison_plotter.__init__

   .. py:method:: plot_files(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale=False)
      :canonical: plotting.comparison_plotter.plot_files

      .. autodoc2-docstring:: plotting.comparison_plotter.plot_files

.. py:class:: combo_plotter(datafolder: str)
   :canonical: plotting.combo_plotter

   .. autodoc2-docstring:: plotting.combo_plotter

   .. rubric:: Initialization

   .. autodoc2-docstring:: plotting.combo_plotter.__init__

   .. py:method:: plot_files(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale=False)
      :canonical: plotting.combo_plotter.plot_files

      .. autodoc2-docstring:: plotting.combo_plotter.plot_files

   .. py:method:: plot_ivsq(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale: bool = False)
      :canonical: plotting.combo_plotter.plot_ivsq

      .. autodoc2-docstring:: plotting.combo_plotter.plot_ivsq

   .. py:method:: plot_ivschi(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale: bool = False)
      :canonical: plotting.combo_plotter.plot_ivschi

      .. autodoc2-docstring:: plotting.combo_plotter.plot_ivschi

   .. py:method:: plot_exitmap(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale: bool = False)
      :canonical: plotting.combo_plotter.plot_exitmap

      .. autodoc2-docstring:: plotting.combo_plotter.plot_exitmap

   .. py:method:: plot_qmap(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale: bool = False)
      :canonical: plotting.combo_plotter.plot_qmap

      .. autodoc2-docstring:: plotting.combo_plotter.plot_qmap

   .. py:method:: plot_chimap(filenames: list, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None, logscale: bool = False)
      :canonical: plotting.combo_plotter.plot_chimap

      .. autodoc2-docstring:: plotting.combo_plotter.plot_chimap

.. py:function:: plot_i07_list(dirpath: pathlib.Path, scantype: str, title=None)
   :canonical: plotting.plot_i07_list

   .. autodoc2-docstring:: plotting.plot_i07_list

.. py:function:: plot_chi_profile(chi, intensity, chi_min=None, chi_max=None, logscale=False, title='Chi Profile', label=None)
   :canonical: plotting.plot_chi_profile

   .. autodoc2-docstring:: plotting.plot_chi_profile

.. py:function:: plot_contour(csv_file, outfile, cmap='viridis', levels=100, figsize=(10, 6))
   :canonical: plotting.plot_contour

   .. autodoc2-docstring:: plotting.plot_contour

.. py:function:: plot_i07_list_colab(dirpath: pathlib.Path, scantype: str, title=None)
   :canonical: plotting.plot_i07_list_colab

   .. autodoc2-docstring:: plotting.plot_i07_list_colab

.. py:function:: view_2D_image(img_data, cmap='viridis', flip_vertical=False, flip_horizontal=False)
   :canonical: plotting.view_2D_image

   .. autodoc2-docstring:: plotting.view_2D_image

.. py:function:: remove_colorbars(fig)
   :canonical: plotting.remove_colorbars

   .. autodoc2-docstring:: plotting.remove_colorbars

.. py:function:: remove_axes(fig)
   :canonical: plotting.remove_axes

   .. autodoc2-docstring:: plotting.remove_axes
