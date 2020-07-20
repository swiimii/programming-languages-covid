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

document.getElementById('facts-date').innerText += " " + date_string()
