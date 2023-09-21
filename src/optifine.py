from typing import ClassVar

from beet import Context, JsonFile, PngFile


def beet_default(ctx: Context):
    ctx.assets.extend_namespace += [JsonBiomes, FogSkyBiomes]


class JsonBiomes(JsonFile):
    """Class representing a json biome list."""

    scope: ClassVar[tuple[str, ...]] = ("optifine_biome_colors",)
    extension: ClassVar[str] = ".json"


class FogSkyBiomes(PngFile):
    """Class representing a png biome fog and sky colors."""

    scope: ClassVar[tuple[str, ...]] = ("optifine_biome_colors",)
    extension: ClassVar[str] = ".png"
