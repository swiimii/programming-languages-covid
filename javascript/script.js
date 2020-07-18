'use strict'

function date_string() {
	const today = new Date()
	return today.toDateString()
}

document.getElementById('facts-date').innerText += " " + date_string()
