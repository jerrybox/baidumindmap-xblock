function BaiduMindmapStudioXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    $(element).find('.save-button').bind('click', function() {
        var form_data = new FormData();
        var display_name = $(element).find('input[name=display_name]').val();
        var width = $(element).find('input[name=width]').val();
        var height = $(element).find('input[name=height]').val();
        var img_url = $(element).find('input[name=img_url]').val();
        // var json_data = $(element).find('textarea[name=json_data]').val();

        form_data.append('display_name', display_name);
        form_data.append('width', width);
        form_data.append('height', height);
        form_data.append('img_url', img_url);
        // form_data.append('json_data', json_data);
        runtime.notify('save', {
            state: 'start'
        });

        $.ajax({
            url: handlerUrl,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: "POST",
            success: function(response) {
                if (response.errors.length > 0) {
                    response.errors.forEach(function(error) {
                        runtime.notify("error", {
                            "message": error,
                            "title": "BaiduMindmap component save error"
                        });
                    });
                } else {
                    runtime.notify('save', {
                        state: 'end'
                    });
                }
            }
        });

    });

    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });
}