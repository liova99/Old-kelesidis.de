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


            /* Side menu for screens smaller than 730px */
document.getElementById("toggle").addEventListener('click', function() {

    if ( document.body.style.backgroundColor != "white")  {
        console.log("close");
        document.getElementById("header").style.cssText = "position: fixed; left: -250px;";
        document.getElementById("toggle").style.cssText = "";
        document.getElementsByTagName("body")[0].style.cssText = "background-color: white;"

    } else {
        console.log("open")
        document.getElementById("header").style.cssText = "position: absolute; left:0px;";
        document.getElementById("toggle").style.cssText = "position: absolute; left:250px;";
        document.getElementsByTagName("body")[0].style.cssText = "background-color: #ffffff; overflow: hidden;";
    }
});


/*************** Paralax raw JavaScript  ********************/
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
    hello_txt.style.cssText =  'transform: translateX(0px)' + 'translateY(' + ((yScroll) /2.2) + 'px )'
    hello_header.style.cssText =  'transform: translate(0px, ' + ((yScroll) /1.5) + 'px )'
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



/* ************************************* Leo Market Page **********************************************/


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
