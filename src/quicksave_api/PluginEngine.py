# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import os
import random
import datetime
import time

from quicksave_pybeans.generated.QsBeans import TagBean, MetaBean, ItemBean, BackgroundTaskBean

from quicksave_api.rabbit_push import rabbit_push


def main(internalCreateRequestBean):
    createRequestBean = internalCreateRequestBean.createRequest
    metaBean = createRequestBean.meta
    if metaBean.meta_type == 'image':
        rabbit_push('request', BackgroundTaskBean(name='image', internalCreateRequest=internalCreateRequestBean, kwargs='{}'))
    if metaBean.meta_type == 'page':
        rabbit_push('request', BackgroundTaskBean(name='thumbnail', internalCreateRequest=internalCreateRequestBean, kwargs='{}'))
        rabbit_push('request', BackgroundTaskBean(name='wget', internalCreateRequest=internalCreateRequestBean, kwargs='{}'))
    tags = [TagBean(name='python_sync')]
    if metaBean.source_url is not None:
        if 'youtube.com' in metaBean.source_url:
            rabbit_push('request', BackgroundTaskBean(name='youtube', internalCreateRequest=internalCreateRequestBean, kwargs='{}'))
        if 'github.com' in metaBean.source_url:
            rabbit_push('request', BackgroundTaskBean(name='git', internalCreateRequest=internalCreateRequestBean, kwargs='{}'))
        if ('wikipedia' in metaBean.source_url):
            tags.append(TagBean(name='wiki'))

    item = ItemBean(meta=metaBean, tags=tags, files=[], actions=[])
    return item

