from pathlib import Path
import os

class BaseConfig:
    pass


class LocalConfig:
    input_path = Path.cwd().joinpath("s3").joinpath("examples").joinpath("rawxml")
    output_path = Path.cwd().joinpath("demo").joinpath("output").joinpath("csv")
    output_format = "csv"


config = {
    'local': LocalConfig()
}