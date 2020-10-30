# -*- coding:utf-8 -*-
from django.shortcuts import reverse
from django.template import Context, Template

import logging
import json
import pkg_resources

from mako.template import Template as MakoTemplate
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.fragment import Fragment
from webob import Response


# Make '_' a no-op so we can scrape strings
def _(text):
    return text

logger = logging.getLogger(__name__)


class BaiduMindmapXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """
    display_name = String(
        display_name=_("Display Name"),
        help=_("Display name for this module"),
        default="BaiduMindmap",
        scope=Scope.settings,
    )
    width = Integer(
        display_name=_("Display width (%)"),
        help=_("Width of iframe (default: 100%)"),
        default=100,
        scope=Scope.settings,
    )
    height = Integer(
        display_name=_("Display height (px)"),
        help=_("Height of iframe"),
        default=450,
        scope=Scope.settings,
    )
    json_data = String(
        display_name="Map Data JSON",
        help="Mindmap source json data",
        scope=Scope.settings,
        default="""
            {
                "root":
                {
                    "data":
                    {
                        "id": "c6p0ivtrlg80",
                        "created": 1603937875499,
                        "text": "BaiduMindmap"
                    },
                    "children": []
                },
                "template": "default",
                "theme": "fresh-blue",
                "version": "1.4.43"
            }
        """
    )

    has_author_view = True

    @staticmethod
    def resource_string(path):
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @staticmethod
    def json_response(data):
        return Response(json.dumps(data), content_type="application/json")

    @staticmethod
    def html_response(content):
        content.encode("utf-8")
        return Response(content, content_type="text/html", charset="utf-8")

    def render_template(self, template_path, context):
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

    def get_context_studio(self):
        return {
            "field_display_name": self.fields["display_name"],
            "field_width": self.fields["width"],
            "field_height": self.fields["height"],
            "field_map": self.fields["json_data"],
            "baidumindmap_xblock": self,
        }

    def studio_view(self, context=None):
        """
        xblock编辑按钮视图
        :param context:
        :return:
        """
        context = self.get_context_studio()
        template = self.render_template("static/html/studio.html", context)
        frag = Fragment(template)
        frag.add_javascript(self.resource_string("static/js/src/studio.js"))
        frag.initialize_js("BaiduMindmapStudioXBlock")
        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix):
        """
        暂时不通过studio编辑json_data
        """
        self.display_name = request.params["display_name"]
        self.width = request.params["width"]
        self.height = request.params["height"]
        # self.json_data = request.params["json_data"]
        response = {"result": "success", "errors": []}
        return self.json_response(response)

    def author_view(self, context=None):
        """
        cms视图
        """
        html = self.resource_string("static/html/author.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/author.js"))
        frag.initialize_js('BaiduMindmapAuthorXBlock')
        return frag

    @XBlock.handler
    def editor(self, request, suffix=''):
        """
        新页面加载百度脑图编辑器
        """
        html = self.resource_string("static/html/editor.html")
        # 硬编码依赖cms url
        content = MakoTemplate(html).render(data=self.json_data,
                                            url=reverse(
                                                "component_handler",
                                                args=(self.scope_ids.usage_id, "save_map", ""))
                                            )
        return self.html_response(content)

    @XBlock.json_handler
    def save_map(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        cms保存导图数据到数据库
        """
        self.json_data = json.dumps(data)
        result = {'msg': 'ok'}
        return self.json_response(result)

    def student_view(self, context=None):
        """
        lms视图
        """
        html = self.resource_string("static/html/student.html")
        frag = Fragment(html.format(display_name=self.display_name, height=self.height, width=self.width))
        frag.add_css(self.resource_string("static/css/baidumindmap.css"))
        frag.add_javascript(self.resource_string("static/js/src/student.js"))
        frag.initialize_js('BaiduMindmapStudentXBlock')
        return frag

    @XBlock.handler
    def map(self, request, context=None):
        """
        lms视图
        """
        html = self.resource_string("static/html/map.html")
        content = MakoTemplate(html).render(data=self.json_data)
        return self.html_response(content)
