window.onload = function loadmenu() {

    var menu = document.getElementById("menu");

    menu.onclick = function myfunction() {
        var x = document.getElementById("myTopnav");

        if(x.className == "topnav") {
            x.className += " responsive";
        } else{
            x.className = "topnav";
        }
    }
}