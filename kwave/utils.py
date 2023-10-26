import matplotlib.pyplot as plt


def imshow(
    img, title="", ax=None, cbar=False, extent=None, cmap=None, axis_off=False, **kwargs
):
    """
    kwargs are passed to ax.imshow()

    hspacing and vspacing overrides extent
    """
    if ax is None:
        plt.close()
        fig, ax = plt.subplots()
    else:
        fig = plt.gcf()

    if not cmap and len(img.shape) == 2:
        cmap = "gray"

    im = ax.imshow(img, extent=extent, cmap=cmap, **kwargs)

    if cbar and len(img.shape) == 2:
        fig.colorbar(im)

    if title:
        ax.set_title(title)

    if axis_off:
        ax.set_axis_off()

    return im


def imshow2(img1, img2, t1="1", t2="2", extent=None, **kwargs):
    """
    Params
    ------
    img1: image 1
    img2: image 2
    t1: title 1
    t2: title 2
    """
    assert img1.shape == img2.shape
    plt.close()
    fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
    i1 = imshow(img1, ax=ax[0], extent=extent, title=t1, **kwargs)
    i2 = imshow(img2, ax=ax[1], extent=extent, title=t2, **kwargs)
    fig.tight_layout()
    plt.show()
    return i1, i2
