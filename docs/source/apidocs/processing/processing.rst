:py:mod:`processing`
====================

.. py:module:: processing

.. autodoc2-docstring:: processing
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`result2d <processing.result2d>`
     - .. autodoc2-docstring:: processing.result2d
          :summary:
   * - :py:obj:`result1d <processing.result1d>`
     - .. autodoc2-docstring:: processing.result1d
          :summary:
   * - :py:obj:`data_loader <processing.data_loader>`
     - .. autodoc2-docstring:: processing.data_loader
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`parse_peak_kwargs <processing.parse_peak_kwargs>`
     - .. autodoc2-docstring:: processing.parse_peak_kwargs
          :summary:
   * - :py:obj:`peakfit_and_plot <processing.peakfit_and_plot>`
     - .. autodoc2-docstring:: processing.peakfit_and_plot
          :summary:
   * - :py:obj:`fit_peaks <processing.fit_peaks>`
     - .. autodoc2-docstring:: processing.fit_peaks
          :summary:
   * - :py:obj:`check_shape <processing.check_shape>`
     - .. autodoc2-docstring:: processing.check_shape
          :summary:
   * - :py:obj:`main <processing.main>`
     - .. autodoc2-docstring:: processing.main
          :summary:

API
~~~

.. py:function:: parse_peak_kwargs(peakinfo, prefix)
   :canonical: processing.parse_peak_kwargs

   .. autodoc2-docstring:: processing.parse_peak_kwargs

.. py:function:: peakfit_and_plot(peaklist, x, y)
   :canonical: processing.peakfit_and_plot

   .. autodoc2-docstring:: processing.peakfit_and_plot

.. py:function:: fit_peaks(peaklist: list, x: numpy.ndarray, y: numpy.ndarray, background=None)
   :canonical: processing.fit_peaks

   .. autodoc2-docstring:: processing.fit_peaks

.. py:class:: result2d
   :canonical: processing.result2d

   .. autodoc2-docstring:: processing.result2d

   .. py:attribute:: data
      :canonical: processing.result2d.data
      :type: numpy.ndarray
      :value: None

      .. autodoc2-docstring:: processing.result2d.data

   .. py:attribute:: x_axis
      :canonical: processing.result2d.x_axis
      :type: numpy.ndarray
      :value: None

      .. autodoc2-docstring:: processing.result2d.x_axis

   .. py:attribute:: y_axis
      :canonical: processing.result2d.y_axis
      :type: numpy.ndarray
      :value: None

      .. autodoc2-docstring:: processing.result2d.y_axis

   .. py:attribute:: x_unit
      :canonical: processing.result2d.x_unit
      :type: str | None
      :value: None

      .. autodoc2-docstring:: processing.result2d.x_unit

   .. py:attribute:: y_unit
      :canonical: processing.result2d.y_unit
      :type: str | None
      :value: None

      .. autodoc2-docstring:: processing.result2d.y_unit

.. py:class:: result1d
   :canonical: processing.result1d

   .. autodoc2-docstring:: processing.result1d

   .. py:attribute:: data
      :canonical: processing.result1d.data
      :type: numpy.ndarray
      :value: None

      .. autodoc2-docstring:: processing.result1d.data

   .. py:attribute:: data_name
      :canonical: processing.result1d.data_name
      :type: str
      :value: None

      .. autodoc2-docstring:: processing.result1d.data_name

   .. py:attribute:: x_axis
      :canonical: processing.result1d.x_axis
      :type: numpy.ndarray
      :value: None

      .. autodoc2-docstring:: processing.result1d.x_axis

   .. py:attribute:: x_axis_name
      :canonical: processing.result1d.x_axis_name
      :type: str
      :value: None

      .. autodoc2-docstring:: processing.result1d.x_axis_name

   .. py:attribute:: x2_axis
      :canonical: processing.result1d.x2_axis
      :type: numpy.ndarray | None
      :value: None

      .. autodoc2-docstring:: processing.result1d.x2_axis

   .. py:attribute:: x2_axis_name
      :canonical: processing.result1d.x2_axis_name
      :type: str | None
      :value: None

      .. autodoc2-docstring:: processing.result1d.x2_axis_name

.. py:function:: check_shape(inshape, expected_shape, index1, index2)
   :canonical: processing.check_shape

   .. autodoc2-docstring:: processing.check_shape

.. py:class:: data_loader(datafolder: str)
   :canonical: processing.data_loader

   .. autodoc2-docstring:: processing.data_loader

   .. rubric:: Initialization

   .. autodoc2-docstring:: processing.data_loader.__init__

   .. py:method:: get_1d_data(data, paths, dataind, axisind)
      :canonical: processing.data_loader.get_1d_data

      .. autodoc2-docstring:: processing.data_loader.get_1d_data

   .. py:method:: get_2d_data(data, paths, dataind, axisind)
      :canonical: processing.data_loader.get_2d_data

      .. autodoc2-docstring:: processing.data_loader.get_2d_data

   .. py:method:: read_1d_datafile(filepath: pathlib.Path, paths: list, index1: numpy.int32 | tuple, index2: numpy.int32 | tuple)
      :canonical: processing.data_loader.read_1d_datafile

      .. autodoc2-docstring:: processing.data_loader.read_1d_datafile

   .. py:method:: read_1dbatch_datafile(filepath: pathlib.Path, paths: list, index1: numpy.int32 | tuple | None, index2: numpy.int32 | tuple | None)
      :canonical: processing.data_loader.read_1dbatch_datafile

      .. autodoc2-docstring:: processing.data_loader.read_1dbatch_datafile

   .. py:method:: read_2d_datafile(filepath: pathlib.Path, map_namestring: str, index1: numpy.int32 | None, index2: numpy.int32 | None)
      :canonical: processing.data_loader.read_2d_datafile

      .. autodoc2-docstring:: processing.data_loader.read_2d_datafile

   .. py:method:: get_ivsq(filename: str, index1: numpy.int32 | None = None, index2: numpy.int32 | None = None)
      :canonical: processing.data_loader.get_ivsq

      .. autodoc2-docstring:: processing.data_loader.get_ivsq

   .. py:method:: get_ivsq_heatmap(filename: str, index1: numpy.int32 | None = None, index2: numpy.int32 | None = None)
      :canonical: processing.data_loader.get_ivsq_heatmap

      .. autodoc2-docstring:: processing.data_loader.get_ivsq_heatmap

   .. py:method:: get_ivschi(filename: str, index1: numpy.int32 | None = None, index2: numpy.int32 | None = None)
      :canonical: processing.data_loader.get_ivschi

      .. autodoc2-docstring:: processing.data_loader.get_ivschi

   .. py:method:: get_qmap(filename: str, index1: numpy.int32 | None = None, index2: numpy.int32 | None = None)
      :canonical: processing.data_loader.get_qmap

      .. autodoc2-docstring:: processing.data_loader.get_qmap

   .. py:method:: get_chimap(filename: str, index1: numpy.int32 | None = None, index2: numpy.int32 | None = None)
      :canonical: processing.data_loader.get_chimap

      .. autodoc2-docstring:: processing.data_loader.get_chimap

   .. py:method:: get_exitmap(filename: str, index1: numpy.int32 | None = None, index2: numpy.int32 | None = None)
      :canonical: processing.data_loader.get_exitmap

      .. autodoc2-docstring:: processing.data_loader.get_exitmap

   .. py:method:: parse_loader(filename)
      :canonical: processing.data_loader.parse_loader

      .. autodoc2-docstring:: processing.data_loader.parse_loader

   .. py:method:: loadfiles(filenames: str, index1vals: numpy.ndarray | None = None, index2vals: numpy.ndarray | None = None)
      :canonical: processing.data_loader.loadfiles

      .. autodoc2-docstring:: processing.data_loader.loadfiles

.. py:function:: main()
   :canonical: processing.main

   .. autodoc2-docstring:: processing.main
