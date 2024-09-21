let contentDiv = document.getElementById('content');
let resultsDiv = document.getElementById('results');
let results = document.getElementById('resultsContent');

function initAutocomplete() {
  // Create the search box and link it to the UI element.
  const input = document.getElementById("search");
  const options = {
    fields: ["formatted_address","address_components", "geometry", "name"],
    strictBounds: false,
  };
  const searchBox = new google.maps.places.Autocomplete(input, options);

  google.maps.event.addListener(searchBox, 'place_changed', function () {
    const place = searchBox.getPlace();
    var lat =  place.geometry.location.lat()
    var long = place.geometry.location.lng()
    var zip = ""



    console.log(place.geometry.location.lat());
    console.log(place.geometry.location.lng());
    for(let address_component of place.address_components){
      if(address_component["types"]?.includes("postal_code")){
        zip = address_component["short_name"]
      }
    }


    fetch(`http://127.0.0.1:5000/make_flood_prediction?zip=${zip}&lat=${lat}&long=${long}`).then((val)=>{
      console.log(val.json().then((value)=>{
        contentDiv.style.display = "none";
        resultsDiv.style.display = "block";
        results.innerHTML = JSON.stringify(value);
        return value;
      }))
    })
    // http://127.0.0.1:5000/make_flood_prediction?zip=33179&lat=59.91&long=10.75
  });
}

window.initAutocomplete = initAutocomplete;