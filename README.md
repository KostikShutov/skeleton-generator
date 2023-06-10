# skeleton-generator

## Другие компоненты общей системы

[Raspberry server](https://github.com/KostikShutov/skeleton-server)

[Webview for server](https://github.com/KostikShutov/skeleton-webview)

## Docker

Поднять docker контейнеры

 ```bash
make d-up
 ```

Остановить docker контейнеры

```bash
make d-down
```

Перезапустить docker контейнеры

```bash
make d-restart
```

Зайти в контейнер с Python

```bash
make d-python
```

## Запуск

Поднять сервер (<http://localhost:3001>):

```bash
make generator
```

Запустить обучение нейронной сети:

```bash
make train
```

Запустить tensorboard (<http://localhost:3002>):

```bash
make tensorboard
```

Очистить папку с логами:

```bash
make clear
```

Запустить тесты:

```bash
make tests
```
