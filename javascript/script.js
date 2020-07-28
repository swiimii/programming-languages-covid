'use strict'

function date_string() {
	const today = new Date()
	return today.toDateString()
}

/*
 * Downloads the file at the given URL.
 */
function get_file(url) {
	const request = new XMLHttpRequest()
	// This throws a warning about synchronous requests being deprecated
	request.open('GET',url,false)
	request.send()
	return request.responseText
}

/*
 * Splits the CSV string grabbed from the CDC website into a list of lists. The
 * drop argument will drop the first n rows from the return value.
 */
function parse_csv(csv_str, drop=3) {
	const rows = csv_str.split("\r\n").slice(drop)
	return rows.map(function (row) {return row.split(",")})
}

/*
 * Adds name as an option to the given dropdown element.
 */
function create_dropdown_option(name, dropdown) {
	const el = document.createElement("option")
	el.textContent = name
	el.value = name
	dropdown.appendChild(el)
}

/*
 * Returns the region currently selected in the dropdown menu.
 */
function get_selected_region() {
	const dropdown = document.getElementById("region")
	return dropdown.options[dropdown.selectedIndex].value
}

function update_case_facts(csv) {
	const region = get_selected_region()
	const region_row = csv.filter(function (x) {if (x[2] === region) {return true}})[0]
	const facts = region_row.slice(3)

	const total_cases = facts[0]
	const total_deaths = facts[1]
	const deaths_per_100k = facts[2]
	const cases_7_days = facts[3]
	const cases_per_100k = facts[4]

	document.getElementById('fact-1').innerText = "Since the start of the pandemic, there have been " + total_cases + " COVID-19 cases in " + region + ". " + total_deaths + " people have died from the disease."
	document.getElementById('fact-2').innerText = "This means for every 100,000 people in " + region + ", " + cases_per_100k + " people have caught COVID-19, and " + deaths_per_100k + " have died."
	document.getElementById('fact-3').innerText = "In the last 7 days alone, there have been " + cases_7_days + " cases in " + region + "."
}

function update_test_facts(json) {
	const region = get_selected_region()
	const facts = json.filter(function (x) {if (x['name'] === region) {return true}})[0]

	const tests_performed = facts['cumulative_tests_performed']
	const percent_positive = facts['percent_positive_range']

	if (tests_performed === null) {
		const out = "Unfortunately, this site does not have any data on the COVID-19 tests performed in " + region + "."
		document.getElementById('fact-4').innerText = out
	} else if (tests_performed === null) {
		const out = percent_positive + " of the COVID-19 tests performed in " + region + " have come back positive."
		document.getElementById('fact-4').innerText = out
	} else {
		const out = tests_performed + " COVID-19 tests have been performed in " + region + ". " + percent_positive + " of those tests have come back positive."
		document.getElementById('fact-4').innerText = out
	}
}

document.getElementById('facts-date').innerText += " " + date_string()

const case_data = get_file('https://www.cdc.gov/covid-data-tracker/Content/CoronaViewJson_01/US_MAP_DATA.csv')
const case_data_csv = parse_csv(case_data)

const test_data = get_file('https://www.cdc.gov/covid-data-tracker/Content/CoronaViewJson_01/US_MAP_TESTING.json')
const test_data_json = JSON.parse(test_data)['US_MAP_TESTING']

// Populate the dropdown menu with all the regions provided by the case CSV
const dropdown = document.getElementById("region")
const options = case_data_csv.map(function (x) {return x[2]})
options.map(function (region) {create_dropdown_option(region, dropdown)})
