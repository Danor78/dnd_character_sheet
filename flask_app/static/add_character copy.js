function get_attrb(){
    var attrib = {
    "str" : document.querySelector("#str"),
    "dex" : document.querySelector("#dex"),
    "con" : document.querySelector("#con"),
    "int" : document.querySelector("#int"),
    "wis" : document.querySelector("#wis"),
    "cha" : document.querySelector("#cha")
    }
    return attrib
}

function get_profs(){
    var profArray = {
        "str_sav" : ["str", document.querySelector("#str_sav_prof")],
        "dex_sav" : ["dex", document.querySelector("#dex_sav_prof")],
        "con_sav" : ["con", document.querySelector("#con_sav_prof")],
        "int_sav" : ["int", document.querySelector("#int_sav_prof")],
        "wis_sav" : ["wis", document.querySelector("#wis_sav_prof")],
        "cha_sav" : ["cha", document.querySelector("#cha_sav_prof")],
        "acrobatics" : ["dex", document.querySelector("#acrobatics_prof")],
        "animal_handling" : ["wis", document.querySelector("#animal_handling_prof")],
        "arcana" : ["int", document.querySelector("#arcana_prof")],
        "athletics" : ["str", document.querySelector("#athletics_prof")],
        "deception" : ["cha", document.querySelector("#deception_prof")],
        "history" : ["int", document.querySelector("#history_prof")],
        "insight" : ["wis", document.querySelector("#insight_prof")],
        "intimidation" : ["cha", document.querySelector("#intimidation_prof")],
        "investigation" : ["int", document.querySelector("#investigation_prof")],
        "medicine" : ["wis", document.querySelector("#medicine_prof")],
        "nature" : ["int", document.querySelector("#nature_prof")],
        "perception" : ["wis", document.querySelector("#perception_prof")],
        "performance" : ["cha", document.querySelector("#performance_prof")],
        "persuasion" : ["cha", document.querySelector("#persuasion_prof")],
        "religion" : ["int", document.querySelector("#religion_prof")],
        "sleight_of_hand" : ["dex", document.querySelector("#sleight_of_hand_prof")],
        "stealth" : ["dex", document.querySelector("#stealth_prof")],
        "survival" : ["wis", document.querySelector("#survival_prof")]
    };

    return profArray;
}

function get_classes() {
    var classes = document.querySelector('#classes')
    return classes
}

function display_class(element){
    var id = element.value
    var source = "/display_class" + String(id)
    console.log("display class id: ", id)
    document.querySelector("#display_class").setAttribute("src",source)

}

function populate_mods(){
    console.log("___populate mods called___")
    attrb = get_attrb()
    profs = get_profs()

    for (let prof in profs){
        console.log(prof, profs[prof])
        if (profs[prof][1].checked){
            console.log("${prof}_prof is checked")
            var mod = Math.floor(( parseInt(attrb[profs[prof][0]].value)  - 10)/2) + 2
        }
        else{
            var mod = Math.floor(( parseInt(attrb[profs[prof][0]].value)  - 10)/2)
        }
        if (mod > 0){
            mod = '+' + mod.toString()
        }
        else{
            mod = mod.toString()
        }
        document.querySelector("#" + prof + "_mod").innerText = mod
    }
}

function roll_attrib(){
    console.log("\n___Roll_attrib function called____");

    var attrib = get_attrb();

    for (let atb in attrib){
        console.log("\n___atb in loop is____->", atb);
        // console.log("\n___Value at {key}____->", attrib[atb]);
        // console.log("\n___Value at {key}.value____->", attrib[atb].value);

        var rolled_nums = [];
        for (let x=0; x<4; x++){
            // console.log("__x is__",x);
            roll = Math.floor(Math.random() * 6) + 1;
            // console.log("___rolled num___", roll)
            rolled_nums.push(roll);
        }
        console.log("___rolled nums array___", rolled_nums)
        var lowest_index =0;
        for (let x=0; x<4; x++){
            if ( rolled_nums[lowest_index] > rolled_nums[x]){
                lowest_index = x;
            }
        }
        console.log("___lowest index___", lowest_index);
        rolled_nums[lowest_index]= 0;
        console.log("___lowest droped___",rolled_nums);
        // console.log("\n___Rolled nums____->", rolled_nums);

        var sum =0;
        for (let i=0; i<4; i++){
            sum = sum + rolled_nums[i];
        }
        console.log("___Sum value is____->", sum);

        attrib[atb].value = sum
    }
    populate_mods();
}
populate_mods();

function clear_prof(){
    profs = get_profs()

    for (let prof in profs){
        profs[prof][1].checked = false;
        // document.querySelector("#" + prof + "_mod").innerText = "";
    }
    populate_mods()
}

function clear_all(){
    attrb = get_attrb()
    profs = get_profs()

    for (let atb in attrb){
        attrb[atb].value = "1"
    }

    for (let prof in profs){
        profs[prof][1].checked = false;
        document.querySelector("#" + prof + "_mod").innerText = "";
    }

}




console.log("\n___Add Character script added____");
console.log("\n profs", get_profs())