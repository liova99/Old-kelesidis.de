/* Alternativ way to post data

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

function add_product(obj){

    var formDAta = {
        'product_name'          : $('#product_name').val();
        'product_description'   : $('#product_description').val();
        'product_price'         : $('#product_price').val();
        'availability'          : $('#availability').val();
        'categories'            : $('#categories').val();
    }
    $.ajax({
        url:"/leo_markt_add_product",
        type: "POST",
        data: {formDAta}
    });

    .done(function(data){
        console.log(data);
    })

    event.preventDefault();

}

/* ***************Ajax **************/
function id_num(elem_id)  {

    var details_id = elem_id.id

    $.ajax({
        url: "/leo_markt_details",
        type: 'POST',
        data: {details_id : details_id },
        success: function(data) {
            var result = data;
            obj = JSON.parse(result);
            document.getElementById("show_name").innerHTML =  obj.name;
            document.getElementById("show_description").innerHTML =  obj.description;
            document.getElementById("show_price").innerHTML =  obj.price;
            document.getElementById("show_availability").innerHTML = "Availability " + obj.availability;
            //document.getElementById("show_category").innerHTML =  obj.category;
            // modal
            // $("div#results").text(data);
        }
    });
    return false;
}

/* ******** Modals  ***************************/

var modal = document.getElementById('add_product');
var modal_2 = document.getElementById('edit_categories');
var modal_3 = document.getElementById('show_details_box');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if ((event.target == modal) || (event.target == modal_2) || (event.target == modal_3)) {
        modal.style.display = "none";
        modal_2.style.display = "none";
        modal_3.style.display = "none";
    }
}

