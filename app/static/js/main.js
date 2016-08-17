

/*
function id_num(elem_id){
    var details_id = elem_id.id
    $.post(
    "/leo_markt_details",
    {details_id : details_id},
    function(data) {
        $('div#results').text(data);
    });
}

*/

function id_num(elem_id)  {
    
    var details_id = elem_id.id

    $.ajax({
        url: "/leo_markt_details",
        type: 'POST',
        data: {details_id : details_id },
        success: function(data) {
            $("div#results").text(data);
        }
    });
    return false;
}


// Get the modal
var modal = document.getElementById('add_product');
var modal_2 = document.getElementById('edit_categories');


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal || event.target == modal_2) {
        modal.style.display = "none";
        modal_2.style.display = "none";

    }
}





