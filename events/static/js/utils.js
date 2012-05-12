function submit_form_ajax(form_element, success_func) {
    // Function takes a jQuery <form> element.It is also possible 
    // to define a function to call after the submit is done.
    var data = form_element.serializeArray();
    $.ajax({
        type : form_element.attr('method'),
        url  : form_element.attr('action'),
        data : data,
        success : function(response) {
            if(typeof(success_func) != 'undefined')
                success_func(response);
            else
		$('#main').html(response);
        }, error : function() {
            alert('error :(');
        }
    });
    return false;
}