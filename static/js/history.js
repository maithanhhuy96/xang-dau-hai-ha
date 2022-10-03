function get_tank_data(){
    // get tank value from #tank option
    var tank = document.getElementById("tank").value;
    // tank_from_date: "YYYY-MM-DD HH:MM:SS"
    var tank_from_date = document.getElementById("tank_from_date").value.replace("T", " ");
    // tank_to_date: "YYYY-MM-DD HH:MM:SS"
    var tank_to_date = document.getElementById("tank_to_date").value.replace("T", " ");
    console.log("tank: " + tank);
    console.log("tank_from_date: " + tank_from_date);
    console.log("tank_to_date: " + tank_to_date);
    // check if 3 values are not empty
    if (tank != "" && tank_from_date != "" && tank_to_date != "") {

        // fetch
        fetch("/tank_history", {
            method: "POST",
            body: JSON.stringify({
                tank: tank,
                tank_from_date: tank_from_date,
                tank_to_date: tank_to_date
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            data = data.data;
            // update table-body: #tank-table
            var table_body = document.getElementById("tank-table");
            table_body.innerHTML = "";
            for (var i = 0; i < data.length; i++) {
                var row = data[i];
                var row_html = "<tr>";
                row_html += "<td>" + row["storedata"] + "</td>";
                row_html += "<td>" + row["tankno"] + "</td>";
                row_html += "<td>" + row["product"] + "</td>";
                row_html += "<td>" + row["level"] + "</td>";
                row_html += "<td>" + row["avgtemp"] + "</td>";
                row_html += "<td>" + row["density"] + "</td>";
                row_html += "<td>" + row["grossvolume"] + "</td>";
                row_html += "<td>" + row["netvolume"] + "</td>";
                row_html += "<td>" + row["mass"] + "</td>";
                row_html += "</tr>";
                table_body.innerHTML += row_html;
            }
        }
        )
    }
    else {
        alert("Please fill all the fields");
    }
}

function get_product_data(){
    // get product value from #product option
    var product = document.getElementById("product").value;
    // product_from_date: "YYYY-MM-DD HH:MM:SS"
    var product_from_date = document.getElementById("product_from_date").value.replace("T", " ");
    // product_to_date: "YYYY-MM-DD HH:MM:SS"
    var product_to_date = document.getElementById("product_to_date").value.replace("T", " ");
    console.log("product: " + product);
    console.log("product_from_date: " + product_from_date);
    console.log("product_to_date: " + product_to_date);
    // check if 3 values are not empty
    if (product != "" && product_from_date != "" && product_to_date != "") {

        // fetch
        fetch("/product_history", {
            method: "POST",
            body: JSON.stringify({
                product: product,
                product_from_date: product_from_date,
                product_to_date: product_to_date
            })
        })
        .then(response => response.json())
        .then(data => {
            // update table-body: #product-table
            var table_body = document.getElementById("product-table");
            table_body.innerHTML = "";
            data = data.data;
            for (var i = 0; i < data.length; i++) {
                var row = data[i];
                var row_html = "<tr>";
                row_html += "<td>" + row["storedata"] + "</td>";
                row_html += "<td>" + row["product"] + "</td>";
                row_html += "<td>" + row["totalgrossvolume"] + "</td>";
                row_html += "<td>" + row["totalnetvolume"] + "</td>";
                row_html += "<td>" + row["totalmass"] + "</td>";
                row_html += "</tr>";
                table_body.innerHTML += row_html;
            }
        }
        )
    }
    else {
        alert("Please fill all the fields");
    }
}