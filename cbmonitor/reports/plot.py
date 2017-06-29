from itertools import cycle
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas

matplotlib.rcParams.update({
    'axes.formatter.limits': (-6, 6),
    'axes.grid': True,
    'axes.linewidth': 0.2,
    'axes.xmargin': 0.005,
    'font.size': 5,
    'grid.linestyle': 'dashed',
    'grid.linewidth': 0.3,
    'legend.fancybox': True,
    'legend.markerscale': 1.5,
    'legend.numpoints': 1,
    'lines.linestyle': 'None',
    'lines.linewidth': 0.2,
    'lines.marker': '.',
    'lines.markersize': 1.5,
    'xtick.direction': 'inout',
    'xtick.major.size': 2,
    'xtick.major.width': 0.3,
    'ytick.direction': 'inout',
    'ytick.major.size': 2,
    'ytick.major.width': 0.3,
})


def plot_as_png(filename: str,
                series: List[pandas.Series],
                labels: List[str],
                colors: List[str],
                ylabel: str,
                chart_type: str,
                rebalances: List[List[int]]):
    """Plot and save in PNG format one or multiple time series."""
    fig = plt.figure(figsize=(5, 2.5))  # 1000 x 500 px (200 dpi)
    ax = init_ax(fig)

    if chart_type in ('lt90', 'gt80', 'histo'):
        plot_percentiles(ax, series, labels, colors, ylabel, chart_type)
    else:
        plot_time_series(ax, series, labels, colors, ylabel)
        highlight_rebalance(rebalances, colors)

    legend = ax.legend()
    legend.get_frame().set_linewidth(0.5)

    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close()


def init_ax(fig: plt.Figure) -> plt.Subplot:
    """Initialize subplot object within the figure object."""
    ax = fig.add_subplot(1, 1, 1)
    ax.ticklabel_format(useOffset=False)
    return ax


def plot_time_series(ax: plt.Subplot,
                     series: List[pandas.Series],
                     labels: List[str],
                     colors: List[str],
                     ylabel: str):
    """Plot line charts."""
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.set_xlabel('Time elapsed, sec')
    for s, label, color in zip(series, labels, colors):
        ax.plot(s.index, s, label=label, color=color)
    ymin, ymax = ax.get_ylim()
    plt.ylim(ymin=0, ymax=max(1, ymax * 1.05))


def plot_percentiles(ax: plt.Subplot,
                     series: List[pandas.Series],
                     labels: List[str],
                     colors: List[str],
                     ylabel: str,
                     chart_type: str):
    """Plot bar charts with 3 possible percentile ranges.

    Supported options:
    1) 1 to 99 (linear)
    2) 1 to 89 (linear)
    3) 80 to 99.999 (non-linear, pre-defined)
    """
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Percentile')
    align = cycle(('edge', 'center'))
    width = cycle((0.6, 0.4))

    if chart_type == 'lt90':
        percentiles = range(1, 90)
        x = percentiles
        plt.xlim(0, 90)
    elif chart_type == 'gt80':
        percentiles = 80, 85, 90, 95, 97.5, 99, 99.9, 99.99, 99.999
        x = range(len(percentiles))
        plt.xticks(x, percentiles)
    else:
        percentiles = range(1, 100)
        x = percentiles
        plt.xlim(0, 100)

    for s, label, color in zip(series, labels, colors):
        y = numpy.percentile(s, percentiles)
        ax.bar(x=x, y=y, linewidth=0.0, label=label, color=color,
               align=next(align), width=next(width))


def highlight_rebalance(rebalances: List[List[int]],
                        colors: List[str]):
    """Add a transparent span that highlights the rebalance progress."""
    for (start, end), color in zip(rebalances, colors):
        plt.axvspan(xmin=start, xmax=end, facecolor=color, alpha=0.1,
                    linewidth=0.5)
