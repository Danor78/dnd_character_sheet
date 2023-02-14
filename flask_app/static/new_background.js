function add_description_box(){
    console.log("add_description called")
    org_div = document.getElementById("description_section_1")
    description_num = parseInt(document.querySelector("#description_num").value) + 1;
    console.log("description_num", description_num);
    console.log("description_num", typeof(description_num));

    const div = document.createElement("div");
    div.classList.add("mt-3");
    const descipt_label1 = document.createElement("label");
    descipt_label1.for = "description_heading_" + description_num
    text = document.createTextNode("Background Description Heading: ");
    strong = document.createElement("strong");
    strong.appendChild(text);
    descipt_label1.appendChild(strong);
    descipt_label1.classList.add("mr-2");
    div.appendChild(descipt_label1);
    input = document.createElement("input");
    input.type = "text";
    input.name = "description_heading_" + description_num;
    div.appendChild(descipt_label1);
    div.appendChild(input);
    // div.appendChild(document.createElement("br"));

    div_desc = document.createElement("div");
    div_desc.setAttribute("class","d-flex align-items-center")

    const descipt_labe2= document.createElement("label");
    descipt_labe2.for = "description_" + description_num;
    text = document.createTextNode("Background Description: ");
    strong = document.createElement("strong");
    strong.appendChild(text);
    descipt_labe2.appendChild(strong);
    descipt_labe2.setAttribute("class","mr-2");
    div_desc.appendChild(descipt_labe2);

    textarea = document.createElement("textarea");
    textarea.name = "description_" + description_num;
    textarea.setAttribute("id", "description_" + description_num);
    textarea.setAttribute("cols","63");
    textarea.setAttribute("rows","5");
    div_desc.appendChild(textarea);
    div.appendChild(div_desc)

    document.querySelector("#description_num").value = description_num

    org_div.appendChild(div)
}