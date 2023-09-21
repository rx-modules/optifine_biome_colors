from dataclasses import dataclass
from typing import Iterable, NamedTuple

from beet import Context
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenBiome, worldgen
from PIL import Image

from .optifine import FogSkyBiomes, JsonBiomes

FOG_COLORS = "fogcolor0"
SKY_COLORS = "skycolor0"


class RGB(NamedTuple):
    red: int
    green: int
    blue: int

    def as_hex(self):
        return f"{self.red:02x}{self.green:02x}{self.blue:02x}"

    def as_int(self):
        return int(self.as_hex(), 16)


@dataclass
class Biome:
    id: int
    name: str
    fog_color: RGB | None
    sky_color: RGB | None

    @property
    def resource_name(self):
        return f"minecraft:{self.name}"


def get_biomes(biomes: list[str], fog: Image, sky: Image) -> Iterable[Biome]:
    """Reads in a list of biomes, alongside the 2 optifine image files to produce a
    a stream of biome definitions.
    """

    for i in range(len(biomes)):
        pix_pos = i, 0
        if sky.getpixel(pix_pos) != (128, 177, 255):
            yield Biome(
                id=i,
                name=biomes[i],
                fog_color=RGB(*fog.getpixel(pix_pos)[:3]),
                sky_color=RGB(*sky.getpixel(pix_pos)[:3]),
            )
        else:
            yield Biome(id=i, name=biomes[i], fog_color=None, sky_color=None)


def beet_default(ctx: Context):
    ctx.require(worldgen)

    vanilla = ctx.inject(Vanilla)
    fog = ctx.assets[FogSkyBiomes]["the3gg:fogcolor0"]
    sky = ctx.assets[FogSkyBiomes]["the3gg:skycolor0"]
    biome_file = ctx.assets[JsonBiomes]["the3gg:biomes"]

    assert "biomes" in biome_file.data

    biomes = get_biomes(biome_file.data["biomes"], fog.image, sky.image)

    for biome in biomes:
        vanilla_biome = vanilla.data[WorldgenBiome].get(biome.resource_name)
        if vanilla_biome is not None and (
            biome.sky_color is not None or biome.fog_color is not None
        ):
            print(biome.name)
            effects = vanilla_biome.data["effects"]

            if biome.fog_color is not None:
                old_color = effects["fog_color"]
                color = effects["fog_color"] = biome.fog_color.as_int()
                print(" ", "fog_color", old_color, "=>", color)

            if biome.sky_color is not None:
                old_color = effects["sky_color"]
                color = effects["sky_color"] = biome.sky_color.as_int()
                print(" ", "sky_color", old_color, "=>", color)

            ctx.data[WorldgenBiome][biome.resource_name] = vanilla_biome
            print()
