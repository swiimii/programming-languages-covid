'use strict'

function date_string() {
	const today = new Date()
	return today.toDateString()
}

function get_cdc_data() {
	let request = new XMLHttpRequest()
	// This throws a warning about synchronous requests being deprecated
	request.open('GET','https://www.cdc.gov/covid-data-tracker/Content/CoronaViewJson_01/US_MAP_DATA.csv',false)
	request.send()
	return request.responseText
}

function parse_csv(csv_str) {
	let rows = csv_str.split("\r\n").slice(3)
	return rows.map(function (row) {return row.split(",")})
}

function create_dropdown_option(name, dropdown) {
	let el = document.createElement("option")
	el.textContent = name
	el.value = name
	dropdown.appendChild(el)
}

function get_selected_region() {
	let dropdown = document.getElementById("region")
	return dropdown.options[dropdown.selectedIndex].value
}

function get_facts(region, csv) {
	if (csv[0][2] === region) {
		return csv[0].slice(3)
	} else {
		return get_facts(region, csv.slice(1))
	}
}

function update_facts(csv) {
	let region = get_selected_region()
	let facts = get_facts(region, csv)

	let total_cases = facts[0]
	let total_deaths = facts[1]
	let deaths_per_100k = facts[2]
	let cases_7_days = facts[3]
	let cases_per_100k = facts[4]

	document.getElementById('fact-1').innerText = "Since the start of the pandemic, there have been " + total_cases + " COVID-19 cases in " + region + ". " + total_deaths + " people have died from the disease."
	document.getElementById('fact-2').innerText = "This means for every 100,000 people in " + region + ", " + cases_per_100k + " people have caught COVID-19, and " + deaths_per_100k + " have died."
	document.getElementById('fact-3').innerText = "In the last 7 days alone, there have been " + cases_7_days + " cases in " + region + "."
}

document.getElementById('facts-date').innerText += " " + date_string()

let cdc_data = get_cdc_data()
let cdc_data_csv = parse_csv(cdc_data)

let dropdown = document.getElementById("region")
let options = cdc_data_csv.map(function (x) {return x[2]})
options.map(function (region) {create_dropdown_option(region, dropdown)})
