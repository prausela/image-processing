import matplotlib.pyplot as plt
import numpy as np

def plot_phantom(phantom: np.ndarray) -> plt.Figure:
    fig = plt.Figure()
    axes = fig.gca()
    ax = axes.imshow(phantom, cmap=plt.get_cmap("hot"), vmax=1, vmin=0)
    plt.colorbar(ax)
    return fig

def plot_radon_transform(radon_transform: np.ndarray, theta: np.ndarray) -> plt.Figure:
    fig = plt.Figure()
    axes = fig.gca()
    ax = axes.imshow(
        radon_transform,
        cmap=plt.cm.get_cmap("hot"),
        aspect='auto',
        extent=[theta[0], theta[-1], 125, -125]
    )
    plt.colorbar(ax)
    return fig

def plot_single_degree_radon_transform(radon_transform: np.ndarray, degree: int, theta: np.ndarray) -> plt.Figure:
    if degree not in theta:
        return None
    idx = np.where(theta == degree)
    fig = plt.Figure()
    axes = fig.gca()
    axes.plot(radon_transform[:, idx[0]])
    return fig

def plot_inverse_radon(iphantom: np.ndarray) -> plt.Figure:
    fig = plt.Figure()
    axes = fig.gca()
    ax = axes.imshow(
        iphantom,
        cmap=plt.cm.get_cmap("hot"),
        aspect='auto',
        vmin=0,
        vmax=1
    )
    plt.colorbar(ax)
    return fig