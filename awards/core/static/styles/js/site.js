var cities;
function getCities() {
    $.getJSON("/cities/list", function (rez) {
        cities = rez;
    })
}
function loadCity(obj){
    path = obj.val();
    if(path && path != 0) go(path);
    else loadCountry($("#selectCountry"))
}
function loadCountry(obj){
    path = obj.val();
    if(path && path != 0) go(path);
    else go("/");
}
function go(path)
{
    window.location.href = path;
}
function createCitiesList(container) {
    var availableCity = [];
    $.getJSON("/cities/list", function (cities) {
        $.each(cities, function (key, val) {
            availableCity.push(val);
        });
        $("#"+container).autocomplete({
            source: availableCity
        });
    })
}
function setMenuActive(){
    var currentUrl = window.location.href;
    if($(".site-menu").length){
        $(".site-menu").each(function(){
            $(this).find("a").each(function(){
                var aHref = $(this).attr("href").replace(/\?/g,"/?");
                if(aHref == currentUrl) $(this).closest("li").addClass("active");
            })
        })
    }
}
$(function () {
    setMenuActive();
    $.mask.definitions['~'] = "[+-]";
    $(".phoneformat").mask("+7 (999) 999-99-99");
});