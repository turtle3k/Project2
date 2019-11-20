/**
 * 
 * @param {*} chartID The html chart div
 * @param {*} state the currently selected state to build
 */
function buildRadarChart(chartID, state) {
  // console.log(`Radar Chart: Passed ChartID: ${chartID}`);
  var urlAll = '/pieinfo'
  var urlState = `/pieinfo?state=${state}`
  var pa_type = []; // list for pie all events (labels)
  var pa_nbr = [];  // list of values (nbr events)
  var ps_type = [];  //  These are for pie state values
  var ps_nbr = [];

  d3.json(urlAll).get(function (pieall) {
    // console.log(`Pie All: ${pieall}`);
    pieall.forEach(function (allItem) {
      //  console.log(`Pie All Item: ${allItem}`);
      // console.log(`Event Type: ${allItem.EVENT_TYPE}, Number: ${allItem.NBR_EVENT}`);
      pa_type.push(allItem.EVENT_TYPE);
      pa_nbr.push(allItem.NBR_EVENT);
    });

    d3.json(urlState).get(function (pieState) {
      // console.log(`Pie State: ${pieState}`);
      pieState.forEach(function (stateItem) {
        ps_type.push(stateItem.EVENT_TYPE);
        ps_nbr.push(stateItem.NBR_EVENT);
      });


      // console.log(`pa_type: ${pa_type}`)
      // console.log(`pa_nbr: ${pa_nbr}`)
      // console.log(`ps_nbr: ${ps_nbr}`)

      // Now build the rader chart

      new Chart(document.getElementById(chartID), {
        type: 'radar',
        data: {
          // labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
          labels: pa_type,
          datasets: [
            {
              label: "All Events",
              fill: true,
              backgroundColor: "rgba(179,181,198,0.2)",
              borderColor: "rgba(179,181,198,1)",
              pointBorderColor: "#fff",
              pointBackgroundColor: "rgba(179,181,198,1)",
              data: pa_nbr
            }, {
              label: "State Events",
              fill: true,
              backgroundColor: "rgba(255,99,132,0.2)",
              borderColor: "rgba(255,99,132,1)",
              pointBorderColor: "#fff",
              pointBackgroundColor: "rgba(255,99,132,1)",
              pointBorderColor: "#fff",
              data: ps_nbr
            }
          ]
        },
        options: {

          title: {
            display: true,
            text: 'All Events/State Events'
          },
          tooltips: {
            enabled: true,
            mode: 'single',
            callbacks: {
              label: function (tooltipItems, data) {
                return tooltipItems.yLabel + ' ' + tooltipItems.xLabel;
              }
            }

          }
        }
      });

    });
  });
} // End buildRadarChart



// Animation - animate on scroll - https://github.com/michalsnik/aos
AOS.init({
  duration: 1200,
});

// Creating map object
var map = L.map('map').setView([37.8, -96], 4);

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
}).addTo(map);


var link = "/../static/data/usStates.geojson";
// var totalevents = "/../static/data/nmbr_events.json";
var totalevents = "/api/disasters"
// var totaleventdata = []

d3.json(link, function (data) {
  d3.json(totalevents, function (nbreventdata) {
    var nbreventsmap = {};
    // nbreventdata.forEach(function (event) { nbreventsmap[event.STATE] = event.NMBR_EVENTS; });
    nbreventdata.forEach(function (event) { nbreventsmap[event.state] = event.number_events; });
    L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        feature.properties.nbrofevents = nbreventsmap[feature.properties.name]
        // totaleventdata = nbreventsmap
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
              fillOpacity: 0.2
            });
          },
          // When a feature (neighborhood) is clicked, it is enlarged to fit the screen
          click: function (event) {
            var nameinit = feature.properties.name
            map.fitBounds(event.target.getBounds());
            buildCharts(nameinit);
            buildMetadata(nameinit);
            d3.select("#selDataset").html("");
            d3.select("#selDataset").append("option").text(nameinit);
          }
        });
        // Giving each feature a pop-up with information pertinent to it
        layer.bindPopup("<h5>" + feature.properties.name + "</h5>" + "<br>" + "<h5>" + "Total Natural Disasters:" + feature.properties.nbrofevents + "</h5>");
      }
    }).addTo(map);

  })
});


//Main Pie Chart
var counts = []
var events = []

d3.json("/pieinfo").get(function (pieinfo) {
  pieinfo.forEach(function (item) {
    counts.push(item.NBR_EVENT);
    events.push(item.EVENT_TYPE)
  })
  var ptrace = {
    values: counts,
    labels: events,
    textinfo: events,
    type: "pie",
  }
  var pdata = [ptrace]

  var layout = {
    title: "Distribution of Natural Disasters<br>" + "2000 - 2018 in USA"
  }

  Plotly.newPlot("pie", pdata, layout)

});

//Main Line Graph
var flood_deaths = []
var flood_years = []
var tornado_deaths = []
var tornado_years = []
var wildfire_deaths = []
var wildfire_years = []
d3.json("/lineinfo").get(function (lineinfo) {
  lineinfo.forEach(function (item) {
    if (item.EVENT_TYPE == "Flood") {
      flood_deaths.push(item.DEATHS);
      flood_years.push(item.YEAR)
    }
    else if (item.EVENT_TYPE == "Tornado") {
      tornado_deaths.push(item.DEATHS);
      tornado_years.push(item.YEAR)
    }
    else {
      wildfire_deaths.push(item.DEATHS);
      wildfire_years.push(item.YEAR)
    }
  })
  var floodtrace = {
    x: flood_years,
    y: flood_deaths,
    type: "scatter",
    name: "Flood"
  };

  var tornadotrace = {
    x: tornado_years,
    y: tornado_deaths,
    type: "scatter",
    name: "Tornado"
  };

  var wildfiretrace = {
    x: wildfire_years,
    y: wildfire_deaths,
    type: "scatter",
    name: "Wild Fire"
  }

  var linedata = [floodtrace, tornadotrace, wildfiretrace]

  var layout = {
    title: {
      text: 'Number of deaths by disaster type in USA'
    },
    xaxis: {
      title: {
        text: 'Year'
      },
    },
    yaxis: {
      title: {
        text: 'Number of deaths',
      }
    }
  };

  Plotly.newPlot("line", linedata, layout)
})


function buildMetadata(state) {
  d3.json(`/pieinfo?state=${state}`).get((data) => {
    var sampleData = d3.select("#sample-metadata")
    sampleData.html("")
    data.forEach(function (item) {
      sampleData.append("h6").text(`${item.EVENT_TYPE}: ${item.NBR_EVENT}`)
    });
  });
}

function buildCharts(state) {
  // console.log(`IN BUILD CHARTS`)
  var localcounts = []
  var localevents = []

  d3.json(`/pieinfo?state=${state}`).get((pieinfo) => {
    pieinfo.forEach(function (item) {
      localcounts.push(item.NBR_EVENT);
      localevents.push(item.EVENT_TYPE)
    })
    var ptrace = {
      values: localcounts,
      labels: localevents,
      textinfo: localevents,
      type: "pie",
    }
    var pdata = [ptrace]

    var layout = {
      title: `Distribution of Natural Disasters <br>` + `2000 - 2018 in ${state}`
    }

    Plotly.newPlot("pie", pdata, layout)

  });
  //Local Line Graph
  var local_flood_deaths = []
  var local_flood_years = []
  var local_tornado_deaths = []
  var local_tornado_years = []
  var local_wildfire_deaths = []
  var local_wildfire_years = []
  d3.json(`/lineinfo?state=${state}`).get(function (lineinfo) {
    lineinfo.forEach(function (item) {
      if (item.EVENT_TYPE == "Flood") {
        local_flood_deaths.push(item.DEATHS);
        local_flood_years.push(item.YEAR)
      }
      else if (item.EVENT_TYPE == "Tornado") {
        local_tornado_deaths.push(item.DEATHS);
        local_tornado_years.push(item.YEAR)
      }
      else {
        local_wildfire_deaths.push(item.DEATHS);
        local_wildfire_years.push(item.YEAR)
      }
    })
    var local_floodtrace = {
      x: local_flood_years,
      y: local_flood_deaths,
      type: "scatter",
      name: "Flood"
    };

    var local_tornadotrace = {
      x: local_tornado_years,
      y: local_tornado_deaths,
      type: "scatter",
      name: "Tornado"
    };

    var local_wildfiretrace = {
      x: local_wildfire_years,
      y: local_wildfire_deaths,
      type: "scatter",
      name: "Wild Fire"
    }

    var local_linedata = [local_floodtrace, local_tornadotrace, local_wildfiretrace]

    var layout = {
      title: {
        text: `Number of deaths by disaster type in ${state}`
      },
      xaxis: {
        title: {
          text: 'Year'
        },
      },
      yaxis: {
        title: {
          text: 'Number of deaths',
        }
      }
    };

    Plotly.newPlot("line", local_linedata, layout)
  })

  // Finally, now that we have a state, build the
  // Radar Chart
  buildRadarChart('radar-chart', state);  

};


