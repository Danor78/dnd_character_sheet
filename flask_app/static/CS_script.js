
function get_attrib(){
    var attribArray = [document.querySelector("#str_attrib p").innerText,
    document.querySelector("#dex_attrib p").innerText,
    document.querySelector("#con_attrib p").innerText,
    document.querySelector("#int_attrib p").innerText,
    document.querySelector("#wis_attrib p").innerText,
    document.querySelector("#cha_attrib p").innerText];

    return attribArray;
}

function get_attrib_for_Mods(){
    var attribModArray = [
    document.querySelector("#str_attrib p").innerText,  // str save
    document.querySelector("#dex_attrib p").innerText,  // dex save
    document.querySelector("#con_attrib p").innerText,  // con save
    document.querySelector("#int_attrib p").innerText,  // int save
    document.querySelector("#wis_attrib p").innerText,  // wis save
    document.querySelector("#cha_attrib p").innerText,  // cha save
    document.querySelector("#dex_attrib p").innerText,  // acrobatics
    document.querySelector("#wis_attrib p").innerText,  // animal handling
    document.querySelector("#int_attrib p").innerText,  // arcana
    document.querySelector("#str_attrib p").innerText,  // athletics
    document.querySelector("#cha_attrib p").innerText,  // deception
    document.querySelector("#int_attrib p").innerText,  // history
    document.querySelector("#wis_attrib p").innerText,  // insight
    document.querySelector("#cha_attrib p").innerText,  // intimidation-----
    document.querySelector("#int_attrib p").innerText,  // investigation
    document.querySelector("#wis_attrib p").innerText,  // Medicine
    document.querySelector("#int_attrib p").innerText,  // Nature
    document.querySelector("#wis_attrib p").innerText,  // perception
    document.querySelector("#cha_attrib p").innerText,  // performance
    document.querySelector("#cha_attrib p").innerText,  // persuasion
    document.querySelector("#int_attrib p").innerText,  // religion
    document.querySelector("#dex_attrib p").innerText,  // sleight of hand
    document.querySelector("#dex_attrib p").innerText,  // stealth
    document.querySelector("#wis_attrib p").innerText,  // survival
    document.querySelector("#dex_attrib p").innerText];  // Initiative 

    return attribModArray;
}


function get_profs(){
    var profArray = [document.querySelector("#str_sav_prof"),
    document.querySelector("#dex_sav_prof"),
    document.querySelector("#con_sav_prof"),
    document.querySelector("#int_sav_prof"),
    document.querySelector("#wis_sav_prof"),
    document.querySelector("#cha_sav_prof"),
    document.querySelector("#acrobatics_prof"),
    document.querySelector("#animal_handling_prof"),
    document.querySelector("#arcana_prof"),
    document.querySelector("#athletics_prof"),
    document.querySelector("#deception_prof"),
    document.querySelector("#history_prof"),
    document.querySelector("#insight_prof"),
    document.querySelector("#intimidation_prof"),
    document.querySelector("#investigation_prof"),
    document.querySelector("#medicine_prof"),
    document.querySelector("#nature_prof"),
    document.querySelector("#perception_prof"),
    document.querySelector("#performance_prof"),
    document.querySelector("#persuasion_prof"),
    document.querySelector("#religion_prof"),
    document.querySelector("#sleight_of_hand_prof"),
    document.querySelector("#stealth_prof"),
    document.querySelector("#survival_prof"),
    document.querySelector("#initiative_mod")];


    return profArray;
}

function get_mods(){
    var modArray = [document.querySelector("#str_sav"),
    document.querySelector("#dex_sav"),
    document.querySelector("#con_sav"),
    document.querySelector("#int_sav"),
    document.querySelector("#wis_sav"),
    document.querySelector("#cha_sav"),
    document.querySelector("#acrobatics_mod"),
    document.querySelector("#animal_handling_mod"),
    document.querySelector("#arcana_mod"),

    document.querySelector("#athletics_mod"),
    document.querySelector("#deception_mod"),
    document.querySelector("#history_mod"),
    document.querySelector("#insight_mod"),
    document.querySelector("#intimidation_mod"),
    document.querySelector("#investigation_mod"),
    document.querySelector("#medicine_mod"),
    document.querySelector("#nature_mod"),
    document.querySelector("#perception_mod"),
    document.querySelector("#performance_mod"),
    document.querySelector("#persuasion_mod"),
    document.querySelector("#religion_mod"),
    document.querySelector("#sleight_of_hand_mod"),
    document.querySelector("#stealth_mod"),
    document.querySelector("#survival_mod"),
    document.querySelector("#initiative_mod")
]

    return modArray;
}

// console.log(attribArray);

// Checks if the mod is + or - and prints its correctly
function printMod(element, mod){
    // console.log("print mod is " + mod);
    if (mod == ''){
        element.innerText = '--'
    }else if (mod < 0){
        element.innerText = mod;
    }else if (mod >= 0){
        element.innerText = '+' + mod;
    }
}

//calculates the modifier
function calcMod(attrib, prof){
    // console.log("calcMod attrib is " + attrib); 
    if(attrib == ''){
        return attrib;
    }
    if (prof == true){
        var mod = Math.floor(( attrib - 10)/2) + 2
    }else{
        var mod = Math.floor(( attrib - 10)/2)
    } 
    return mod;
}

// Populate the modifers of the Saving throws and Kills boxes
function populate_savs_and_skills_Values(){
    var attribArray = get_attrib();
    var profArray = get_profs();
    var modArray = get_mods();
    var attribModArray = get_attrib_for_Mods();

    for (var i=0; i<modArray.length; i++){
    // console.log(modArray[i], profArray[i]);/
    console.log(modArray[i], calcMod(attribModArray[i], profArray[i].checked));
    printMod(modArray[i], calcMod(attribModArray[i], profArray[i].checked));
    // console.log("Attribute for " + attribModArray[i] + " is " + calcMod(attribModArray[i],profArray[i].checked));
    }

}

function populate_attrib_mods(){
    var attribArray = get_attrib();
    var element;

    element = document.querySelector("#str_attrib_mod");
    printMod(element, Math.floor((attribArray[0] - 10)/2));

    element = document.querySelector("#dex_attrib_mod");
    printMod(element, Math.floor((attribArray[1] - 10)/2));

    element = document.querySelector("#con_attrib_mod");
    printMod(element, Math.floor((attribArray[2] - 10)/2));

    element = document.querySelector("#int_attrib_mod");
    printMod(element, Math.floor((attribArray[3] - 10)/2));

    element = document.querySelector("#wis_attrib_mod");
    printMod(element, Math.floor((attribArray[4] - 10)/2));

    element = document.querySelector("#cha_attrib_mod");
    printMod(element, Math.floor((attribArray[5] - 10)/2));

}



// Function prommpts the user for the value to change the attribute then changes it
function changeAttrib(element, attrib_type){
    var trueAttrib = false;
    while (trueAttrib == false){
        var attrib = prompt("Enter in the numeric value 0 - 20 for the " + attrib_type + " attribute")
        if (attrib >= 0 && attrib <= 20){
            trueAttrib = true;
        }
    }
    element.innerText = attrib;
    if (attrib_type == "Strength"){
        // console.log("Strength Mod");
        element = document.querySelector("#str_attrib_mod");
        printMod(element, Math.floor((attrib - 10)/2));
    }else if (attrib_type == "Dexerity"){
        // console.log("Dexerity Mod");
        element = document.querySelector("#dex_attrib_mod");
        printMod(element, Math.floor((attrib - 10)/2));
    }else if (attrib_type == "Constatution"){
        // console.log("Constatution Mod");
        element = document.querySelector("#con_attrib_mod");
        printMod(element, Math.floor((attrib - 10)/2));
    }else if (attrib_type == "Intelligence"){
        // console.log("Intelegence Mod");
        element = document.querySelector("#int_attrib_mod");
        printMod(element, Math.floor((attrib - 10)/2));
    }else if (attrib_type == "Wisdom"){
        // console.log("Wisdom Mod");
        element = document.querySelector("#wis_attrib_mod");
        printMod(element, Math.floor((attrib - 10)/2));
    }else if (attrib_type == "Charisma"){
        // console.log("Charisma Mod");
        element = document.querySelector("#cha_attrib_mod");
        printMod(element, Math.floor((attrib - 10)/2));
    }

    populate_savs_and_skills_Values();
}

function toggleRadio(element){
    console.log("Radio toggled " + element.checked)
    if (element.checked == true){
        element.checked = false;
    }//else{
    //     element.checked = true;
    // }
}

populate_savs_and_skills_Values();
populate_attrib_mods();


// This updates the <p> element at the top of the menu with the selection what was made
function change_selection(element, title){
    // console.log("Title tag is " + title)
    document.querySelector('#' + title).innerText = element.innerText;
}

var first_hp_update = true
function update_current_hp(){
    element = document.querySelector(".current_hp");
    console.log("current hp inner text is ",element.innerText)
    if(first_hp_update){
        console.log("first time updated current hp fired")
        element.innerText = Number(document.querySelector("#hp_max").value) + Number(document.querySelector("#temp_hp").value);
        first_hp_update = false
    }
    else{
        element.innerText = Number(document.querySelector("#temp_hp").value);
    }
}

update_current_hp()

function adjust_hp(type){
    max_hp = document.querySelector("#hp_max").value;
    current_hp = document.querySelector(".current_hp").innerText;
    current_hp = Number(current_hp);
    // console.log("current hp is " + current_hp)
    // console.log(typeof(current_hp));
    adjustment_hp = Number(document.querySelector("#hp_change").value);
    // adjustment_hp = document.querySelector("#hp_change").innerText
    // console.log("adjusted hp is " , typeof(adjustment_hp))
    // console.log(typeof(hp_change));


    if( type == 'Heal'){
        // console.log("Heal button was clicked")
        current_hp = Number(current_hp) +  adjustment_hp;
        if( Number(current_hp) > max_hp){
            current_hp = max_hp;
        }
    }
    if( type == 'Damage'){
        // console.log("damage button was clicked")

        if (Number(document.querySelector("#temp_hp").value) > 0){
            document.querySelector("#temp_hp").value -= adjustment_hp;
            if (Number(document.querySelector("#temp_hp").value) < 0){
                current_hp += Number(document.querySelector("#temp_hp").value)
                document.querySelector("#temp_hp").value = 0
            }


        }

        current_hp -= adjustment_hp;
        // console.log("current hp type is", typeof(current_hp))
        if( current_hp < 0 ){
            current_hp = 0;
        }
    }
    document.querySelector(".current_hp").innerText = current_hp;
    console.log("Updated current hp is " + current_hp)

}

