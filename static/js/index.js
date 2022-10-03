var overiew_data = [
    {
        "tankno":"1",
        "product":"Xăng RON92",
        "level":"123",
        "avgtemp":"22.1",
        "density":"0.1",
        "vcf":"0.3",
        "grossvolume":"123.4256",
        "netvolume":"123.4253",
        "mass":"124",
    },
    {
        "tankno":"2",
        "product":"Xăng RON92",
        "level":"123",
        "avgtemp":"22.1",
        "density":"0.1",
        "vcf":"0.3",
        "grossvolume":"123.4256",
        "netvolume":"123.4253",
        "mass":"124",
    },
    {
        "tankno":"3",
        "product":"Xăng RON95",
        "level":"123",
        "avgtemp":"22.1",
        "density":"0.1",
        "vcf":"0.3",
        "grossvolume":"123.4256",
        "netvolume":"123.4253",
        "mass":"124",
    },
    {
        "tankno":"4",
        "product":"index1",
        "level":"123",
        "avgtemp":"22.1",
        "density":"0.1",
        "vcf":"0.3",
        "grossvolume":"123.4256",
        "netvolume":"123.4253",
        "mass":"124",
    },
    {
        "tankno":"1",
        "product":"index1",
        "level":"123",
        "avgtemp":"22.1",
        "density":"0.1",
        "vcf":"0.3",
        "grossvolume":"123.4256",
        "netvolume":"123.4253",
        "mass":"124",
    },
]

var dropdown_index = 0;
var dropdown_maping_data = ["Xăng RON92", "Xăng RON95", "Dầu DO 0.05S", "Xăng E5 RON92"];
function change_option(value){
    // convert to int   
    dropdown_index = parseInt(value);
    update_total_value();
}
function update_data_table() {
    var table_body = document.getElementById("data-table");
    table_body.innerHTML = "";
    for (var i = 0; i < overiew_data.length; i++) {
        var row = table_body.insertRow(i);
        // add view_detail event
        row.onclick = function() {
            view_detail(this.rowIndex);
        }
        var tankno = row.insertCell(0);
        // add class
        tankno.className = "align-middle text-center text-sm";
        tankno.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + overiew_data[i].tankno + '</span></td>';
        var product = row.insertCell(1);
        product.className = "align-middle text-center text-sm";
        product.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + overiew_data[i].product + '</span></td>';
        var level = row.insertCell(2);
        level.className = "align-middle text-center text-sm";
        level.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + overiew_data[i].level + '</span></td>';
        var avgtemp = row.insertCell(3);
        avgtemp.className = "align-middle text-center text-sm";
        // convert to float with 2 decimal places
        avgtemp.innerHTML = '<td class="align-middle text-center text-sm"><span class="badge badge-sm bg-gradient-success">' + parseFloat(overiew_data[i].avgtemp).toFixed(2) + '</span></td>';
        var density = row.insertCell(4);
        density.className = "align-middle text-center text-sm";
        // 1 decimal place
        density.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + parseFloat(overiew_data[i].density).toFixed(1) + '</span></td>';
        var vcf = row.insertCell(5);
        vcf.className = "align-middle text-center text-sm";
        // 1 decimal place
        vcf.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + parseFloat(overiew_data[i].vcf).toFixed(1) + '</span></td>';
        var grossvolume = row.insertCell(6);
        grossvolume.className = "align-middle text-center text-sm";
        // 3 decimal places
        grossvolume.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + parseFloat(overiew_data[i].grossvolume).toFixed(3) + '</span></td>';
        var netvolume = row.insertCell(7);
        netvolume.className = "align-middle text-center text-sm";
        // 3 decimal places
        netvolume.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + parseFloat(overiew_data[i].netvolume).toFixed(3) + '</span></td>';
        var mass = row.insertCell(8);
        mass.className = "align-middle text-center text-sm";
        // 3 decimal places
        mass.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + parseFloat(overiew_data[i].mass).toFixed(3) + '</span></td>';
    }
}

function update_total_value(){
    // grossvolume
    var grossvolume = 0;
    var netvolume = 0;
    var mass = 0;
    for (var i = 0; i < overiew_data.length; i++) {
        if (overiew_data[i].product == dropdown_maping_data[dropdown_index]) {
            {
                grossvolume += parseFloat(overiew_data[i].grossvolume);
                netvolume += parseFloat(overiew_data[i].netvolume);
                mass += parseFloat(overiew_data[i].mass);
            }
            }
    }
    
    // update total value in #total-table
    var table_body = document.getElementById("total-table");
    table_body.innerHTML = "";
    var row = table_body.insertRow(0);
    var grossvolume_cell = row.insertCell(0);
    grossvolume_cell.className = "align-middle text-center text-sm";
    grossvolume_cell.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + grossvolume.toFixed(3) + '</span></td>';
    var netvolume_cell = row.insertCell(1);
    netvolume_cell.className = "align-middle text-center text-sm";
    netvolume_cell.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + netvolume.toFixed(3) + '</span></td>';
    var mass_cell = row.insertCell(2);
    mass_cell.className = "align-middle text-center text-sm";
    mass_cell.innerHTML = '<td class="align-middle text-center text-sm"><span class="text-secondary text-sm font-weight-bold">' + mass.toFixed(3) + '</span></td>';
}

function view_detail(row_index){
    console.log("view detail of row " + row_index);
    // put value to modal
    var tankno = document.getElementById("tankno");
    tankno.innerHTML = "TANK "+overiew_data[row_index-1].tankno;
    var product = document.getElementById("product");
    product.innerHTML = overiew_data[row_index-1].product;
    var level = document.getElementById("level");
    level.innerHTML = overiew_data[row_index-1].level;
    var avgtemp = document.getElementById("avgtemp");
    avgtemp.innerHTML = overiew_data[row_index-1].avgtemp;
    var density = document.getElementById("density");
    density.innerHTML = overiew_data[row_index-1].density;
    var vcf = document.getElementById("vcf");
    vcf.innerHTML = overiew_data[row_index-1].vcf;
    var grossvolume = document.getElementById("grossvolume");
    grossvolume.innerHTML = overiew_data[row_index-1].grossvolume;
    var netvolume = document.getElementById("netvolume");
    netvolume.innerHTML = overiew_data[row_index-1].netvolume;
    var mass = document.getElementById("mass");
    mass.innerHTML = overiew_data[row_index-1].mass;
    $('#modal').modal('show');
    // settimout
    setTimeout(function(){
        var width = document.getElementById("tank_image").offsetWidth;
        var height = document.getElementById("tank_image").offsetHeight;
        // 
        var level_image = document.getElementById("level_image");
        // set 40% of width
        level_image.style.width = width * 0.15 + "px";
        level_image.style.height = height * 0.678 + "px";
    }, 500);
}

// handle socketio event from flask
// # socketio.emit("mqtt_message", data, namespace="/test")
// @socketio.on("mqtt_message", namespace="/test")
// def handle_mqtt_message(message):
//     print("message received: ", message)
//     socketio.emit("mqtt_message", message, namespace="/test")
// import socketio
document.addEventListener('DOMContentLoaded', () => {
    var server_address = 'http://127.0.0.1:5000';
    var socket = io(server_address);

    socket.on('connect', () => {
        console.log("connect");
    }
    );

    socket.on('disconnect', () => {
        console.log("disconnect");
    }
    );

    socket.on('mqtt_message', (data) => {
        console.log("mqtt_message");
        console.log(data);
        // update data
        update_data_table(data);
        // update table
        update_total_value();
    }
    );

});