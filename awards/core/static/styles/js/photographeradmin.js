(function($) {
    $(document).ready(function(){

        /** Vendor images
         * we are changing the default dir of file browser fields using javascript as not possible from django
         * **/

        function change_dir(As,dir){
            As.each(function(){
                a = $(this);
                arr = a.attr('href').split('=');
                arr[2] = dir +"');";
                a.attr('href',arr.join('='));

                //Show images on admin
                $img_div = a.parent();
                $img_val = $img_div.find('input').val();
                $p_tag = $img_div.find('p');
                $img_tag = $img_div.find('img');

                if ($img_val.length){
                    $p_tag.css('max-width', '130px');
                    $p_tag.css('max-height', '50px');
                    $img_tag.css('width', '100%');
                    $img_tag.css('height', '100%');
                    $img_div.find('img').attr('src','/media/' + $img_val);
                    $img_div.find('p').show();
                }
            });
        }

        var dir = 'asdasd/asdasd'+ $('#id_photographer_media_dir').val();
        change_dir($("input[id*=id_core-image-content_type] + a.fb_show"),dir);
        change_dir($("input[id*=id_core-document-content_type] + a.fb_show"),dir);

    });

}(django.jQuery));