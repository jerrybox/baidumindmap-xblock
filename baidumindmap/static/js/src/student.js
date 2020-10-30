function BaiduMindmapStudentXBlock (runtime, element) {
    var map_link = runtime.handlerUrl(element, 'map');

    $(element).find(".baidumindmap_object").attr("src", map_link);

    var $baidumindmapBlock = $(".js-baidumindmap-block", element);
    $('.js-button-full-screen', element).on( "click", function() {
      $baidumindmapBlock.toggleClass("full-screen-baidumindmap");
    });
};
