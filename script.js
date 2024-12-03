// Fetch fossil fuel data
d3.json('/api/fossil_fuel_data').then(function(fossilFuelData) {
    // Fetch renewable energy data
    d3.json('/api/renewable_energy_data').then(function(renewableEnergyData) {
        // Create visualizations here
        createEnergyConsumptionChart(fossilFuelData);
        createRenewableShareChart(renewableEnergyData);
    });
});

function createEnergyConsumptionChart(data) {
    // Filter data for the world
    const worldData = data.filter(d => d.Entity === 'World');

    // Set up dimensions
    const margin = {top: 20, right: 20, bottom: 30, left: 50};
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Set up scales
    const x = d3.scaleLinear()
        .domain(d3.extent(worldData, d => d.Year))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(worldData, d => Math.max(d['Gas Consumption (TWh)'], d['Oil Consumption (TWh)'], d['Coal Consumption (TWh)']))])
        .range([height, 0]);

    // Create lines
    const line = d3.line()
        .x(d => x(d.Year))
        .y(d => y(d.value));

    const energyTypes = ['Gas Consumption (TWh)', 'Oil Consumption (TWh)', 'Coal Consumption (TWh)'];
    const color = d3.scaleOrdinal()
        .domain(energyTypes)
        .range(['#1f77b4', '#ff7f0e', '#2ca02c']);

    energyTypes.forEach(type => {
        const typeData = worldData.map(d => ({Year: d.Year, value: d[type]}));
        svg.append("path")
            .datum(typeData)
            .attr("fill", "none")
            .attr("stroke", color(type))
            .attr("stroke-width", 1.5)
            .attr("d", line);
    });

    // Add axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y));

    // Add legend
    const legend = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
        .data(energyTypes)
        .enter().append("g")
        .attr("transform", (d, i) => `translate(0,${i * 20})`);

    legend.append("rect")
        .attr("x", width - 19)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", color);

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(d => d);
}

function createRenewableShareChart(data) {
    // Implementation for renewable share chart
    // Similar to createEnergyConsumptionChart, but with renewable share data
}