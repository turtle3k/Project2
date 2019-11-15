// Creating map object
var map = L.map('map').setView([37.8, -96], 4);

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
}).addTo(map);




var link = "static/data/usStates.geojson";
var totalevents = "static/data/nmbr_events.json";

d3.json(link, function (data) {
  d3.json(totalevents, function (nbreventdata) {
    var nbreventsmap = {};
    nbreventdata.forEach(function (event) {nbreventsmap[event.STATE] = event.NMBR_EVENTS; });
    L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        feature.properties.nbrofevents = nbreventsmap[feature.properties.name] 

  layer.on({
    // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
    mouseover: function (event) {
      layer = event.target;
      layer.setStyle({
        fillOpacity: 0.9
      });
    },
    // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
    mouseout: function (event) {
      layer = event.target;
      layer.setStyle({
        fillOpacity: 0.5
      });
    },
    // When a feature (neighborhood) is clicked, it is enlarged to fit the screen
    click: function (event) {
      map.fitBounds(event.target.getBounds());
    }
  });
  // Giving each feature a pop-up with information pertinent to it
  layer.bindPopup("<h5>" + feature.properties.name + "</h5>" + "<br>" + "<h5>"+ "Total Natural Disasters:" + feature.properties.nbrofevents + "</h5>");
}
  }).addTo(map);
})
});
