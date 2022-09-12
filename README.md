**whsh-accounting**

Сервис наполняет таблицу t_accounting аккаунтами клиентов и изменяет баланс при получении инвойсов от whsh-billing.

В сервисе 3 метода:

`GET /top_10_accounts` - Делает выборку первых 10 строк из t_accounts. Без параметров. Можно быстро проверить наличие записей в таблице.

`POST /check_balance` - Вернет аккаунт по id_account. Аргументы в url (`/check_balance/?id_account=1`).

`POST /create_account` - Добавляет запись в таблицу `t_accounts`. В body передается тело записи, которая будет добавляться в таблицу `t_accounts`

`POST /update_balance` -
На вход получает json от whsh-billing и по полученному id_account 
обновить баланс в t_accounts из operation. whsh-billing передает параметры через body запроса.

**Запуск:**

Сервис запускается из склонированной директории через `docker-compose up`.
При запуске сервис создает свою БД `postgresql` с таблицей `t_accounts`.
После запуска можно проверить работоспособность сервиса http тестами из папки tests/http,
через http://localhost:8009/docs
или curl-ом к какому-нибудь из методов:

`curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
  "name": "Vasya",
  "balance": 100
}' \
 http://localhost:8009/create_account`

Также можно использовать тесты из test_accounting для проверки основного функционала.
В текущей версии в test_accounting используется БД sqlite, которая создается для тестов. 
