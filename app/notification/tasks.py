# -*- coding: utf-8 -*-
from celery import shared_task


@shared_task(name='app_user_test_task')
def test_task():
    print('this is test task of app user, auto discovered by celery')
