# This file is a part of quickave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

from PluginEngine import main
from quicksave_pybeans.generated.QsBeans import InternalCreateRequestBean

def process(internalCreateRequestBean):
    return main(internalCreateRequestBean)

