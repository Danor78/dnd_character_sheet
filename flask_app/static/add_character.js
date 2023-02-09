

function get_classes() {
    var classes = document.querySelector('#classes')
    return classes
}

function display_class(element){
    var id = element.value
    console.log("display class id: ", id)
    if (id == "" || id == "null"){
        document.querySelector("#display_class").setAttribute("src","")
        return
    }
    var source = "/display_class/" + String(id)
    document.querySelector("#display_class").setAttribute("src",source)

}

function display_race(element){
    var id = element.value
    console.log("display race id: ", id)
    if (id == "" || id == "null"){
        document.querySelector("#display_race").setAttribute("src","")
        return
    }
    var source = "/display_race/" + String(id) + "/False"
    document.querySelector("#display_race").setAttribute("src",source)

}
