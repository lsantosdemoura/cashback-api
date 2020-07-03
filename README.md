# Cashback API
API for creating, reading, updating and deleting resellers and their purchases and check their cashback

---
## REQUIREMENTS
- [docker-compose](https://docs.docker.com/compose/install/)
- [docker](https://docs.docker.com/engine/install/)
- python3.8+
---

## USAGE
### Run the project
```
$ git clone https://github.com/lsantosdemoura/cashback-api
$ cd cashback-api
# You can build and start docker at once
$ make runserver
```
#### You can access all images' bashes:
- The project itself: ``` $ docker-compose exec web bash ```
- Postgres:  ``` $ docker-compose exec db bash ```

### Run tests
```
$ cd cashback-api
$ make run-tests
```

## Endpoints


### /resellers/
  - create resellers
  - POST
  - payload:
  ```javascript
  {
      "email": "string",
      "fullname": "string",
      "cpf": "string",
      "password": "string"
  }
  ```
  - response:
  ```javascript
  {
      "email": "string",
      "fullname": "string",
      "cpf": "string"
  }
  ```

### /login/
  - Returns a refresh and an access token that will be used as authentication in other endpoints
  - POST
  - payload:
  ```javascript
  {
      "email": "string",
      "password": "string"
  }
  ```
  - response:
  ```javascript
  {
      "refresh": "string",
      "access": "string"
  }
  ```

### /refresh-token/
  - Returns a new access token
  - POST
  - payload:
  ```javascript
  {
      "refresh": "string"
  }
  ```
  - response:
  ```javascript
  {
      "access": "string"
  }
  ```

### /purchases/
  - Creates a new purchase for the given reseller, it creates only if it is authenticated, it also can have start_date and end_date query parameters for a range of date in response
  - GET
  - query parameters [optional]:
  ```
  start_date: "%Y-%m-%d"
  end_date: "%Y-%m-%d"
  ```
  - headers:
  ```javascript
  {
      "Authorization": "Bearer <access token>"
  }
  ```
  - payload:
  ```javascript
  {
      "code": "string",
      "value": "float",
      "date": "string",
      "reseller": "string"
  }
  ```
  - response:
  ```javascript
  {
      "count": "integer",
      "next": "integer",
      "previous": "integer",
      "results": [
          {
              "code": "string",
              "value": "string",
              "date": "string",
              "reseller": "string",
              "status": "string",
              "cashback_percentage": "string",
              "cashback_value": "string"
          }
      ]
 }
  ```

### /gathered-cashback/
  - Returns the reseller's already gahered cashback
  - GET
  - headers:
  ```javascript
  {
      "Authorization": "Bearer <access token>"
  }
  ```
  - response:
  ```javascript
  {
    "credit": "integer"
  }
  ```
