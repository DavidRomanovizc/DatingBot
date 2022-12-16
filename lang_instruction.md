## Title - dating

### Launching for the first time

1. We pull the texts out of the files (he finds it himself)
   `pybabel extract . -o locales/dating.pot`
2. Creating a folder for translation into English
   `pybabel init -i locales/dating.pot -d locales -D dating -l en`
3. Into Russian
   `pybabel init -i locales/dating.pot -d locales -D dating -l ru`
4. We translate, and then collect the translations
   `pybabel compile -d locales -D dating`

### Обновляем переводы

1. We pull the texts out of the files, Add the text to the translated versions
   `pybabel extract . -o locales/dating.pot`
   `pybabel update -d locales -D dating -i locales/dating.pot`
2. Manually make transfers, and then collect
   `pybabel compile -d locales -D dating`

## Название - dating

### Запускаем первый раз

1. Вытаскиваем тексты из файлов (он сам находит)
   `pybabel extract . -o locales/dating.pot`
2. Создаем папку для перевода на английский
   `pybabel init -i locales/dating.pot -d locales -D dating -l en`
3. То же, на русский
   `pybabel init -i locales/dating.pot -d locales -D dating -l ru`
5. Переводим, а потом собираем переводы
   `pybabel compile -d locales -D dating`

### Обновляем переводы

1. Вытаскиваем тексты из файлов, Добавляем текст в переведенные версии
   `pybabel extract . -o locales/dating.pot`
   `pybabel update -d locales -D dating -i locales/dating.pot`
2. Вручную делаем переводы, а потом Собираем
   `pybabel compile -d locales -D dating`