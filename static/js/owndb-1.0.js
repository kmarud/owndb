/* 
 * Owndb client-side logic file.
 *
 */

var field_name = '<p><input class="field_name" type="text" placeholder=" set field name" required /></p>';
var field_name_empty = '<p><input class="field_name" type="hidden" value="-" /></p>';

var text_settings = field_name + '<p>Not null: <input class="notnull" type="checkbox" /> | Multiline: <input class="multiline" type="checkbox" /></p>';
var number_settings = field_name + '<p>Not null: <input class="notnull" type="checkbox" /> | Natural values: <input class="natural" type="checkbox" /></p>'
var choice_settings = field_name + '<p><a class="add_choice">Add option</a></p><ul class="options_block"></ul>';
var checkbox_settings = field_name + '<p><a class="add_checkbox">Add option</a></p><ul class="options_block"></ul>';
var image_settings = field_name + '<p><input class="image" disabled type="file" accept=".png,.gif,.jpg,.jpeg" /></p>';
var file_settings = field_name + '<p><input class="file" disabled type="file" /></p>';
var connection_settings = field_name + '<p>Select form:&nbsp;<select class="connection_form"></select></p>';
var labeltext_settings = field_name_empty + '<p><input class="label_text" type="text" placeholder=" set text" /></p>';
var labelimage_settings = field_name_empty + '<p><input class="label_image" name="file" type="file" accept=".png,.gif,.jpg,.jpeg" required /><progress min="0" max="100" value="0"></progress></p>';
var nextform_settings = field_name_empty + '<p>Select form:&nbsp;<select class="connection_form"></select></p>';

var choice_item = '\
    <li>\
        <span>\
            <input type="radio" name="r" tabindex="-1" />&nbsp;\
            <input class="option_item" type="text" placeholder=" option text" />\
            <a class="remove_option">Remove</a>\
        </span>\
    </li>';
    
var checkbox_item = '\
    <li>\
        <span>\
            <input type="checkbox" tabindex="-1" />&nbsp;\
            <input class="option_item" type="text" placeholder=" option text" />\
            <a class="remove_option">Remove</a>\
        </span>\
    </li>';
    
var field = '\
    <tr class="field_row">\
        <td class="field_cell">\
            <div class="field_settings">\
                <p>Choose type:&nbsp;\
                    <select class="field_type">\
                        <option value="LabelText">LabelText</option>\
                        <option value="LabelImage">LabelImage</option>\
                        <option value="Text">Text</option>\
                        <option value="Number">Number</option>\
                        <option value="Choice">Choice</option>\
                        <option value="Checkbox">Checkbox</option>\
                        <option value="Image">Image</option>\
                        <option value="File">File</option>\
                        <option value="Connection">Connection</option>\
						<option value="NextForm">NextForm</option>\
                    </select>\
                </p>\
                ' + labeltext_settings + '\
            </div>\
            <p>\
                <a class="remove_field">Remove</a> or customize this field.\
            </p>\
        </td>\
    </tr>';
 
var error = "Some error occured while sending data. Try again later.";
 
var redirect = false;


$(function() {
	
	var destElem;

	$(".modal-launcher").click(function () {
		destElem = $(this).siblings(".modal-choice");
		var fpk = $(this).prop('name');
		var table = $(this).siblings(".modal-content").find(".instances");
		var modal = $(this).siblings(".modal-content, .modal-background");
		$.ajax({
			url: $(this).attr('action'),
			method: "POST",
			data: {
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').prop('value'),
				'connection': "instances",
				'form': fpk
			}
		}).done(function (data) {
			table.children().remove();
			table.append(data);
			modal.toggleClass("active");
		}).fail(function () {
			alert(error);
		});
	});
	
	$(".modal-background").click(function () {
		$(this).siblings(".modal-content").toggleClass("active");
		$(this).toggleClass("active");
	});
	
	$('.modal-content').on('click', '.modal-select', function () {
		destElem.children().remove();
		$(this).parent().parent().clone().appendTo(destElem);
		var pk = destElem.find('.modal-select').attr('name');
		destElem.attr('name', pk);
		destElem.find('.modal-select').remove();
	});
		
});
  

var owndbHelpers = {
	
	lostWarning: "Unsaved data will be lost! Are you sure?",
	
	loadingIndicator: function() {
		$(document).bind('ajaxStart', function() {
			$("#loading").show();
		}).bind('ajaxStop', function() {
			$("#loading").hide();
		});
	},
	
	preventRedirection: function() {
		$(window).bind('beforeunload', function () {
			if ($(".field_cell").length > 0 && !redirect)
				return owndbHelpers.lostWarning;
		});
	},
	
	preventAccidentalEnter: function() {
		$('#add_form, #edit_form, #add_forminstance').bind('keypress keydown keyup', function (e) {
			if (e.keyCode == 13) { e.preventDefault(); }
		});
	},
	
	discardChanges: function() {
		$("#cancel_button").click(function (e) {
			redirect = true;
			$(location).attr('href', $(this).prop('name'));
		});
	}
};
 
$(function() {
    
	owndbHelpers.loadingIndicator();
    owndbHelpers.preventRedirection();
    owndbHelpers.preventAccidentalEnter();
    owndbHelpers.discardChanges();

    var $wrapper = $("#fields_wrapper tbody");
    
    //insert field area
    $("#add_field").click(function (e) {
        e.preventDefault();
        $($wrapper).append(field);
        if ($(".field_cell").length == 1)
            $("#submit_button").removeAttr("disabled");
    });

    //remove field area
    $($wrapper).on("click", ".remove_field", function () {
        $(this).parent().closest('tr').remove();
        if ($(".field_cell").length == 0)
            $('#submit_button').attr("disabled", true);
    });

    //insert choice item
    $($wrapper).on("click", ".add_choice", function () {
        $(this).parent().siblings(".options_block").append(choice_item);
    });
    
    //insert checkbox item
    $($wrapper).on("click", ".add_checkbox", function () {
        $(this).parent().siblings(".options_block").append(checkbox_item);
    });
    
    //reorder option list
    $('.options_block').livequery(function() {
        $(this).sortable({
            tolerance: 'pointer',
            cursor: "move",
            axis: "y",
            opacity: 0.75
        });
    });

    //remove option list item
    $($wrapper).on("click", ".remove_option", function () {
        $(this).closest("li").remove();
    });
    
    //reorder field areas
    $($wrapper).sortable({
        tolerance: 'pointer',
        cursor: "move",
        axis: "y",
        opacity: 0.75,
        revert: true,
        start: function (e, ui) {
            ui.placeholder.height(ui.item.height());
        }
    });
	
	//next form button
    $("#fields_render tbody").on("click", ".next_form", function () {
		$('input[name="after_process"]').prop('value', $(this).prop('name'));
		$("#add_forminstance").trigger("submit");
    });
    
    //change field settings area
    $($wrapper).on("change", ".field_type", function () {
        $(this).parent('p').siblings().remove();
        var settings = "";
		var type = $(this).find('option:selected').val();
        switch (type) {
            case "Text":
                settings = text_settings;
                break;
            case "Number":
                settings = number_settings;
                break;
            case "Choice":
                settings = choice_settings;
                break;
            case "Checkbox":
                settings = checkbox_settings;
                break;
            case "Image":
                settings = image_settings;
                break;
            case "File":
                settings = file_settings;
                break;
            case "Connection":
			case "NextForm":
                $.ajax({
                    url: $(this).attr('action'),
                    method: "POST",
                    data: {
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').prop('value'),
                        'connection': "forms"
                    }
                }).done(function (data) {
                    $("#add_form, #edit_form").find(".connection_form").append(data);
                }).fail(function () {
                    alert(error);
                });
				if (type == "Connection")
					settings = connection_settings;
				else
					settings = nextform_settings;
                break;
            case "LabelText":
                settings = labeltext_settings;
                break;
            case "LabelImage":
                settings = labelimage_settings;
                break;
        }
        $(this).parent().closest('div').append(settings);
    });
	
    function progressHandlingFunction(e) {
        if (e.lengthComputable) {
            $('progress').attr({value:e.loaded,max:e.total});
        }
    }
	
    //parse form and send
    $("#add_form, #edit_form").submit(function (e) {
        e.preventDefault();

        var formData = new FormData();
		var csrf = $('input[name="csrfmiddlewaretoken"]').prop('value');
		formData.append('csrfmiddlewaretoken', csrf);

		var title = $("#form_name").val();
        var field_names = [];
        var field_types = [];
        var field_settings = [];
		
		var i = 0;
        $(".field_cell").each(function () {
            field_names[i] = $(this).find(".field_name").val();
            field_types[i] = $(this).find(".field_type").find('option:selected').val();
            switch (field_types[i]) {
                case "Text":
                    field_settings[i] = $(this).find('.notnull').is(':checked') ? "1" : "0";
                    field_settings[i] += $(this).find('.multiline').is(':checked') ? ";1" : ";0";
                    break;
                case "Number":
                    field_settings[i] = $(this).find('.notnull').is(':checked') ? "1" : "0";
                    field_settings[i] += $(this).find('.natural').is(':checked') ? ";1" : ";0";
                    break;
                case "Choice":
                case "Checkbox":
                    field_settings[i] = $(this).find(".option_item").length;
                    $(this).find(".option_item").each(function () {
                        field_settings[i] += ";"+$(this).val();
                    });
                    break;
                case "Image":
                case "File":
                    field_settings[i] = "-";
                    break;
                case "Connection":
				case "NextForm":
                    var formid = $(this).find(".connection_form").find('option:selected').val();
                    field_settings[i] = formid;
                    break;
                case "LabelText":
                    field_settings[i] = $(this).find(".label_text").val();
                    break;
                case "LabelImage":
                    field_settings[i] = "-";
					var file = $(this).find(".label_image").get(0).files[0];
					var label = 'labelimage' + i;
					formData.append(label, file);
                    break;
            }
            i = i + 1;
        });

		formData.append('title', title);
		formData.append('names', JSON.stringify(field_names));
		formData.append('types', JSON.stringify(field_types));
		formData.append('settings', JSON.stringify(field_settings));

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            enctype: 'multipart/form-data',
            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload) {
                    myXhr.upload.addEventListener('progress', progressHandlingFunction, false);
                }
                return myXhr;
            },
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            if (data == "OK") {
                redirect = true;
                $(location).attr('href', $('input[name="after_process"]').prop('value'));
            } else {
				$(".messages").children().remove();
				$(".messages").append("<li>" + data + "</li>");
            }
        }).fail(function () {
            alert(error);
        });
    });

    //parse form and send
    $("#add_forminstance").submit(function (e) {
        e.preventDefault();
		
		var formData = new FormData();
		var csrf = $('input[name="csrfmiddlewaretoken"]').prop('value');
		formData.append('csrfmiddlewaretoken', csrf);
		
		var t = true;
		
        var field_contents = [];
        var i = 0;
        $(".field_render").each(function () {
			switch (true) {
				case $(this).hasClass('Text'):
					field_contents[i] = $(this).find('.textcontent').val();
					break;
				case $(this).hasClass('Number'):
					field_contents[i] = $(this).find('.numbercontent').val();
					break;
				case $(this).hasClass('Choice'):
				case $(this).hasClass('Checkbox'):
					field_contents[i] = $(this).find(".option_item").length;
                    $(this).find(".option_item").each(function () {
                        field_contents[i] += ($(this).is(':checked'))?";1":";0";
                    });
					break;
				case $(this).hasClass('Image'):
					field_contents[i] = "-";
					var file = $(this).find(".image").get(0).files[0];
					var label = 'image' + i;
					formData.append(label, file);
					break;
				case $(this).hasClass('File'):
					field_contents[i] = "-";
					break;
				case $(this).hasClass('Connection'):
					var fpk = $(this).find(".modal-choice").attr('name');
					if (fpk != '')
						field_contents[i] = fpk;
					else {
						field_contents[i] = '';
						t = false;
					}
					break;
				case $(this).hasClass('LabelText'):
				case $(this).hasClass('LabelImage'):
				case $(this).hasClass('NextForm'):
					field_contents[i] = "-";
					break;
			}
            i = i + 1;
        });
		
		if (t==false) {
			$(".messages").children().remove();
			$(".messages").append("<li>You have to choose all instances!</li>");
			return 0;
		}
		
		formData.append('contents', JSON.stringify(field_contents));
        		
		$.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            enctype: 'multipart/form-data',
            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload) {
                    myXhr.upload.addEventListener('progress', progressHandlingFunction, false);
                }
                return myXhr;
            },
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            if (data == "OK") {
                redirect = true;
                $(location).attr('href', $('input[name="after_process"]').prop('value'));
            } else {
				$(".messages").children().remove();
				$(".messages").append("<li>" + data + "</li>");
            }
        }).fail(function () {
            alert(error);
        });
    });
	
});
