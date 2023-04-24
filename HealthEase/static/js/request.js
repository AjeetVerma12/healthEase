// $('.add').on('click', add);
// $('.remove').on('click', remove);

// function add() {
// var new_chq_no = parseInt($('#total_chq').val()) + 1;
// var new_input = "<input type='text' id='new_" + new_chq_no + "'>";

// $('#new_chq').append(new_input);

// $('#total_chq').val(new_chq_no);
// }

// function remove() {
// var last_chq_no = $('#total_chq').val();

// if (last_chq_no > 1) {
// $('#new_' + last_chq_no).remove();
// $('#total_chq').val(last_chq_no - 1);
// }
// }

$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID
   
    var x = 1; //initlal text box count
	
	
   $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
	
		     //text box increment
            $(wrapper).append('<div><input type="text" name="mytext[]"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
            x++; 
	  }
    });
   
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
       
		e.preventDefault(); 
		$(this).parent('div').remove(); 
		x--;
    })
});