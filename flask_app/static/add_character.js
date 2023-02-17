

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


function display_background(element){
    var id = element.value
    console.log("display background id: ", id)
    if (id == "" || id == "null"){
        document.querySelector("#display_background").setAttribute("src","")
        return
    }
    var source = "/show_background/" + String(id) + "/False"
    document.querySelector("#display_background").setAttribute("src",source)

}

function display_alignment(element){
    console.log("display_alignment_called")
    // const algn = document.querySelector("#alignment").value
    const algn = JSON.parse(document.querySelector("#alignment").value); 
    // console.log("algn = ", algn)
    chosen_algn = element.value
    console.log("chosen_algn = ", chosen_algn)
    console.log("algn,chosen_algn = ", algn[chosen_algn]  )
    document.querySelector(".alignment_desc").innerText = algn[chosen_algn]

}

const algn = JSON.parse(document.querySelector("#alignment").value); 


document.querySelector(".alignment_desc").innerText = algn['definition']