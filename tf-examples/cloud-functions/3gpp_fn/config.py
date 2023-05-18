from pathlib import Path
import os

class BaseConfig:
    pass


class LocalConfig:
    input_path = Path.cwd().joinpath("raw").joinpath("xml")
    output_path = Path.cwd().joinpath("raw").joinpath("json")
    output_format = "json"


config = {
    'local': LocalConfig()
}