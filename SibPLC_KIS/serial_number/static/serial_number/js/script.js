window.data_box = 0; // Это глобальная переменная  в которой будем хранить всю таблицу учёта шкафов

document.addEventListener('DOMContentLoaded', function() {
  // Поиск элемента по ID
  var inputElement = document.getElementById('filter-name');

  // Добавление слушателя событий на изменение поля
  inputElement.addEventListener('input', function() {
    // Вывод сообщения в консоль браузера
    console.log('Значение поля изменилось на: ' + this.value);
  });
});

