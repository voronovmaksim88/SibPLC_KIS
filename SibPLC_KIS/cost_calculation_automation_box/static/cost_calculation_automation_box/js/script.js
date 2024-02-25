var isRowAdded = false;

function addOrRemoveRow(equipment_id, price_date, height, width, depth, material, ip) {
    var table = document.getElementById("TableEquipment");
    var row = document.getElementById('tr_'+equipment_id);
    var newIndex = row.rowIndex + 1;
    var isRowAdded = row.dataset.isRowAdded === 'true';
    if (isRowAdded) {
        table.deleteRow(newIndex);
        row.dataset.isRowAdded = 'false';
    } else {
        var newRow = table.insertRow(newIndex);
        var cell1 = newRow.insertCell(0);
        cell1.colSpan = "8";
        cell1.innerHTML = `
                        <p>Дата стоимости: <b> ${price_date}</b></p>
                        <p>В х Ш х Г: <b> ${height} х ${width} х ${depth}</b></p>
                        <p>Материал: <b> ${material}</b> </p>
                        <p>Степень защиты: <b> ${ip}</b> </p>
                        `;
        row.dataset.isRowAdded = 'true';
    }
    console.log('пытаемся развернуть данные строки ', price_date);


    var myButtonClass = document.getElementById('btn_'+equipment_id).className;
    // Если текущий класс кнопки 'btn btn-primary', меняем его на 'btn btn-secondary'
    // Если текущий класс кнопки не 'btn btn-primary', меняем его на 'btn btn-primary'
    if (myButtonClass === 'btn btn-primary') {
        document.getElementById('btn_'+equipment_id).className = 'btn btn-secondary';
    } else {
        document.getElementById('btn_'+equipment_id).className = 'btn btn-primary';
    }
}


;