/* Requires JQuery... */


var popup_record = function(animal_id) {
    var oReq = new XMLHttpRequest();

    var write_html = function() {
        $("#popup-content").html(this.responseText);
    };

    oReq.addEventListener("load", write_html);
    oReq.open("GET", "/popup/" + animal_id);
    oReq.send();
    $("#popup-content").text("Fetching Pet Record, please wait...")
    $("#popup").show();
};


var popup_text = function(data) {
    $("#popup-content").text(data)
    $("#popup").show();
};


var kill_popup = function() {
    $("#popup").hide();
};
