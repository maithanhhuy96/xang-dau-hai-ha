function save_image(){
    // send image to server
    // from <input type='file' id="imageInput" onchange="save_image()" name="imageInput" accept="image/*"/>
    var image = document.getElementById("imageInput").files[0];
    var form_data = new FormData();
    form_data.append("image", image);
    // fetch
    fetch("/save_image", {
        method: "POST",
        body: form_data
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // set src image #map_image
        var map_image = document.getElementById("map_image");
        console.log("../static/images/"+data.image_name)
        map_image.src = "../static/images/"+data.image_name;
        alert("Image saved successfully");
    })


}
