/* 
 * Owndb client-side logic file.
 *
 */

var field_name = '<p><input class="field_name" type="text" placeholder=" set field name" required /></p>';
var field_name_label = '<p><input class="field_name" type="hidden" value="label" /></p>';

var text_settings = field_name + '<p>Not null: <input class="notnull" type="checkbox" /> | Multiline: <input class="multiline" type="checkbox" /></p>';
var number_settings = field_name + '<p>Not null: <input class="notnull" type="checkbox" /> | Natural values: <input class="natural" type="checkbox" /></p>'
var choice_settings = field_name + '<p><a class="add_choice">Add option</a></p><ul class="options_block"></ul>';
var checkbox_settings = field_name + '<p><a class="add_checkbox">Add option</a></p><ul class="options_block"></ul>';
var image_settings = field_name + '<p><input class="image" disabled type="file" accept=".png,.gif,.jpg,.jpeg" /></p>';
var file_settings = field_name + '<p><input class="file" disabled type="file" /></p>';
var connection_settings = field_name + '<p>Select form and field:&nbsp;<select class="connection_form"></select>&nbsp;<select class="connection_field"></select></p>';
var labeltext_settings = field_name_label + '<p><input class="label_text" type="text" placeholder=" set text" /></p>';
var labelimage_settings = field_name_label + '<p><input class="label_image" type="file" accept=".png,.gif,.jpg,.jpeg" /></p>';

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
						<option value="LabelText">Text label</option>\
						<option value="LabelImage">Image label</option>\
						<option value="Text">Plain text</option>\
						<option value="Number">Number</option>\
						<option value="Choice">Choice (single)</option>\
						<option value="Checkbox">Checkbox (multiple)</option>\
						<option value="Image">Image</option>\
						<option value="File">File</option>\
						<option value="Connection">Connection</option>\
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
    	
	//set up a loading indicator
	$(document).bind("ajaxStart", function() {
		$("#loading").show();
	}).bind("ajaxStop", function() {
		$("#loading").hide();
	});
	
	//prevent redirection
    $(window).bind('beforeunload', function () {
        if ($(".field_cell").length > 0 && !redirect)
            return 'Unsaved data will be lost! Are you sure?';
    });
	
    //prevent accidental enter
    $('#add_form, #edit_form, #add_forminstance').bind('keypress keydown keyup', function (e) {
        if (e.keyCode == 13) { e.preventDefault(); }
    });
	
	//discard changes
    $("#cancel_button").click(function (e) {
        redirect = true;
		$(location).attr('href', $('input[name="after_process"]').prop('value'));
    });

});
 
$(function() {
		
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
	
	//change field list of form in connection settings
	$($wrapper).on("change", ".connection_form", function () {
		
		$.ajax({
			url: $(this).attr('action'),
			method: "POST",
			data: {
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').prop('value'),
				'connection': "field",
				'form': $(".connection_form").find('option:selected').val()
			}
		}).done(function (data) {
			$("#add_form, #edit_form").find(".connection_field").children().remove();
			$("#add_form, #edit_form").find(".connection_field").append(data);
		}).fail(function () {
			alert(error);
		});

    });
	
    //change field settings area
    $($wrapper).on("change", ".field_type", function () {
        $(this).parent('p').siblings().remove();
        var settings = "";
        switch ($(this).find('option:selected').val()) {
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

				$.ajax({
					url: $(this).attr('action'),
					method: "POST",
					data: {
						'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').prop('value'),
						'connection': "form"
					}
				}).done(function (data) {
					$("#add_form, #edit_form").find(".connection_form").append(data);
					$(".connection_form").trigger("change");
				}).fail(function () {
					alert("Some error occured while sending data. Try again later.");
				});

                settings = connection_settings;
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

    //parse form and send
    $("#add_form, #edit_form").submit(function (e) {
		e.preventDefault();

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
					field_settings[i] = "none";
					break;
				case "Connection":
					var formid = $(this).find(".connection_form").find('option:selected').val();
					var fieldid = $(this).find(".connection_field").find('option:selected').val();
					field_settings[i] = formid + ";" + fieldid;
					break;
				case "LabelText":
					field_settings[i] = $(this).find(".label_text").val();
					break;
				case "LabelImage":
					field_settings[i] = "primary_key_of_image_object";
					break;
				default:
					field_settings[i] = "error";
					break;
			}
            i = i + 1;
        });

        $.ajax({
            url: $(this).attr('action'),
            method: "POST",
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').prop('value'),
				'connection': "false",
				'title': title,
                'names': field_names,
                'types': field_types,
				'settings': field_settings
            }
        }).done(function (data) {
            if (data == "OK") {
				redirect = true;
				$(location).attr('href', $('input[name="after_process"]').prop('value'));
			} else {
				alert(data);
			}
        }).fail(function () {
            alert(error);
        });
    });
	
	//parse form and send
    $("#add_forminstance").submit(function (e) {
		e.preventDefault();
		
		var field_contents = [];
		var i = 0;
        $(".field_render").each(function () {
			if ($(this).find('.textcontent').length > 0) {
				field_contents[i] = $(this).find('.textcontent').val();
			} else {
				field_contents[i] = "temp answer";
			}
            i = i + 1;
        });
		
        $.ajax({
            url: $(this).attr('action'),
            method: "POST",
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').prop('value'),
				'contents': field_contents
            }
        }).done(function (data) {
            if (data == "OK") {
				redirect = true;
				$(location).attr('href', $('input[name="after_process"]').prop('value'));
			} else {
				alert(data);
			}
        }).fail(function () {
            alert(error);
        });
    });

});
