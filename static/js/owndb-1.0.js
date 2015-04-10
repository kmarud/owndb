/* 
 * Owndb client-side logic file.
 *
 */

var text_settings = '\
	<p>Not null: <input class="notnull" type="checkbox" /> | Multiline: <input class="multiline" type="checkbox" /></p>';
	
var number_settings = '\
	<p>Not null: <input class="notnull" type="checkbox" /> | Natural values: <input class="natural" type="checkbox" /></p>'

var choice_settings = '\
	<p><a class="add_option">Add option</a></p>\
	<ul class="options_block"></ul>';

var checkbox_settings = '\
	<p><a class="add_checkbox">Add option</a></p>\
	<ul class="options_block"></ul>';
	
var picture_settings = '<p><input class="picture" type="file" accept=".png,.gif,.jpg,.jpeg" /></p>';
var file_settings = '<p><input class="file" type="file" /></p>';
var connection_settings = '\
	<p>Select form and field:&nbsp;\
		<select class="connection_form"></select>&nbsp;\
		<select class="connection_field"></select>\
	</p>';
var labeltext_settings = '<p><input class="label_text" type="text" placeholder=" set label text" /></p>';
var labelimage_settings = '<p><input class="label_image" type="file" accept=".png,.gif,.jpg,.jpeg" /></p>';
	
var choice_item = '\
	<li>\
		<span>\
			<input type="radio" name="r" tabindex="-1" />&nbsp;\
			<input class="radio_field" type="text" placeholder=" set option name" />\
			<a class="remove_option">Remove</a>\
		</span>\
	</li>';
	
var checkbox_item = '\
	<li>\
		<span>\
			<input type="checkbox" tabindex="-1" />&nbsp;\
			<input class="radio_field" type="text" placeholder=" set option name" />\
			<a class="remove_option">Remove</a>\
		</span>\
	</li>';
	
var field = '\
	<tr class="field_row">\
		<td class="field_cell">\
			<p>\
				<input class="field_name" type="text" placeholder=" field name" required />\
			</p>\
			<div class="field_settings">\
				<p>Choose type:&nbsp;\
					<select class="field_type">\
						<option value="Text">Plain text</option>\
						<option value="Number">Number</option>\
						<option value="Choice">Choice (single)</option>\
						<option value="Checkbox">Checkbox (multiple)</option>\
						<option value="Picture">Picture</option>\
						<option value="File">File upload</option>\
						<option value="Connection">Connection</option>\
						<option value="LabelText">Text label</option>\
						<option value="LabelImage">Image label</option>\
					</select>\
				</p>\
				' + text_settings + '\
			</div>\
			<p>\
				<a class="remove_field">Remove</a> or customize this field.\
			</p>\
		</td>\
	</tr>';
 
var redirect = false;

$(function() {
    	
	//set up a loading indicator
	$(document).bind("ajaxStart", function() {
		$("#loading").show();
	}).bind("ajaxStop", function() {
		$("#loading").hide();
	});
	
    $(window).bind('beforeunload', function () {
        if ($(".field_cell").length > 0 && !redirect)
            return 'Unsaved data will be lost! Are you sure?';
    });
	
    //prevent accidental enter
    $('#edit_form, #add_form, #add_forminstance').bind('keypress keydown keyup', function (e) {
        if (e.keyCode == 13) { e.preventDefault(); }
    });

});
 
$(function() {
		
	var $wrapper = $("#fields_wrapper tbody");
	
	//insert field area
    $("#add_field").click(function (e) {
        e.preventDefault();
        $($wrapper).append(field);
        if ($(".field_cell").length == 1)
            $("#submit_button").get(0).type = 'submit';
    });

	//remove field area
    $($wrapper).on("click", ".remove_field", function () {
        $(this).parent().closest('tr').remove();
        if ($(".field_cell").length == 0)
            $('#submit_button').get(0).type = 'hidden';
    });

    //insert choice item
    $($wrapper).on("click", ".add_option", function () {
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
	
	//change list of fields in connection settings
	$($wrapper).on("change", ".connection_form", function () {
        	
		var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

		$.ajax({
			url: $(this).attr('action'),
			method: "POST",
			data: {
				'csrfmiddlewaretoken': token,
				'connection': "field",
				'form': $(".connection_form").find('option:selected').val()
			}
		}).done(function (data) {
			$("#add_form, #edit_form").find(".connection_field").children().remove();
			$("#add_form, #edit_form").find(".connection_field").append(data);
		}).fail(function () {
			alert("Some error occured while sending data. Try again later.");
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
			case "Picture":
                settings = picture_settings;
                break;
			case "File":
                settings = file_settings;
                break;
			case "Connection":
				
				var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

				$.ajax({
					url: $(this).attr('action'),
					method: "POST",
					data: {
						'csrfmiddlewaretoken': token,
						'connection': "true"
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
    $("#add_form").submit(function (e) {
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
					var q = $(this).find(".radio_field").length;
					field_settings[i] = q;
					$(this).find(".radio_field").each(function () {
						field_settings[i] += ";"+$(this).val();
					});
					break;
				case "Picture":
				case "File":
				case "LabelImage":
					//url or foreign key of image model will be fine, but we have to send image meanwhile via different ajax request
					field_settings[i] = "-;-";
					break;
				case "Connection": 
					//here will be foreign key of connection (as show at erd diagrams) but we'll do it in view, now send form and field ids.
					field_settings[i] = "formid;fieldid;additionalsettings";
					break;
				case "LabelText":
					field_settings[i] = $(this).find(".label_text").val();
					break;
				default:
					field_settings[i] = "not supported";
					break;
			}
            i = i + 1;
        });
		
		var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

        $.ajax({
            url: $(this).attr('action'),
            method: "POST",
            data: {
                'csrfmiddlewaretoken': token,
				'title': title,
                'names': field_names,
                'types': field_types,
				'settings': field_settings,
				'connection': "false"
            }
        }).done(function (data) {
            if (data == "OK") {
				redirect = true;
				$(location).attr('href', $('input[name="after_process"]').prop('value'));
			} else {
				alert(data);
			}
        }).fail(function () {
            alert("Some error occured while sending data. Try again later.");
        });
    });
	
	//parse form and send
    $("#edit_form").submit(function (e) {
		e.preventDefault();
		
		var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

        $.ajax({
            url: $(this).attr('action'),
            method: "POST",
            data: {
                'csrfmiddlewaretoken': token,
				'connection': "false"
            }
        }).done(function (data) {
            if (data == "OK") {
				redirect = true;
				$(location).attr('href', $('input[name="after_process"]').prop('value'));
			} else {
				alert(data);
			}
        }).fail(function () {
            alert("Some error occured while sending data. Try again later.");
        });
    });
	
	//parse form and send
    $("#add_forminstance").submit(function (e) {
		e.preventDefault();
		
		var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

        $.ajax({
            url: $(this).attr('action'),
            method: "POST",
            data: {
                'csrfmiddlewaretoken': token
            }
        }).done(function (data) {
            if (data == "OK") {
				redirect = true;
				$(location).attr('href', $('input[name="after_process"]').prop('value'));
			} else {
				alert(data);
			}
        }).fail(function () {
            alert("Some error occured while sending data. Try again later.");
        });
    });

});
