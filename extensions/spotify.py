import urllib.request
from io import BytesIO
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as sp
import spotipy
import toml
from core.extension import Extension
from PIL import Image
from pydantic import BaseModel
from sklearn.cluster import KMeans
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from core.pixel import Pixel

cache = []


def getCurrentPlaybackInfo(user: spotipy.Spotify):

    currentPlayback = user.current_playback()
    if currentPlayback and currentPlayback["currently_playing_type"] == "track":
        song = currentPlayback["item"]["name"]
        song_id = currentPlayback["item"]["id"]
        artists = [artist["name"] for artist in currentPlayback["item"]["artists"]]
        album = currentPlayback["item"]["album"]["name"]
        cover_url = currentPlayback["item"]["album"]["images"][-1]["url"]
        length_ms = currentPlayback["item"]["duration_ms"]
        position = currentPlayback["progress_ms"]

        print(
            f"{song} - {', '.join(artists)}: {position/1000}/{length_ms/1000}, {cover_url}"
        )


class spotify(Extension):
    name = "spotify"

    def initialize(self):
        config = toml.load("conf.toml")
        redirectUrl = "https://example.com/callback"
        scope = " ".join(
            [
                "user-read-currently-playing",
                "user-read-playback-state",
                "user-modify-playback-state",
                "user-library-read",
                "app-remote-control",
            ]
        )
        clientId = config["CLIENT_ID"]
        clientSecret = config["CLIENT_SECRET"]

        self.user = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=clientId,
                client_secret=clientSecret,
                redirect_uri=redirectUrl,
                scope=scope,
            )
        )

        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=clientId, client_secret=clientSecret
            )
        )

    def display(self, delay):
        c = fetch_spotify_cover_color(self.user)
        self.pixels.fill(c.toTuple())
        self.pixels.show()
        sleep(1)

    def createModel(self):
        self.model = BaseModel


def best_color(img_url, k=8, color_tol=5):
    """Returns a suitable background color for the given image.
    Uses k-means clustering to find `k` distinct colors in
    the image. A colorfulness index is then calculated for each
    of these colors. The color with the highest colorfulness
    index is returned if it is greater than or equal to the
    colorfulness tolerance `color_tol`. If no color is colorful
    enough, a gray color will be returned. Returns more or less
    the same color as Spotify in 80 % of the cases.
    Args:
        img_url: url to image
        k (int): Number of clusters to form.
        color_tol (float): Tolerance for a colorful color.
            Colorfulness is defined as described by Hasler and
            Süsstrunk (2003) in https://infoscience.epfl.ch/
            record/33994/files/HaslerS03.pdf.
    Returns:
        tuple: (R, G, B). The calculated background color.
    """
    for c in cache:
        if c[0] == img_url:
            return c[1]

    image_bytes = BytesIO(urllib.request.urlopen(img_url).read())
    img = np.array(Image.open(image_bytes))

    artwork = img.copy()
    img = img.reshape((img.shape[0] * img.shape[1], 3))

    clt = KMeans(n_clusters=k)
    clt.fit(img)
    hist = find_histogram(clt)
    centroids = clt.cluster_centers_

    colorfulness = [
        calc_colorfulness(color[0], color[1], color[2]) for color in centroids
    ]
    max_colorful = np.max(colorfulness)

    if max_colorful < color_tol:
        # If not colorful, set to gray
        best_color = [230, 230, 230]
    else:
        # Pick the most colorful color
        best_color = centroids[np.argmax(colorfulness)]

    return Pixel(r=best_color[0], g=best_color[1], b=best_color[2])


def format_color(color):
    return "#%02x%02x%02x" % (
        color[0] if type(color[0]) == int else color[0].astype(np.int64),
        color[1] if type(color[1]) == int else color[1].astype(np.int64),
        color[2] if type(color[2]) == int else color[2].astype(np.int64),
    )


def find_histogram(clt):
    """Create a histogram of image.
    Args:
        clt (array_like): Input data.
    Returns:
        array: The values of the histogram.
    """
    num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    hist, _ = np.histogram(clt.labels_, bins=num_labels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def calc_colorfulness(r, g, b):
    """Returns a colorfulness index of given RGB combination.
    Implementation of the colorfulness metric proposed by
    Hasler and Süsstrunk (2003) in https://infoscience.epfl.ch/
    record/33994/files/HaslerS03.pdf.
    Args:
        r (int): Red component.
        g (int): Green component.
        b (int): Blue component.
    Returns:
        float: Colorfulness metric.
    """
    rg = np.absolute(r - g)
    yb = np.absolute(0.5 * (r + g) - b)

    # Compute the mean and standard deviation of both `rg` and `yb`.
    rg_mean, rg_std = (np.mean(rg), np.std(rg))
    yb_mean, yb_std = (np.mean(yb), np.std(yb))

    # Combine the mean and standard deviations.
    std_root = np.sqrt((rg_std ** 2) + (yb_std ** 2))
    mean_root = np.sqrt((rg_mean ** 2) + (yb_mean ** 2))

    return std_root + (0.3 * mean_root)


def fetch_spotify_cover_color(sp):
    current_playback = sp.currently_playing(additional_types="episode")
    try:
        if current_playback.get("item", {}).get("images"):  # Podcasts
            url = current_playback["item"]["images"][2]["url"]
        else:  # Music
            url = current_playback["item"]["album"]["images"][2]["url"]
        out = best_color(url)
        return out
    except Exception:
        return Pixel(120, 120, 120)
