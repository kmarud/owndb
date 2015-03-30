/* 
 * Adding new form client-side logic.
 */

$(function add_new_form() {

    var $wrapper = $("#fields_wrapper tbody");
    
    var plaintext_settings = '\
		<p>Not null: <input class="notnull" type="checkbox" /> | Multiline: <input class="multiline" type="checkbox" /></p>';
		
	var number_settings = '\
		<p>Not null: <input class="notnull" type="checkbox" /> | Natural values: <input class="natural" type="checkbox" /></p>'

    var choice_settings = '\
		<p class="options_block">\
			<a class="add_option" style="cursor:pointer">Add option</a>\
		</p>';

    $("#add_field").click(function (e) {
        e.preventDefault();
        $($wrapper).append(
            '<tr class="field_row">\
                <td class="field_cell" style="background-color:#fafafa; padding:5px; border-bottom:5px solid #fff; width:600px">\
                    <p>\
                        <input class="field_name" type="text" placeholder=" set field name" style="width:250px" />\
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
                                <option value="Connection">Connect with other form</option>\
                            </select>\
                        </p>\
                        ' + plaintext_settings + '\
                    </div>\
                    <p>\
                        <a class="remove_field" style="cursor:pointer">Remove</a> or customize this field.\
                    </p>\
                </td>\
            </tr>'
        );
        if ($(".field_cell").length == 1)
            $('#add_button').get(0).type = 'submit';
    });

    $($wrapper).on("click", ".remove_field", function () {
        $(this).parent().closest('tr').remove();
        if ($(".field_cell").length == 0)
            $('#add_button').get(0).type = 'hidden';
    });

    //insert radio option
    $($wrapper).on("click", ".add_option", function () {
        $(this).parent().append('\
			<div>\
				<input type="radio" name="r" />&nbsp;\
				<input class="radio_field" type="text" placeholder=" set option name" />\
				<a class="remove_option" style="cursor:pointer">Remove</a>\
			</div>'
        );
    });

    //remove radio option
    $($wrapper).on("click", ".remove_option", function () {
        $(this).parent().remove();
    });

    //changing area settings
    $($wrapper).on("change", ".field_type", function () {
        $(this).parent('p').siblings().remove();
        var settings = "";
        switch ($(this).find('option:selected').val()) {
            case "Text":
                settings = plaintext_settings;
                break;
            case "Number":
                settings = number_settings;
                break;
            case "Choice":
                settings = choice_settings;
                break;
            default:
                settings = '<p>This type is not implemented yet...</p>';
                break;
        }
        $(this).parent().closest('div').append(settings);
    });


    var redirect = false;
    
    $(window).bind('beforeunload', function () {
        if ($(".field_cell").length > 0 && !redirect)
            return 'Your form will be lost! Are you sure?';
    });

    //reordering field areas
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
	
	//preventing accidental enter
    $('#add_form').bind('keypress keydown keyup', function (e) {
        if (e.keyCode == 13) { e.preventDefault(); }
    });

	
    var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

    //parse form and send
    $("#add_form").submit(function (e) {
        e.preventDefault();

		var title = $("#form_name").val();
		
        var field_quantity = $(".field_cell").length;

        var field_names = [];
        var i = 0;
        $(".field_name").each(function () {
            field_names[i] = $(this).val();
            i = i + 1;
        });

        var field_types = [];
        var i = 0;
        $(".field_type").each(function () {
            field_types[i] = $(this).find('option:selected').val();
            i = i + 1;
        });
		
		var after_process = $(this).attr('action');
		var process_address = after_process + "/add_form/";

        $.ajax({
            url: process_address,
            method: "POST",
            data: {
                'csrfmiddlewaretoken': token,
				'title': title,
                'number': field_quantity,
                'names': field_names,
                'types': field_types
            }
        }).done(function (data) {
            if (data == "OK") {
				redirect = true;
				$(location).attr('href', after_process);
			} else {
				alert(data);
			}
        }).fail(function () {
            alert("Some error occured while sending data. Try again later.");
        });
    });

});
