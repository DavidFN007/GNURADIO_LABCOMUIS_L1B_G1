#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: medida_de_potencia
# Author: Camilo y Pedreros
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Mod_L1B



from gnuradio import qtgui

class medida_de_potencia(gr.top_block, Qt.QWidget):

    def __init__(self, l_vect=1024):
        gr.top_block.__init__(self, "medida_de_potencia", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("medida_de_potencia")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "medida_de_potencia")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.l_vect = l_vect

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.A = A = 1

        ##################################################
        # Blocks
        ##################################################
        self._A_range = Range(0, 45, 1, 1, 200)
        self._A_win = RangeWidget(self._A_range, self.set_A, "'A'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._A_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            2048, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.potencia_Lineal_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.potencia_Lineal_1.set_update_time(0.10)
        self.potencia_Lineal_1.set_title('potencia Logarítmica [dBm]')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.potencia_Lineal_1.set_min(i, -1)
            self.potencia_Lineal_1.set_max(i, 1)
            self.potencia_Lineal_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.potencia_Lineal_1.set_label(i, "Data {0}".format(i))
            else:
                self.potencia_Lineal_1.set_label(i, labels[i])
            self.potencia_Lineal_1.set_unit(i, units[i])
            self.potencia_Lineal_1.set_factor(i, factor[i])

        self.potencia_Lineal_1.enable_autoscale(True)
        self._potencia_Lineal_1_win = sip.wrapinstance(self.potencia_Lineal_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._potencia_Lineal_1_win)
        self.potencia_Lineal_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.potencia_Lineal_0.set_update_time(0.10)
        self.potencia_Lineal_0.set_title('potencia Logarítmica [dBW]')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.potencia_Lineal_0.set_min(i, -1)
            self.potencia_Lineal_0.set_max(i, 1)
            self.potencia_Lineal_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.potencia_Lineal_0.set_label(i, "Data {0}".format(i))
            else:
                self.potencia_Lineal_0.set_label(i, labels[i])
            self.potencia_Lineal_0.set_unit(i, units[i])
            self.potencia_Lineal_0.set_factor(i, factor[i])

        self.potencia_Lineal_0.enable_autoscale(True)
        self._potencia_Lineal_0_win = sip.wrapinstance(self.potencia_Lineal_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._potencia_Lineal_0_win)
        self.potencia_Lineal = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.potencia_Lineal.set_update_time(0.10)
        self.potencia_Lineal.set_title('potencia_Lineal_[W]')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.potencia_Lineal.set_min(i, -1)
            self.potencia_Lineal.set_max(i, 1)
            self.potencia_Lineal.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.potencia_Lineal.set_label(i, "Data {0}".format(i))
            else:
                self.potencia_Lineal.set_label(i, labels[i])
            self.potencia_Lineal.set_unit(i, units[i])
            self.potencia_Lineal.set_factor(i, factor[i])

        self.potencia_Lineal.enable_autoscale(True)
        self._potencia_Lineal_win = sip.wrapinstance(self.potencia_Lineal.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._potencia_Lineal_win)
        self.fft_vxx_0 = fft.fft_vfc(l_vect, True, window.blackmanharris(1024), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, l_vect)
        self.blocks_nlog10_ff_1 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 30)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(3.70053e-6)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(l_vect)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 12928, A, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SAW_WAVE, 60, A, 0, 0)
        self.Mod_L1B_SumaVectorL1B_0 = Mod_L1B.SumaVectorL1B(l_vect)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.Mod_L1B_SumaVectorL1B_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.Mod_L1B_SumaVectorL1B_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_nlog10_ff_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.potencia_Lineal, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.potencia_Lineal_1, 0))
        self.connect((self.blocks_nlog10_ff_1, 0), (self.potencia_Lineal_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "medida_de_potencia")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_l_vect(self):
        return self.l_vect

    def set_l_vect(self, l_vect):
        self.l_vect = l_vect

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A
        self.analog_sig_source_x_0.set_amplitude(self.A)
        self.analog_sig_source_x_0_0.set_amplitude(self.A)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--l-vect", dest="l_vect", type=intx, default=1024,
        help="Set Longitud FFT [default=%(default)r]")
    return parser


def main(top_block_cls=medida_de_potencia, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(l_vect=options.l_vect)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
