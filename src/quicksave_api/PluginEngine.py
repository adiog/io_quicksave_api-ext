# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

from quicksave_pybeans.generated.QsBeans import TagBean, MetaBean, ItemBean, BackgroundTaskBean

from quicksave_api.rabbit_pusher import RabbitPusher


def schedule_background_task(rabbit_pusher, name, internal_create_request_bean, kwargs='{}'):
    rabbit_pusher.push(BackgroundTaskBean(name=name, internalCreateRequest=internal_create_request_bean, kwargs=kwargs))


def main(internal_create_request_bean):
    with RabbitPusher() as rabbit_pusher:
        create_request_bean = internal_create_request_bean.createRequest
        meta_bean = create_request_bean.meta

        if meta_bean.meta_type == 'image':
            schedule_background_task(rabbit_pusher, 'image', internal_create_request_bean)
        if meta_bean.meta_type == 'audio':
            schedule_background_task(rabbit_pusher, 'audio', internal_create_request_bean)
        if meta_bean.meta_type == 'video':
            schedule_background_task(rabbit_pusher, 'video', internal_create_request_bean)
        if meta_bean.meta_type == 'page':
            schedule_background_task(rabbit_pusher, 'thumbnail', internal_create_request_bean)
            schedule_background_task(rabbit_pusher, 'wget', internal_create_request_bean)

        if meta_bean.meta_type == 'selection':
            if meta_bean.text is not None:
                if 'facebook.com' in meta_bean.text and 'videos' in meta_bean.text:
                    schedule_background_task(rabbit_pusher, 'facebook:video', internal_create_request_bean)

        tags = [TagBean(name='python_sync')]

        if meta_bean.source_url is not None:
            if 'youtube.com' in meta_bean.source_url:
                schedule_background_task(rabbit_pusher, 'youtube:video', internal_create_request_bean)
            if 'github.com' in meta_bean.source_url:
                schedule_background_task(rabbit_pusher, 'git', internal_create_request_bean)
            if 'wikipedia' in meta_bean.source_url:
                tags.append(TagBean(name='wiki'))

        item = ItemBean(meta=meta_bean, tags=tags, files=[], actions=[])

        return item
