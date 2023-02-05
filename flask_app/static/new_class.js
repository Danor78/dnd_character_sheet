function add_description_box(){
    console.log("add_description called")
    org_div = document.getElementById("description_section_1")
    descript_num = parseInt(document.querySelector("#descript_num").value) + 1;
    console.log("descript_num", descript_num);
    console.log("descript_num", typeof(descript_num));

    const div = document.createElement("div");
    div.classList.add("mt-3")
    const descipt_label1 = document.createElement("label");
    descipt_label1.for = "desc_heading_" + descript_num
    text = document.createTextNode("Class Description Heading");
    strong = document.createElement("strong");
    strong.appendChild(text);
    descipt_label1.appendChild(strong);
    descipt_label1.classList.add("mr-2")
    div.appendChild(descipt_label1);
    input = document.createElement("input");
    input.type = "text";
    input.name = "desc_heading_" + descript_num;
    div.appendChild(descipt_label1);
    div.appendChild(input);

    div_desc = document.createElement("div");
    div_desc.setAttribute("class","d-flex align-items-center")

    const descipt_labe2= document.createElement("label");
    descipt_labe2.for = "description_" + descript_num;
    text = document.createTextNode("Class Description");
    strong = document.createElement("strong");
    strong.appendChild(text);
    descipt_labe2.appendChild(strong);
    descipt_labe2.setAttribute("class","mr-2");
    div_desc.appendChild(descipt_labe2);

    textarea = document.createElement("textarea");
    textarea.name = "description_" + descript_num;
    textarea.setAttribute("id", "class_description_" + descript_num);
    textarea.setAttribute("cols","63");
    textarea.setAttribute("rows","5");
    div_desc.appendChild(textarea);
    div.appendChild(div_desc)

    document.querySelector("#descript_num").value = descript_num

    org_div.appendChild(div)
}

function add_feature_box(){
    console.log("add_feature called")
    org_div = document.getElementById("feature_container")
    feature_num = parseInt(document.querySelector("#feature_num").value) + 1;
    console.log("feature_num", feature_num);
    console.log("feature_num", typeof(feature_num));

    const div = document.createElement("div");
    div.classList.add("mt-3");
    const descipt_label1 = document.createElement("label");
    descipt_label1.for = "feature_name_" + feature_num
    text = document.createTextNode("Class Feature Name: ");
    strong = document.createElement("strong");
    strong.appendChild(text);
    descipt_label1.appendChild(strong);
    descipt_label1.classList.add("mr-2");
    div.appendChild(descipt_label1);
    input = document.createElement("input");
    input.type = "text";
    input.name = "feature_name_" + feature_num;
    div.appendChild(descipt_label1);
    div.appendChild(input);
    div.appendChild(document.createElement("br"));

    feat_lvl = document.createElement("label");
    feat_lvl.classList.add("mr-2");
    feat_lvl.for = "feature_level_" + feature_num;
    text = document.createTextNode("Level Feature is implemented: ");
    strong = document.createElement("strong");
    strong.appendChild(text);
    feat_lvl.appendChild(strong);
    div.appendChild(feat_lvl);
    // div.appendChild(document.createElement("br"));

    select = document.createElement("select");
    select.name = "feature_level_" + feature_num;
    for (let i=1; i<=20; i++){
        option = document.createElement("option");
        option.value = i;
        num = document.createTextNode(i);
        option.appendChild(num);
        select.appendChild(option)
    }
    div.appendChild(select)

    div_desc = document.createElement("div");
    div_desc.setAttribute("class","d-flex align-items-center")

    const descipt_labe2= document.createElement("label");
    descipt_labe2.for = "feature_descript_" + feature_num;
    text = document.createTextNode("Feature Description: ");
    strong = document.createElement("strong");
    strong.appendChild(text);
    descipt_labe2.appendChild(strong);
    descipt_labe2.setAttribute("class","mr-2");
    div_desc.appendChild(descipt_labe2);

    textarea = document.createElement("textarea");
    textarea.name = "feature_descript_" + feature_num;
    textarea.setAttribute("id", "feature_descript_" + feature_num);
    textarea.setAttribute("cols","63");
    textarea.setAttribute("rows","5");
    div_desc.appendChild(textarea);
    div.appendChild(div_desc)

    document.querySelector("#feature_num").value = feature_num

    org_div.appendChild(div)
}