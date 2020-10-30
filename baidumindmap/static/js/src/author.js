function BaiduMindmapAuthorXBlock (runtime, element) {
    var editor_link = runtime.handlerUrl(element, 'editor');
    $(element).find(".baidumindmap_editor").click(function(){window.open(editor_link)});
};
