/* 
 * Owndb client-side logic.
 * Designing new form script.
 */

$(function () {

    var $wrapper = $("#fields_wrapper tbody");
    
    var plaintext_settings = '<p>Content can be nullable: <input class="nullable" type="checkbox" /></p>';

    //insert field area
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
                                <option value="text">Plain text</option>\
                                <option value="number">Number</option>\
                                <option value="choice">Choice (single)</option>\
                                <option value="checkbox">Checkbox (multiple)</option>\
                                <option value="picture">Picture</option>\
                                <option value="file">File upload</option>\
                                <option value="connection">Connect with other form</option>\
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

    //remove field area
    $($wrapper).on("click", ".remove_field", function () {
        $(this).parent().closest('tr').remove();
        if ($(".field_cell").length == 0)
            $('#add_button').get(0).type = 'hidden';
    });

    var number_settings = '<p>This field accepts all type of numbers.</p>'

    var choice_settings = '<p class="options_block"><a class="add_option" style="cursor:pointer">Add option</a></p>';


    //insert radio option
    $($wrapper).on("click", ".add_option", function () {
        $(this).parent().append(
            '<div><input type="radio" /> <input class="radio_field" type="text" placeholder=" set option name" />\
             <a class="remove_option" style="cursor:pointer">Remove</a></div>'
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
            case "text":
                settings = plaintext_settings;
                break;
            case "number":
                settings = number_settings;
                break;
            case "choice":
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
    }).disableSelection();

    $('#add_form').bind('keypress keydown keyup', function (e) {
        if (e.keyCode == 13) { e.preventDefault(); }
    });

    var process_address = "/store/add_form/"
    var after_process = "/store/"

    var token = $('input[name="csrfmiddlewaretoken"]').prop('value');

    //parse form and send
    $("#add_form").submit(function (e) {
        e.preventDefault();

        //here we parse form to send data to server
        var field_quantity = $(".field_cell").length;

        var field_names = [];
        var i = 0;
        $(".field_name").each(function () {
            field_names[i] = $(this).val();
            i = i + 1;
        });

        $.ajax({
            url: process_address,
            method: "POST",
            data: {
                csrfmiddlewaretoken: token,
                number: field_quantity,
                names: field_names
            }
        }).done(function (data) {
            alert(data); //check data, if there are some errors display them, if no redirect
        }).fail(function () {
            alert("Some error occured while sending data. Try again later.");
        }).always(function () {
            alert("Now we redirect you to your project view.");
            redirect = true;
            $(location).attr('href', after_process);
        });
    });

});
