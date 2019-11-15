#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import tornado.web


class HelloHandler(tornado.web.RequestHandler):
    """
    /internal/hello
    """
    def get(self):
        """
        support GET
        """
        self.finish()
