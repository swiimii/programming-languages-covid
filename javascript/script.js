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

function update_facts() {
	let region = get_selected_region()
	document.getElementById('fact-1').innerText = "You chose " + region
	document.getElementById('fact-2').innerText = "You chose " + region
	document.getElementById('fact-3').innerText = "You chose " + region
}

document.getElementById('facts-date').innerText += " " + date_string()

let cdc_data = get_cdc_data()
let cdc_data_csv = parse_csv(cdc_data)

let dropdown = document.getElementById("region")
let options = cdc_data_csv.map(function (x) {return x[2]})
options.map(function (region) {create_dropdown_option(region, dropdown)})
