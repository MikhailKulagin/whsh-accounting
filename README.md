**whsh-billing**

В сервисе 3 метода:

`GET /top_10_accounts` - без параметров. Делает выборку первых 10 строк из t_accounts

`POST /check_balance` - аргументы в url (`/check_balance/?id_account=1`). Вернет аккаунт по id_account.  

`POST /create_account` - с body. Добавляет запись в таблицу `t_account`

`POST /update_balance` - с body.  
На вход получает json от whsh-billing, чтобы по полученному id_account 
обновить баланс в t_accounts из operation.

**Запуск:**

Сервис запускается из склонированной директории через `docker-compose up`.
При запуске сервис создает свою БД postgresql с таблицей `t_accounts`.
После запуска можно проверить работоспособность http тестами из папки tests/http,
через http://localhost:8009/docs
или curl-ом:

`curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
  "name": "Vasya",
  "balance": 100
}' \
 http://localhost:8009/create_account`

Также можно использовать тесты из test_accounting для проверки основного функционала.
В текущей версии в test_accounting используется БД sqlite, которая создается для тестов. 
