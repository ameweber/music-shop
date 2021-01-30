### Булавинова Анастасия
### 194-351
### Приложение музыкального магазина###

### Активация виртуальной среды
`source venv/bin/activate`

### Установка зависимостей
`pip install -r requirements.txt`

### Запуск приложения
`flask run`

### Приложение доступно по адресу:
`localhost:5000`

### Страницы проекта и функционал:
`1. Главная.` 
На стартовой странице проекта выводится таблица с лидерами продаж (пластинок ансамбля) года.

`2. Ансамбли. `
Выводится таблица всех существующих в базе ансамблей с их характеристиками: название, лейбл, количество произведений. 
Каждый из ансамблей можно редактировать. 
Внизу страницы предусмотрена кнопка «добавить новый ансамбль», которая ведет на форму создания.

`3.  Добавление ансамбля.` Представляет собой форму с полями: название, тип (жанр), лейбл. С этой же страницы при необходимости можно перейти на форму создания нового лейбла, если в списке нет необходимого. 

`4. Музыканты. `
Вывод всех музыкантов выбранной группы.
Форма для добавления нового участника с полями: Имя, Фамилия, Роль + функционал удаления участника.

`5. Произведения. `
Форма с добавлением нового произведения выбранного ансамбля.
Таблица с выводом всех песен выбранного ансамбля + функционал удаления произведения.

`6. Пластинки.`
Форма с добавлением новой пластинки. Поля: Продавец + добавление нового продавца (форма с вводом имени и адреса), если в списке существующего нет нужного продавца, название, лейбл, оптовая цена, розничная цена, дата выхода.
Вывод всех пластинок выбранного ансамбля.
Добавленные пластинки можно редактировать, удалить, посмотреть копии, посмотреть произведения в конкретной пластинке.

`7. Произведения в пластинке.`
Предусмотрен функционал добавления уже созданных произведений в конкретную пластинку и ее удаление из пластинки.
Вывод добавленных песен в пластинку.

`8. Копии пластинок.`
Вывод таблицы со всеми копиями пластинки с их характеристиками: уникальный ID копии, ID стикера, статус продан (или нет), дата продажи, кнопки «продать» и «удалить».
Добавлен функционал создания копии пластинки с выбором стикера из уже имеющихся или создание нового по кнопке «добавить стикер». Необходимо заполнить поле «имя» для добавления стикера.
