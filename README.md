# Translation-CDDA-Project

Проект по переводу различных модов по игре CDDA.
В пакет входит:
* Программа для извлечения, конвертации и перезаписи строк
* Переведенные моды

Версия v.0.1
* Извлечение строк по тэгам:
   - names -  название
   - description - описание
   - job_descriptions - фразы NPC на вопрос, что они делают.
   - start name - обобщенное название локаций при генерации персонажа 
   - sounds - звуки. Включает в себя также звуки при взаимодействии
   - messages - обширная группа сообщений. Постепенно добавляються новые значения.
   - attacks - сообщения при атаке объекта или нападении на игрока. %s - целевой объект. %1$s - имя атакующего, %2$s - целевой объект атаки %1$s.

* Конвертация строк в формат json для дальнейшей замены

Инструкция v.0.1
1) Разархивировать проект в любой папке.
2) Select mod - выбрать мод из папки. 
3) Extract functions - извлечение строк по тэгам и запись их в папке strings. В папке user создаются файлы словарей.
4) Перевод осуществляется в документах формата .txt  в папке Translation-CDDA-Project/strings
5) Update strings - функция, проверяющая соответствие файлов в папке user c файлами модов. В случае отсутствия строк в файлах user, они будут добавляться. Также строки из файлов strings записываются в файл user (В ближайших обновлениях будет добавлено диалоговое окно, где можно будет выбрать, требуется ли синхронизировать strings и user перед апдейтом. Сейчас синхронизация идет по дефолту)
6) Rewrite json - создает в папке translated файлы json на основе оригинальных файлов и файлов словарей.

Часто появляющиеся ошибки:

Errno1 - file. Недостающие строки - обычно возникает, когда добавляются новые теги для записи. Количество строк в файле txt меньше чем в словаре. Решается через обновление строк (Update strings).

Errno2 - отсутствует файл construction_group.json в папке с модом - может возникать при обновлении мода, когда автор решил убрать файл. Не влияет на работоспособность перевода

Errno3 - missing key. Key {item} doesn't exist in user {file} - в файле нет соответсвующих ключу значений. Для решения проблемы стоит сначала обновить строки (Update strings).
