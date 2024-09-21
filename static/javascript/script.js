window.lat = 0;
window.lng = 0;
window.zip = 0;

let contentDiv = document.getElementById('content');
let resultsDiv = document.getElementById('results');
let results = document.getElementById('resultsContent');

function initAutocomplete() {
  // Create the search box and link it to the UI element.
  const input = document.getElementById("search");
  const options = {
    fields: ["formatted_address", "address_components", "geometry", "name"],
    strictBounds: false,
  };
  const searchBox = new google.maps.places.Autocomplete(input, options);

  google.maps.event.addListener(searchBox, 'place_changed', function() {
    const place = searchBox.getPlace();
    var lat = place.geometry.location.lat()
    var long = place.geometry.location.lng()
    var zip = ""

    //console.log(place.geometry.location.lat());
    //console.log(place.geometry.location.lng());
    for (let address_component of place.address_components) {
      if (address_component["types"]?.includes("postal_code")) {
        zip = address_component["short_name"]
      }
    }

    window.lat = lat;
    window.lng = long;
    window.zip = zip;

    const submitBtn = document.querySelector('#submit-btn');
    submitBtn.disabled = false;
  });
}

window.initAutocomplete = initAutocomplete;
