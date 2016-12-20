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


/********** Check Broswer ****************************/
function whatBrowser() {
    var ba = ["Edge","Chrome","Firefox","Safari","Opera","MSIE","Trident"];
    var b, ua = navigator.userAgent;
    for(var i=0; i < ba.length; i++){
        if( ua.indexOf(ba[i]) > -1 ){
            b = ba[i];
            return b;
        }
    }
}


/*********************** Index Page loading *****************/
  
window.addEventListener("load", function() {
    var loading = document.getElementById('loading')
    //loading.remove();
    try {
        loading.parentNode.removeChild(loading);
    } catch(e) {
        // statements
        console.log(e);
    }
    document.getElementsByTagName("body")[0].style.cssText = "overflow: auto; background-color:white;"
    
});
    
/**** Check if landscape in mobile **************/

if( window.innerWidth < window.innerHeight) {
    //alert("For better experience use on landscape mode")
    //document.getElementById("landscape_loading").style.cssText = "display:block; color:#fff; font-family: 'courier new';"
}


            /* Side menu for screens smaller than 730px */
document.getElementById("toggle").addEventListener('click', function() {

    if ( document.body.style.backgroundColor != "white")  {
        console.log("close");
        document.getElementById("header").style.cssText = "position: fixed; left: -250px;";
        document.getElementById("toggle").style.cssText = "";
       // document.body.style.backgroundColor = "white" ;
        document.getElementsByTagName("body")[0].style.cssText = "background-color: white;"

    } else {
        console.log("open")
        document.getElementById("header").style.cssText = "position: absolute; left:0px;";
        document.getElementById("toggle").style.cssText = "position: absolute; left:250px;";
        //document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
        document.getElementsByTagName("body")[0].style.cssText = "background-color: #ffffff; overflow: hidden;";
        //document.body.style.cssText = "backgroundColor: rgba(0,0,0,0.4); z-index:101" ;
        //document.body.style.z-index = "101";
    }
});

/*

function open_side_menu(){
    document.getElementById("header").style.cssText = "position: absolute; left:0px;";
    document.getElementById("toggle").style.cssText = "position: absolute; left:250px;";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";


}

function closeNav() {
        document.getElementById("header").style.cssText = "position: fixed; left: -250px;";
        document.getElementById("toggle").style.cssText = "";

        document.body.style.backgroundColor = "white";
}
*/

/*
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
*/

/* *************** Ajax jquery **************/
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


/* ******** Draging  ***************************/


function drag(elem_id) {
    //var el = document.getElementById('draggable');
    var el = elem_id;

    var mover = false, x, y, posx, posy, first = true;
    mover = true;

/*
    el.onmousedown = function() {

        mover = true;
    };
*/
    el.onmouseup = function() {
        mover = false;
        first = true;
    };
    el.onmousemove = function(e) {
        if (mover) {
            if (first) {
                x = e.offsetX;
                y = e.offsetY;
                first = false;
            }
            posx = e.pageX - x;
            posy = e.pageY - y;
            this.style.left = posx + 'px';
            this.style.top = posy + 'px';
        }
    };
}



/************************ Paralax jquery **********************************/

/*/$(window).scroll(function() {
    var wScroll = $(this).scrollTop();

    console.log(wScroll);

    $('#p2_ramka').css ({
      'transform' : 'translate(0px, '+ (wScroll/3-90) + 'px )'
    });
});
*/

/*************** Paralax raw JavaScript  (other way) ********************/

if(whatBrowser() == 'Trident' || whatBrowser() == 'Edge' || whatBrowser() == 'MSIE') { // if IE
    alert('You may experience  "lagging" when using Internet Explorer or Microsoft Edge browser');
}

/**** If Windows Width < 729px stop paralax and bokeh */
var min_width = window.matchMedia( "(min-width: 729px)" ); // window width is 730px or more
min_width.addListener(sizeChange);
sizeChange(min_width);


function sizeChange(min_width) {  

    if (min_width.matches) {
        window.addEventListener('scroll', parallax, false);

    }
    else {
        window.removeEventListener('scroll', parallax, false);
      
    }
}
    


//window.addEventListener('scroll', parallax, false);
try {
    function parallax() {
    
    var yScroll =  document.body.scrollTop;  // how much user scrolls,
    console.log("You scrolled: " + yScroll)

    /**************** Index p1 (hello) **************/

    var ariane = document.getElementById("ariane_img");
    var hello_txt = document.getElementById('hello_txt');
    var hello_header = document.getElementById('hello_header');

    var clouds_left = document.getElementById('clouds_left');
    var clouds_right = document.getElementById('clouds_right');
    if(yScroll < 1300 && (whatBrowser() != 'Trident' || whatBrowser() != 'Edge' || whatBrowser() != 'MSIE')  ){
        //ariane.style.cssText =  'transform: translate(0px, ' + -((yScroll) /1.5) + 'px )'
        hello_txt.style.cssText =  'transform: translateX(0px)' + 'translateY(' + ((yScroll) /2.2) + 'px )'
        //hello_txt.style.cssText =  'transform: translate(0px, ' + ((yScroll) /2.2) + 'px )'
        hello_header.style.cssText =  'transform: translate(0px, ' + ((yScroll) /1.5) + 'px )'
        //clouds_left.style.cssText =  'transform: translate(' + -((yScroll) /3) + 'px,' +  '0px )'
        //clouds_right.style.cssText =  'transform: translate(' + -((yScroll) /6) + 'px,' +  '0px )'
    }


    /*************** Index p2 ***********************/
    var trash = document.getElementById('p2_trash');
    var cactus = document.getElementById('p2_cactus');
    var caffe = document.getElementById('p2_caffe');
    var calculator = document.getElementById('p2_calculator');
    var clip = document.getElementById('p2_clip');
    var clip_big = document.getElementById('p2_clip_big');
    var code_note = document.getElementById('p2_code_note');
    var laptop = document.getElementById('p2_laptop');
    var note_graphs = document.getElementById('p2_note_graphs');
    var pencil_black = document.getElementById('p2_pencil_black');
    var pencil_blue = document.getElementById('p2_pencil_blue');
    var pencil_green = document.getElementById('p2_pencil_green');
    var phone = document.getElementById('p2_phone');
    var ramka = document.getElementById('p2_ramka')

    var index2_bg = document.getElementById('index2_table_note');

    var index2_bgYScroll = index2_bg.offsetTop;  // position of index2_bg  from top

    if(yScroll < 2100){

        if(yScroll > index2_bgYScroll-400){
            ramka.style.cssText =  'transform: translate(0px, ' + ((yScroll-index2_bgYScroll+400) /2.5) + 'px )'
            cactus.style.cssText =  'transform: translate(0px, ' + ((yScroll-index2_bgYScroll+400) /3.2) + 'px )'
            note_graphs.style.cssText =  'transform: translate(' + ((yScroll-index2_bgYScroll+400)/15) + 'px,' + ((yScroll-index2_bgYScroll+400) /5) + 'px )'
            code_note.style.cssText =  'transform: translate(' + ((yScroll-index2_bgYScroll+400)/7) + 'px,' + -((yScroll-index2_bgYScroll+400) /8) + 'px )'
            caffe.style.cssText =  'transform: translate(' + -((yScroll-index2_bgYScroll+400)/15) + 'px,' + ((yScroll-index2_bgYScroll+400) /4.5) + 'px )'
        }
        if(yScroll > index2_bgYScroll-500){

            trash.style.cssText =  'transform: translate(0px, ' + ((yScroll-index2_bgYScroll+500) /6) + 'px )'
            laptop.style.cssText =  'transform: translate(0px, ' + -((yScroll-index2_bgYScroll+500) /5) + 'px )'
            phone.style.cssText =  'transform: translate(' + -((yScroll-index2_bgYScroll+500)/15) + 'px,' + ((yScroll-index2_bgYScroll+500) /4.5) + 'px )'

            //var pencil_black_pos = pencil_black.getBoundingClientRect();

            pencil_black.style.cssText =  'transform: translate(' + -((yScroll-index2_bgYScroll+500)/4) + 'px,' + ((yScroll-index2_bgYScroll+500) /4) + 'px )'
            pencil_blue.style.cssText =  'transform: translate(' + -((yScroll-index2_bgYScroll+500)/10) + 'px,' + 0 + 'px )'

            calculator.style.cssText =  'transform: translate(' + -((yScroll-index2_bgYScroll+500)/15) + 'px,' + ((yScroll-index2_bgYScroll+500) /4.5) + 'px )'
        } 
    }

    } // paralax ()
}
catch(e) {
    console.log(e)
}


