'use strict'

function date_string() {
	const today = new Date()
	return today.toDateString()
}

function get_file(url) {
	const request = new XMLHttpRequest()
	// This throws a warning about synchronous requests being deprecated
	request.open('GET',url,false)
	request.send()
	return request.responseText
}

function parse_csv(csv_str, drop=3) {
	const rows = csv_str.split("\r\n").slice(drop)
	return rows.map(function (row) {return row.split(",")})
}

function create_dropdown_option(name, dropdown) {
	const el = document.createElement("option")
	el.textContent = name
	el.value = name
	dropdown.appendChild(el)
}

function get_selected_region() {
	const dropdown = document.getElementById("region")
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
	const region = get_selected_region()
	const facts = get_facts(region, csv)

	const total_cases = facts[0]
	const total_deaths = facts[1]
	const deaths_per_100k = facts[2]
	const cases_7_days = facts[3]
	const cases_per_100k = facts[4]

	document.getElementById('fact-1').innerText = "Since the start of the pandemic, there have been " + total_cases + " COVID-19 cases in " + region + ". " + total_deaths + " people have died from the disease."
	document.getElementById('fact-2').innerText = "This means for every 100,000 people in " + region + ", " + cases_per_100k + " people have caught COVID-19, and " + deaths_per_100k + " have died."
	document.getElementById('fact-3').innerText = "In the last 7 days alone, there have been " + cases_7_days + " cases in " + region + "."
}

document.getElementById('facts-date').innerText += " " + date_string()

const case_data = get_file('https://www.cdc.gov/covid-data-tracker/Content/CoronaViewJson_01/US_MAP_DATA.csv')
const case_data_csv = parse_csv(case_data)

const dropdown = document.getElementById("region")
const options = case_data_csv.map(function (x) {return x[2]})
options.map(function (region) {create_dropdown_option(region, dropdown)})
