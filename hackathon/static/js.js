let map = document.getElementById('mapXY')
let map2 = document.getElementById('mapXZ')
let context = map.getContext("2d")
let context2 = map2.getContext("2d")

map.width = 500
map.height = 500
map2.width = 500
map2.height = 500

context.strokeStyle = "red"
context2.strokeStyle = "red"

let valuesXY = document.getElementById("valuesXY")
let valuesXZ = document.getElementById("valuesXZ")

let XY1 = document.createElement("div")
let XY2 = document.createElement("div")
let XY3 = document.createElement("div")

let XZ1 = document.createElement("div")
let XZ2 = document.createElement("div")
let XZ3 = document.createElement("div")

XY1.innerText = 0
XY2.innerText = 0
XY3.innerText = 0

XZ1.innerText = 0
XZ2.innerText = 0
XZ3.innerText = 0

valuesXY.appendChild(XY1)
valuesXY.appendChild(XY2)
valuesXY.appendChild(XY3)

valuesXZ.appendChild(XZ1)
valuesXZ.appendChild(XZ2)
valuesXZ.appendChild(XZ3)

const webSocket = new WebSocket('ws://'+ window.location.host +'/ws/distances/')
// const webSocket = new WebSocket('ws://localhost:1234/ws/distances/')

$("#sliderX").slider({
	animate: "fast",
	range: "min",
	max: 500,
	min: 0,
	slide: function (event, ui) {
		$("#resultX").text(ui.value)
		paint()
	}
})

$("#sliderY").slider({
	animate: "fast",
	range: "min",
	max: 500,
	min: 0,
	slide: function (event, ui) {
		$("#resultY").text(ui.value)
		paint()
	}
})

$("#sliderZ").slider({
	animate: "fast",
	range: "min",
	max: 500,
	min: 0,
	slide: function (event, ui) {
		$("#resultZ").text(ui.value)
		paint()
	}
})

$("#resultX").text($("#sliderX").slider("value"))
$("#resultY").text($("#sliderY").slider("value"))
$("#resultZ").text($("#sliderZ").slider("value"))


function paint() {

	context.clearRect(0, 0, map.width, map.height)
	context2.clearRect(0, 0, map.width, map.height)
	context.beginPath()
	context2.beginPath()
	let X = $("#sliderX").slider("value")
	let Y = $("#sliderY").slider("value")
	let Z = $("#sliderZ").slider("value")

	context.moveTo(0, 0)
	context2.moveTo(0, 0)
	context.lineTo(X, Y)
	context2.lineTo(X, Z)
	XY1.innerText = Math.round(Math.sqrt((X) ** 2 + (Y) ** 2)).toString()
	XZ1.innerText = Math.round(Math.sqrt((X) ** 2 + (Z) ** 2)).toString()

	context.moveTo(500, 0)
	context2.moveTo(500, 0)
	context.lineTo(X, Y)
	context2.lineTo(X, Z)
	XY2.innerText = Math.round(Math.sqrt((X - 500) ** 2 + (Y) ** 2)).toString()
	XZ2.innerText = Math.round(Math.sqrt((X - 500) ** 2 + (Z) ** 2)).toString()

	context.moveTo(0, 500)
	context2.moveTo(0, 500)
	context.lineTo(X, Y)
	context2.lineTo(X, Z)
	XY3.innerText = Math.round(Math.sqrt((X) ** 2 + (Y - 500) ** 2)).toString()
	XZ3.innerText = Math.round(Math.sqrt((X) ** 2 + (Z - 500) ** 2)).toString()

	context.stroke()
	context2.stroke()
	webSocket.send(JSON.stringify({
		distance: parseInt(XY1.innerText) ,
		id: 'TM1'
	}))
	// + Math.floor(Math.random() * 10) - 5
	webSocket.send(JSON.stringify({
		distance: parseInt(XY2.innerText),
		id: 'TM2'
	}))
	webSocket.send(JSON.stringify({
		distance: parseInt(XY3.innerText),
		id: 'TM3'
	}))
}

map.onmousemove = function (e){
	context.clearRect(0, 0, map.width, map.height)
	context.beginPath()

	let X = e.offsetX
	let Y = e.offsetY

	context.moveTo(0, 0)
	context.lineTo(X, Y)
	XY1.innerText = Math.round(Math.sqrt((X) ** 2 + (Y) ** 2)).toString()

	context.moveTo(500, 0)
	context2.moveTo(500, 0)
	context.lineTo(X, Y)
	XY2.innerText = Math.round(Math.sqrt((X - 500) ** 2 + (Y) ** 2)).toString()

	context.moveTo(0, 500)
	context.lineTo(X, Y)
	XY3.innerText = Math.round(Math.sqrt((X) ** 2 + (Y - 500) ** 2)).toString()

	context.stroke()
	webSocket.send(JSON.stringify({
		distance: parseInt(XY1.innerText) ,
		id: 'TM1'
	}))
	// + Math.floor(Math.random() * 10) - 5
	webSocket.send(JSON.stringify({
		distance: parseInt(XY2.innerText),
		id: 'TM2'
	}))
	webSocket.send(JSON.stringify({
		distance: parseInt(XY3.innerText),
		id: 'TM3'
	}))
}