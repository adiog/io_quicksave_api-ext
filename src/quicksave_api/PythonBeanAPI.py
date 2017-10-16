# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

from quicksave_api.PluginEngine import main
from quicksave_pybeans.generated.QsBeans import InternalCreateRequestBean
from quicksave_pybeans.pybeans import to_string


def process(internal_create_request_bean):
    return main(internal_create_request_bean)

