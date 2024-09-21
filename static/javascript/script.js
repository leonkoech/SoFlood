function initAutocomplete() {
  // Create the search box and link it to the UI element.
  const input = document.getElementById("search");
  const options = {
    fields: ["formatted_address", "geometry", "name"],
    strictBounds: false,
  };
  const searchBox = new google.maps.places.Autocomplete(input, options);

  google.maps.event.addListener(searchBox, 'place_changed', function() {
    const place = searchBox.getPlace();
    console.log(place.geometry.location.lat());
    console.log(place.geometry.location.lng());
  });
}

window.initAutocomplete = initAutocomplete;
