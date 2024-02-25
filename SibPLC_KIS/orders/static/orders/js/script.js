window.data_order = 0; // Это глобальная переменная  в которой будем хранить всю таблицу с заказами
window.show_completed_orders = false;

function receive_order_JSON() {
  //alert("УРА!!!"); // всплывающее окно
  fetch("/get-orders-as-json/")
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Делайте с данными что нужно, например, отобразите в таблице
      console.log("data.length", data.length);
      window.data_order = data;
      sort_table_orders_by_serial("down")

// вывод полученных данных тупо на страницу
//      for (var i = 0; i < data.length; i++) {
//      console.log("id", data[i].id, "   serial", data[i].serial, "   priority", data[i].priority);
//      document.write("id ", data[i].id, "   serial ", data[i].serial, "   priority ", data[i].priority, "</br>");
//      }

      // передаём данные в глобальную переменную

      //document.write(window.data_order.length);
    })
    .catch((error) => console.error("Ошибка:", error));
}

function clear_table_orders() {
    // alert("ща почистим талицу !")
    var table = document.getElementById("TableOrder");
    for (var i = table.rows.length - 1; i > 1; i--) {
        table.deleteRow(i);
    }
}

function print_table_orders(show_completed_orders) {
var table = document.getElementById("TableOrder");
    for (var i = 0; i < window.data_order.length; i++) {
        if (!(show_completed_orders===false &&
            (window.data_order[i].status===4 ||
            window.data_order[i].status===5 ||
            window.data_order[i].status===6))
        ) {
            var row = table.insertRow();

            // Создаем ячейки в новой строке
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);

            // Устанавливаем содержимое ячеек
            if (window.data_order[i].status===0 ||
                window.data_order[i].status===1 ||
                window.data_order[i].status===2 ||
                window.data_order[i].status===3 ||
                window.data_order[i].status===7) {
                cell1.innerHTML = "<b>" + window.data_order[i].serial + "</b>";
            } // жирным подсвечиваем те заказы которые не отменены или не завершены
            else {cell1.innerHTML = window.data_order[i].serial;}


            cell2.innerHTML = window.data_order[i].customer_id;
            cell3.innerHTML = window.data_order[i].priority;
            cell4.innerHTML = window.data_order[i].name;

            if      (window.data_order[i].status===0) {
                cell5.innerHTML = "Не определён";
            }
            else if (window.data_order[i].status===1) {
                cell5.innerHTML ="<b>" + "На согласовании" + "</b>";
                cell5.style.color = "blue"
                row.classList.add("table-secondary");
            }
            else if (window.data_order[i].status===2) {
                cell5.innerHTML ="<b>" + "В работе" + "</b>";
                cell5.style.color = "green"
                row.classList.add("table-success");
            }
            else if (window.data_order[i].status===3) {
                cell5.innerHTML = "Просрочено";
                row.classList.add("table-danger");
            }
            else if (window.data_order[i].status===4) {
                cell5.innerHTML = "Выполнено в срок";
                row.classList.add("table-primary");
            }
            else if (window.data_order[i].status===5) {
                cell5.innerHTML = "Выполнено НЕ в срок";
                row.classList.add("table-warning");
            }
            else if (window.data_order[i].status===6) {
                cell5.innerHTML = "Не согласовано";
                row.classList.add("table-dark");
            }
            else if (window.data_order[i].status===7) {
                cell5.innerHTML = "На паузе";
                row.classList.add("table-info");
            }
            else { cell5.innerHTML = "?"; }
        }
    }
}

function comparePriorityUp(a, b) {
  // Извлекаем год и порядковый номер из серийного номера (формат: NNN-MM-YYYY)
  const yearA = a.serial.slice(7, 11);
  const yearB = b.serial.slice(7, 11);
  const orderNumA = a.serial.slice(0, 3);
  const orderNumB = b.serial.slice(0, 3);
  const PriorityA = a.priority;
  const PriorityB = b.priority;

  // Сравниваем годы
  if (PriorityA !== PriorityB) { // Если приоритет
    return PriorityA - PriorityB;
  }
  else if (yearA !== yearB){ // Если приоритеты одинаковые, сравниваем года
    return yearA - yearB;
  }
  else{
   return orderNumA - orderNumB; // Если года одинаковые, сравниваем номера
  }
}


function comparePriorityDown(a, b) {
  // Извлекаем год и порядковый номер из серийного номера (формат: NNN-MM-YYYY)
  const yearA = a.serial.slice(7, 11);
  const yearB = b.serial.slice(7, 11);
  const orderNumA = a.serial.slice(0, 3);
  const orderNumB = b.serial.slice(0, 3);
  const PriorityA = a.priority;
  const PriorityB = b.priority;

  // Сравниваем годы
  if (PriorityA !== PriorityB) { // Если приоритет
    return PriorityB - PriorityA;
  }
  else if (yearA !== yearB){ // Если приоритеты одинаковые, сравниваем года
    return yearA - yearB;
  }
  else{
   return orderNumA - orderNumB; // Если года одинаковые, сравниваем номера
  }
}




function compareSerialNumbersUp(a, b) {
  // Извлекаем год и порядковый номер из серийного номера (формат: NNN-MM-YYYY)
  const yearA = a.serial.slice(7, 11);
  const yearB = b.serial.slice(7, 11);
  const orderNumA = a.serial.slice(0, 3);
  const orderNumB = b.serial.slice(0, 3);

  // Сравниваем годы
  if (yearA !== yearB) {
    return yearA - yearB;
  }
  // Если годы одинаковые, сравниваем порядковые номера
  return orderNumA - orderNumB;
}


function compareSerialNumbersDown(a, b) {
  // Извлекаем год и порядковый номер из серийного номера (формат: NNN-MM-YYYY)
  const yearA = a.serial.slice(7, 11);
  const yearB = b.serial.slice(7, 11);
  const orderNumA = a.serial.slice(0, 3);
  const orderNumB = b.serial.slice(0, 3);

  // Сравниваем годы
  if (yearA !== yearB) {
    return yearB - yearA;
  }
  // Если годы одинаковые, сравниваем порядковые номера
  return orderNumB - orderNumA;
}

function sort_table_orders_by_serial(direction){
    clear_table_orders()
    if (direction==="up"){
//        window.data_order.sort((a, b) => a.serial.slice(7, 11).localeCompare(b.serial.slice(7, 11)));
        window.data_order.sort(compareSerialNumbersUp);
    }
    if (direction==="down"){
//        window.data_order.sort((a, b) => b.serial.slice(7, 11).localeCompare(a.serial.slice(7, 11)));
        window.data_order.sort(compareSerialNumbersDown);
    }
    console.log("сортируем!")
    print_table_orders(window.show_completed_orders)
}



function sort_table_orders_by_priority(direction){
    clear_table_orders()
    if (direction==="up"){
//        window.data_order.sort(function (a, b) {
//            return a.priority - b.priority;
//        });
        window.data_order.sort(comparePriorityUp);
    };
    if (direction==="down"){
//        window.data_order.sort(function (b, a) {
//            return a.priority - b.priority;
//        });
        window.data_order.sort(comparePriorityDown);
    };
    print_table_orders(window.show_completed_orders);
}

document.addEventListener('DOMContentLoaded', (event) => {
    var checkbox = document.getElementById('flexSwitchCheckChecked');

    checkbox.addEventListener('change', function() {
        if(this.checked) {
            // Чекбокс включен
            console.log('Завершенные: включено');
            window.show_completed_orders=true;
            console.log(show_completed_orders);
        } else {
            // Чекбокс выключен
            console.log('Завершенные: выключено');
            window.show_completed_orders=false;
            console.log(show_completed_orders);
        }
        clear_table_orders();
        print_table_orders(window.show_completed_orders);
    });
});