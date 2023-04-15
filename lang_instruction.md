## Title - dating

### Launching for the first time

1. We pull the texts out of the files (he finds it himself)
   ```sh
   $ pybabel extract . -o locales/dating.pot
   ```
2. Creating a folder for translation into English
   ```sh
   $ pybabel init -i locales/dating.pot -d locales -D dating -l en
   ```
3. Into Russian
   ```sh
   $ pybabel init -i locales/dating.pot -d locales -D dating -l ru
   ```
4. We translate, and then collect the translations
   ```sh
   $ pybabel compile -d locales -D dating
   ```

### Updating translations

1. We pull the texts out of the files, Add the text to the translated versions
   ```sh
   $ pybabel extract . -o locales/dating.pot
   $ pybabel update -d locales -D dating -i locales/dating.pot
   ```
2. Manually make transfers, and then collect
   ```sh
   $ pybabel compile -d locales -D dating
   ```

## Название - dating

### Запускаем первый раз

1. Вытаскиваем тексты из файлов (он сам находит)
   ```sh
   $ pybabel extract . -o locales/dating.pot
   ```
2. Создаем папку для перевода на английский
   ```sh
   $ pybabel init -i locales/dating.pot -d locales -D dating -l en
   ```
3. То же, на русский
   ```sh
   $ pybabel init -i locales/dating.pot -d locales -D dating -l ru
   ```
4. Переводим, а потом собираем переводы
   ```sh
   pybabel compile -d locales -D dating
   ```

### Обновляем переводы

1. Вытаскиваем тексты из файлов, Добавляем текст в переведенные версии
   ```sh
   $ pybabel extract . -o locales/dating.pot
   $ pybabel update -d locales -D dating -i locales/dating.pot
   ```
2. Вручную делаем переводы, а потом собираем
   ```sh
   $ pybabel compile -d locales -D dating
   ```

## Titel - Dating

### Erster Start

1. Extrahieren Sie Texte aus Dateien (er findet sie automatisch)

```sh
$ pybabel extract . -o locales/dating.pot
```

2. Erstellen Sie einen Ordner für die Übersetzung ins Englische

```sh
$ pybabel init -i locales/dating.pot -d locales -D dating -l en
```

3. Dasselbe für Russisch

```sh
$ pybabel init -i locales/dating.pot -d locales -D dating -l ru
```

4. Übersetzen und dann Übersetzungen sammeln

```sh
pybabel compile -d locales -D dating
```

### Aktualisierung der Übersetzungen

1. Extrahieren Sie Texte aus Dateien, fügen Sie den Text zu den übersetzten Versionen hinzu

```sh
$ pybabel extract . -o locales/dating.pot
$ pybabel update -d locales -D dating -i locales/dating.pot
```

2. Manuell übersetzen und dann sammeln

```sh
$ pybabel compile -d locales -D dating
```


