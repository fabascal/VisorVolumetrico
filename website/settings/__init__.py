# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present NovaRet
"""

from flask import Blueprint

blueprint = Blueprint(
    'settings_blueprint',
    __name__,
    url_prefix=''
)