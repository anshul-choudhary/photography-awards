var XC = window.XC = window.XC || {};


$(function () {

    /** All file upload handling goes here **/
    XC.FileUpload = function () {
        /** Ajax file uploading
         *  This section requires jquery.fileupload.js and jquery.fileupload-validate.js
         *  to be loaded in your page
         * **/
        if (!$('input[type="file"]').length)return;


        $('.db_uploadbox').each(function () {

            console.log("inside");

            var MC = $(this); // the main  container div.
            var F = MC.find('input[type="file"]');
            var PRG = MC.find('.progress_container');
            var BTN = MC.find('.db_input_box');
            var UP = MC.find('.uploaded_files');
            var err = MC.find('.error');
            var IMG = MC.find('.aw_image');
            var IMG_SET = MC.data('imageset');

            //var IMG_2 = MC.find('.aw_image2');
            //var IMG_3 = MC.find('.aw_image3');
            //var IMG_4 = MC.find('.aw_image4');
            //var IMG_5 = MC.find('.aw_image5');

            //var THMB = MC.find('.xc_thumbnail');
            //var BILL = MC.hasClass('xc_billcopy');

            var accept = F.data('accept') ? F.data('accept') : "/(\.|\/)(jpe?g|png|gif)$/i";
            var max_size = F.data('max-size') ? F.data('max-size') : 25242880;

            // min size limit only for images. // 20 kb..
            //var min_size = accept.indexOf('pdf') > -1 ? 0:20480;
            var min_size = accept.indexOf('pdf') > -1 ? 0:40480;


            F.fileupload({
                dataType: 'json',
                maxFileSize: max_size,
                minFileSize: min_size,
                acceptFileTypes: eval(accept),
                submit: function (e, data) {
                    BTN.hide();
                    PRG.show();
                    MC.removeClass('has-error');
                },
                done: function (e, data) {

                    var d = data.result
                    var single_existing = false;

                    if (d.status == 'OK') {
                        PRG.hide();
                        BTN.show();
                        if (!F[0].multiple) {
                            if (UP.children('p').length && UP.children('p').hasClass('remove')) {
                                single_existing = true;
                            }
                            BTN.hide();
                        }
                        var _attrs = 'style="background-image:url(\'' + d.version + '\');height: 160px; width: 250px;background-repeat: no-repeat"'
                        if (d.ctype) _attrs = 'class="' + d.ctype + '"'
                        IMG.attr('value', d.version);


                        if (IMG_SET == 'profile_image') {
                            var p = $('<p><img ' + _attrs + '></img><span>' + d.name + '</span>' +
                                '<input class="aw_image" type="hidden" value="' + d.version + '" name="profile_image"></p>');
                        }
                        else if (IMG_SET == 'image_1'){
                            var p = $('<p><img ' + _attrs + '></img><span>' + d.name + '</span>' +
                                '<input class="aw_image" type="hidden" value="' + d.version + '" name="image_1"></p>');
                        }else if (IMG_SET == 'image_2'){
                            var p = $('<p><img ' + _attrs + '></img><span>' + d.name + '</span>' +
                                '<input class="aw_image" type="hidden" value="' + d.version + '" name="image_2"></p>');
                        }else if (IMG_SET == 'image_3'){
                            var p = $('<p><img ' + _attrs + '></img><span>' + d.name + '</span>' +
                                '<input class="aw_image" type="hidden" value="' + d.version + '" name="image_3"></p>');
                        }else if (IMG_SET == 'image_4'){
                            var p = $('<p><img ' + _attrs + '></img><span>' + d.name + '</span>' +
                                '<input class="aw_image" type="hidden" value="' + d.version + '" name="image_4"></p>');
                        }else{
                            var p = $('<p><img ' + _attrs + '></img><span>' + d.name + '</span>' +
                                '<input class="aw_image" type="hidden" value="' + d.version + '" name="image_5"></p>');
                        }
                        UP.prepend(p);
                        MC.attr("data-uploaded", "true");

                        if (F.attr('data-has-document-type')) {
                            p.addClass('document-type')
                            var sel = $('#id_document_type_optns').clone().addClass('db-document-upload-select')
                                .attr('name', 'docs-type-' + Math.ceil(Math.random() * 10000000))
                                .attr('id', 'docs-type-' + Math.ceil(Math.random() * 10000000))
                            sel[0].options[0].selected = true;
                            //.attr('required','required');
                            p.append(sel);
                            sel.rules('add', 'required')
                            sel.wrap('<i>')

                            sel.SumoSelect();
                        }

                        p.append($('<a style="margin-left: 40px; cursor:pointer;">&times Remove</a>').on('click', function () {

                            file_row = $(this).parent();
                            // make a call to delete that file
                            //DB.Ajax.post('/fileuploadhandler/delete/', {'name': d.file},

                            $(this).closest('.db_uploadbox').attr("data-uploaded","false");
                            $.post( "/fileuploadhandler/delete/", {'name': d.file}, function(d){
                                    if (d.status == 'OK') {
                                        file_row.fadeOut(400, function () {
                                            if (!F[0].multiple) {
                                                if (single_existing) {
                                                    //var I = UP.find('input[type="hidden"]');
                                                    //Jimg = JSON.parse(I.val());
                                                    //delete Jimg.changed;
                                                    //I.val(JSON.stringify(Jimg));
                                                }
                                                else BTN.show();
                                            }
                                            file_row.remove();
                                        })
                                    }
                                });
                        }));
                        if (single_existing) {
                            //var I = UP.find('input[type="hidden"]');
                            //Jimg = JSON.parse(I.val());
                            //Jimg.changed = d.file;
                            //I.val(JSON.stringify(Jimg));
                        }
                        else if (F.attr('data-has-document-type')) {
                            dJson = {deleted: false,
                                changed: d.file}

                            p.append($('<input type="hidden"  name="' + F.data('postname') + '" />')
                                .val(JSON.stringify(dJson)));
                        }
                        else p.append('<input type="hidden" value="' + d.file + '" name="' + F.data('postname') + '" />');
                    }

                    if (d.status == 'error') {
                        PRG.hide();
                        BTN.show();
                        MC.addClass('has-error');
                        err.html(d.msg);
                    }
                },
                progressall: function (e, data) {
                    var progress = parseInt(data.loaded / data.total * 100, 10);
                    PRG.find('.prog_counter').text('Uploading ' + progress + '% ... ')
                    PRG.find('.progress-bar').css(
                        'width',
                            progress + '%'
                    );
                },
            })
                .on('fileuploadprocessalways', function (e, data) {
                    var file = data.files[data.index]
                    if (file.error) {
                        MC.addClass('has-error');
                        err.html(file.error);
                    }
                })

                .prop('disabled', !$.support.fileInput)
                .parent().addClass($.support.fileInput ? undefined : 'disabled');

        });


        $(document.body).on('change', '.db-document-upload-select', function () {
            var I = $(this).closest('p').find('input[type="hidden"]');
            Jimg = JSON.parse(I.val());
            Jimg.doc_type = $(this).val();
            I.val(JSON.stringify(Jimg));
        });

        /*** Editing mode file upload manipulations ***/
        $(document.body).on('click', '.db-remove-image', function () {
            var F = $(this).closest('p');
            var I = F.find('input[type="hidde' +
                'n"]');
            F.closest('.db_uploadbox').removeClass('has-error');
            //Jimg = JSON.parse(I.val());
            F.closest('.db_uploadbox').attr("data-uploaded","false");

            file_row = $(this).parent();
            $.post( "/fileuploadhandler/delete/", {'name': file_row.find('span').text()}, function(d){
                    if (d.status == 'OK') {
                        file_row.fadeOut(400, function () {
                            if (!F[0].multiple) {
                                if (single_existing) {
                                    //var I = UP.find('input[type="hidden"]');
                                    //Jimg = JSON.parse(I.val());
                                    //delete Jimg.changed;
                                    //I.val(JSON.stringify(Jimg));
                                }
                                else BTN.show();
                            }
                            file_row.remove();
                        })
                    }
                });

            is_multi = F.closest('.db_uploadbox').find('.fileupload_btn').attr('multiple');
            if (!F.hasClass('remove')) {
                //F.addClass('remove');
                //$(this).html('Restore');
                $(this).hide();
                //Jimg.deleted = true;
                F.closest('.db_uploadbox').children('.db_input_box').show();
                F.remove();
            }
            else {
                F.removeClass('remove');
                $(this).html('&times; Remove');
                //Jimg.deleted = false;

                if (!is_multi) {
                    F.prev().find('a').trigger('click');
                    F.closest('.db_uploadbox').children('.db_input_box').hide();
                }
            }

            //I.val(JSON.stringify(Jimg));
        });
    }
    //End File Upload

});



$(document).ready(function(){
    XC.FileUpload();
});
