import matplotlib.pyplot as plt
import numpy as np

def plot_phantom(fig: plt.Figure, phantom: np.ndarray) -> None:
    fig.clear()
    axes = fig.gca()
    ax = axes.imshow(phantom, cmap=plt.get_cmap("hot"), vmax=1, vmin=0)
    fig.colorbar(ax)
    return None

def plot_radon_transform(fig: plt.Figure, radon_transform: np.ndarray, theta: np.ndarray) -> None:
    fig.clear()
    axes = fig.gca()
    radon_max = radon_transform.max()
    radon_min = radon_transform.min()
    ax = axes.imshow(
        radon_transform,
        cmap=plt.cm.get_cmap("hot"),
        aspect='auto',
        vmin=radon_min,
        vmax=radon_max if radon_max != radon_min else 250,
        extent=[theta[0], theta[-1], 125, -125]
    )
    fig.colorbar(ax)
    return None

def plot_single_degree_radon_transform(fig: plt.Figure, radon_transform: np.ndarray, degree: int, theta: np.ndarray) -> None:
    if degree not in theta:
        return None
    idx = np.where(theta == degree)
    fig.clear()
    axes = fig.gca()
    axes.plot(radon_transform[:, idx[0]])
    return None

def plot_inverse_radon(fig: plt.Figure, iphantom: np.ndarray) -> None:
    fig.clear()
    axes = fig.gca()
    ax = axes.imshow(
        iphantom,
        cmap=plt.cm.get_cmap("hot"),
        aspect='auto',
        vmin=0,
        vmax=1
    )
    fig.colorbar(ax)
    return None