const div_popup = document.createElement('div');
div_popup.id = "popup"
div_popup.innerHTML =
    '    <div id="modal">' +
    '          <input type="hidden" name="csrfmiddlewaretoken" value="' + window.CSRF_TOKEN + '">' +
    '        <p>' +
    '            <label>Введите имя</label><br>' +
    '            <input type="text" name="name" id="name"/>' +
    '        </p>' +
    '        <p>' +
    '            <label>Введите возраст</label><br>' +
    '            <input type="number" name="age" id="age"/>' +
    '        </p>' +
    '        <input class="btn" type="button" value="Сохранить" onclick="submit(\'create/\')">' +
    '    </div>'

div_popup.onclick = function (e) {
    if (e.target.id === "popup")
        document.body.removeChild(div_popup)
}

function popup() {
    document.body.appendChild(div_popup)
}

function submit(url) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            "csrfmiddlewaretoken": window.CSRF_TOKEN,
            name: document.getElementById('name').value,
            age: document.getElementById('age').value
        },
        success: function (data) {
            if(url === 'create/')
                append(data)
            else
                edit_table(data, parseInt(url.substr(5)))
        },
        error: function (err) {
            console.log('err')
        },
        complete: function () {
        }
    });
}

function edit_table(data, id){
    document.getElementById('popup').remove()

    const tr = document.getElementById('person-' + id)
    tr.innerHTML = ''
    let td = document.createElement('td')
    td.innerText = data.id
    tr.appendChild(td)
    td = document.createElement('td')
    td.innerHTML = '<td><a href="' + data.id + '" class="name_ref">' + data.name + '</a></td>\n'
    tr.appendChild(td)
    td = document.createElement('td')
    td.innerText = data.age
    tr.appendChild(td)
    td = document.createElement('td')
    td.innerHTML =
        '<div class="btn_ref" onclick="edit(' + data.id + ')">Изменить</div>\n' +
        '<div class="btn_ref" onclick="del(' + data.id + ')">Удалить</div>'
    tr.appendChild(td)
}

function append(data) {
    document.body.removeChild(div_popup)
    const table_price = document.getElementById('table_price')
    const tr = document.createElement('tr');
    tr.id = "person-" + data.id
    let td = document.createElement('td')
    td.innerText = data.id
    tr.appendChild(td)
    td = document.createElement('td')
    td.innerHTML = '<td><a href="' + data.id + '" class="name_ref">' + data.name + '</a></td>\n'
    tr.appendChild(td)
    td = document.createElement('td')
    td.innerText = data.age
    tr.appendChild(td)
    td = document.createElement('td')
    td.innerHTML =
        '<div class="btn_ref" onclick="edit(' + data.id + ')">Изменить</div>\n' +
        '<div class="btn_ref" onclick="del(' + data.id + ')">Удалить</div>'
    tr.appendChild(td)
    table_price.appendChild(tr)
}

function del(id) {
    $.ajax({
        type: "DELETE",
        url: "delete/" + id,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
        },
        success: function (msg) {
            document.getElementById('person-' + id).remove()
        },
        error: function (err) {
            console.log('err')
        },
    });
}

function edit(id) {
    const div_edit = document.createElement('div');
    div_edit.id = "popup"
    div_edit.innerHTML =
        '    <div id="modal">' +
        '          <input type="hidden" name="csrfmiddlewaretoken" value="' + window.CSRF_TOKEN + '">' +
        '        <p>' +
        '            <label>Введите имя</label><br>' +
        '            <input type="text" name="name" id="name"/>' +
        '        </p>' +
        '        <p>' +
        '            <label>Введите возраст</label><br>' +
        '            <input type="number" name="age" id="age"/>' +
        '        </p>' +
        '        <input class="btn" type="button" value="Сохранить" onclick="submit(\'edit/' + id + '/\')">' +
        '    </div>'
    div_edit.onclick = function (e) {
        if (e.target.id === "popup")
            document.body.removeChild(div_edit)
    }
    document.body.appendChild(div_edit)
}