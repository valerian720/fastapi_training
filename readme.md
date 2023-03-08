# API для заметок

данный api создан на основе fastapi и собирается и деплоится как контейнер


разрабатывается для ознакомления с возможностями fastapi и структурой микросервисов

## особенности которые меня порадовали
- интерактивная документация через /docs
  - дополнительно выводится структура ошибки
  - enum в качестве параметра выводится в виде выпадающего списка
  - если эндпоинт защищен паролем то есть пайплайн что бы автоматом получать jwt и отправлять его вместе с запросом чисто через логин и пароль
- документация через /redoc
- автопроверка на типы и вывод сообщения об ошибке
- существует пайплайн что бы добавить авторизацию и аунтетефикацию с нуля

## доп особенности
- при изменении структур таблиц sqlalchemy их надо удалять и заново создавать (наверное я пока что не понял как создавать и работать с миграциями)
## используемые бизнес объекты
- 