function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  // (See 15,2,5)  ** NOTE to self, backticks ` NOT single quote' **
  // Use d3 to select the panel with id of `#sample-metadata`

  // Use `.html("") to clear any existing metadata

  // Use `Object.entries` to add each key and value pair to the panel
  // Hint: Inside the loop, you will need to use d3 to append new
  // tags for each key-value in the metadata.
  // (see 14,3,5 bonus?)

  

  // d3.json(`/metadata/${sample}`).then((data) => {

  var url = `/metadata/${sample}`;
  d3.json(url).then((x) => {

    var sample_metadata = d3.select("#sample-metadata");

    sample_metadata.html("");

    Object.entries(x).forEach(([key, value]) => {
      sample_metadata.append("h6").text(`${key}: ${value}`);
    });

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
    buildGauge(x.WFREQ);

  })

}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  var chart_url = `/samples/${sample}`;
  d3.json(chart_url).then((d) => {
    var otu_ids = d.otu_ids;
    var sample_values = d.sample_values;
    var otu_labels = d.otu_labels;

    // @TODO: Build a Bubble Chart using the sample data
    var trace1 = {
      x: otu_ids,
      y: sample_values,
      text: otu_labels,
      mode: "markers",
      marker: {
        size: sample_values,
        color: otu_ids
      }
    }
    var data = [trace1];

    var layout = {
      showlegend: false,
      xaxis: {title: "OTU ID"},
    }

    Plotly.newPlot("bubble", data, layout);

      // @TODO: Build a Pie Chart
      // HINT: You will need to use slice() to grab the top 10 sample_values,
      // otu_ids, and labels (10 each).

    var trace2 = {
      labels: otu_ids.slice(0, 10),
      values: sample_values.slice(0, 10),
      hovertext: otu_labels.slice(0, 10),
      type: "pie"
    };

    var pie_data = [trace2];

    var pie_layout = {
      height: 475,
      width: 475
    };

    Plotly.newPlot("pie", pie_data, pie_layout);

  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
