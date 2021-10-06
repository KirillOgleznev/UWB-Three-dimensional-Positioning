let mapXY = document.getElementById('mapXY')
let mapXZ = document.getElementById('mapXZ')
let contextXY = mapXY.getContext("2d")
let contextXZ = mapXZ.getContext("2d")
let height = document.getElementById('height')
let heightCTX = height.getContext("2d")
let heightValue = document.getElementById('heightValue')

let img1 = document.getElementById('img1')
let img2 = document.getElementById('img2')

mapXY.width = 500
mapXY.height = 500
mapXZ.width = 500
mapXZ.height = 500
height.width = 20
height.height = 500


let coordXY = document.getElementById('coordXY')
let coordXZ = document.getElementById('coordXZ')

const webSocket = new WebSocket('ws://' + window.location.host + '/ws/distances/')

// webSocket.onopen = function (e) {
//     webSocket.send(JSON.stringify({id: 'start'}))
// }

let img = new Image()

webSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)

    if (data.X === -1) {
        console.log(123)
        img1.src = img1.src + '?' + Math.random()
        img2.src = img2.src + '?' + Math.random()
        document.getElementById('hidden').setAttribute('style', 'visibility: uset')
        return
    }

    heightCTX.clearRect(0, 0, height.width, height.height)
    contextXY.clearRect(0, 0, mapXY.width, mapXY.height)

    contextXZ.clearRect(0, 0, mapXY.width, mapXY.height)

    heightCTX.beginPath()
    contextXY.beginPath()
    contextXZ.beginPath()

    heightCTX.fillStyle = "red"
    heightCTX.fillRect(0, 0, 50, data.Z)

    contextXY.drawImage(img, 0, 0)
    contextXY.fillRect(data.X, data.Y, 1, 1)
    img.src = mapXY.toDataURL()

    contextXY.arc(data.X, data.Y, 5, 0, 2 * Math.PI)
    contextXY.fill()
    contextXY.fillStyle = "red"

    contextXZ.arc(data.X, data.Z, 5, 0, 2 * Math.PI)
    contextXZ.fill()
    contextXZ.fillStyle = "red"

    heightCTX.stroke()
    contextXY.stroke()
    contextXZ.stroke()

    heightValue.innerHTML = data.Z + 'px'
    coordXY.innerHTML = '<div class="msg">X: ' + data.X + '</div>' + '<div class="msg">Y: ' + data.Y + '</div>'
}

let timer = NaN

function start_stop(text) {
    webSocket.send(JSON.stringify({id: text}))
    if (text === 'start') {
        let btn = document.getElementById('btnStart')
        btn.id = 'btnStop'
        btn.innerText = 'Стоп'
        btn.setAttribute('onclick', 'start_stop(\'stop\')')
        timer = Date.now()
    } else {
        let btn = document.getElementById('btnStop')
        btn.id = 'btnStart'
        btn.innerText = 'Старт'
        btn.setAttribute('onclick', 'start_stop(\'start\')')
    }


    heightCTX.clearRect(0, 0, height.width, height.height)
    contextXY.clearRect(0, 0, mapXY.width, mapXY.height)
    contextXZ.clearRect(0, 0, mapXY.width, mapXY.height)
    img = new Image()
}

