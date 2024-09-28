Инструкция:
1. Подготовка
	1.1. Установка pyenv [Рекомендуется]:
		https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#installation
		
		Winddows: 
			Выполнить в PowerShell
				pip install pyenv-win --target %USERPROFILE%\\.pyenv
				
				Если ошибка "... .ps1 cannot be loaded because running scripts is 
		disabled on this system. ..." выполнить
				Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
				
			Установить Path EvarementVariables
			C:\Users\<replace with your actual username>\.pyenv\pyenv-win\bin
			C:\Users\<replace with your actual username>\.pyenv\pyenv-win\shims
			
	1.2. Установка python:
		Для Pyenv:
			Windows:
				Выполнить в PowerShell
				pyenv install 3.7.4
				pyenv global 3.7.4
	1.3. Установка Pandas 
		Windows:
			Выполнить в PowerShell
			pip install pandas
	1.4. Установка
		Windows:
			Выполнить в PowerShell
			pip install openpyxl
	1.5. Проверка 
		pyenv version

2. Проверка
	pyenv version
	вывод: 3.7.4 (set by C:\Users\<user-name>\.pyenv\pyenv-win\version)
	
3. Запуск
	3.1 Настроить "...\Configuration\Config.json" (см. раздел "Настройка Config.json").
	3.2 Положить excel-файл в путь указанные в Config.json (поле "excelFilePath")
	3.3 Переключиться в папку с проектом через PowerShell
		Windows:
			Выполнить в PowerShell
			cd "<вставить путь до скрипта>\ExcelToJsonParser\ExcelToJsonParcer\"
	3.4 Запустить main.py
		Windows:
			Выполнить в PowerShell
			 python .\main.py
		Если всё прошло успешно, то будет выведено "Done!"
	3.5 Результат находится по пути, указанному в Config.json для каждой фичи отдельно ("parsingFeatures"-> "outputDirectory"/"outputFileName")


Настройка Config.json
	В Config.json находятся параметры, на основе которых осуществляется парсинг excel-документа.
	Что необходимо настроить:
		"excelFilePath" - это путь где искать Excel-файл, который будет парситься.
		"parsingFeatures" - это список фичей, который нужно спарсить из excel-файла.
			Фичи можно укзаывать не все (лишние скрипт проигнорирует)
			
			Для каждой фичи нужно настроить:
				"excelSheetName" - название страницы в excel-файле
				"featureName" - название фичи (должно совпадать с именем в колонках excel-файле).
				"outputDirectory" - это путь куда будет сохранён итоговый json-файл.
				"outputFileName" - имя файла итогового json-файл
				
	FAQ:
	1. Для "outputDirectory" можно использовать относительный путь, чтобы сразу разместить файл там где нужно ("../../TargetPath")
	2. Название фичией featureName не должно повторятся
	3. Фичи можно размещать на разных страницах excel-документа (главное правильно указать "excelSheetName")
	4. В Config.json можно переопределить откуда скрипт будет брать значения (поле "parsingExcel").
		Поле "fieldsSeparator" описывает каким знаком будут разделены уровни в excel-файлеы
		
Правила заполнения Excel-файла для парсинга
	Для того чтобы скрипт успешно выполнил свою работу необходимо корректно заполнить excel документ со всеми правилами и ограничениями. 
	
	Json-файл можно представить в виде дерева. На каждом уровне вложенности L могут быть любые поля
	Layer0	Layer1			Layer2
					-	sub_field0 : 1
			field0	-	sub_field1 : 2
					-	sub_field2 : 15
					
						sub_field0 : 20
	json - 	field1	-	sub_field1 : text1
						sub_field2 : text2
						
			field2	:	"value"
			
	Для преобразования excel-файла в json необходимо перебрать все такие ветви деревьев, где в конечном итоге будет получен полный путь с учётом вложенности и значением. 
	
	json-field0-sub_field0: 0
	json-field0-sub_field1: 1
	...
	json-field1-sub_field2: text2
	...
	json-field3 : value
	
	В результате такой путь поля и значения можно представить в виде таблицы.
	
	Json имеет 3 типа значений
	1. Поле со значением
	2. Объект
	3. Массив
	
	Тип "Поле со значением"
		Представляет из себя строку где ключу соответствует определённое значение <key>:<value>
		
		Для парсинга сущетсвует 3 типа значений
			1. "$str" - строка. 
				Значение представлено в виде текста и в файле json оборачивается в кавычки
			2. "$num" - число.
				Значение представлено в виде числа (целого или дробного), записывается без кавычек
			3. "$null" - null значение, т.е. отсутствие значения в поле
		
		Эти три типа операции являются конечными узлами в дереве json.
		В Excel запись должны выглядеть следующим образом:
		  <root_field_names> | sub_field_name | value
		feauture_name-field0 |		$str	  | 0
		feauture_name-field1 |		$num	  | 123
		feauture_name-field2 |		$null	  |

			Приведённый пример будет преобразован в:
			{
				"field0": "0"
				"field1": 123
				"field2": null
			}
			
		feauture_name - является самым верхним уровнем. На основе этого значения происходит группировка строк.
				
		Поля со значением могут быть частью объектов и массивов.
		
	Тип "Объект"
		Представляет из себя список полей, обёрнутых фигурными скобочками.
		Ниже представлен пример, где поле "fieldX" является объектом
		Пример:
		{
			"fieldX" : 
			{
				"field0": "0"
				"field1": 123
				"field2": null
			}
		}
		
		Парсинг осуществляется по уровням. Каждый вложенный элемент - это новый уровень.
		Уровни с объектами необходимо помечать разделителями "$ld" (сокращение от layer delimiter). 
		В качестве value для значения "$ld" подставляется открывающаяся фигурная скобочка "{"
		
		При переходе от уровня к уровню необходимо сначала описать что находиться на данном уровне, а только потом подставлять значения. 
		Пример выше в виде подготовленных данных для парсинга в excel
				 <root_field_names> | sub_field_name | value
					  feauture_name |	  $ld   	 | {
					  feauture_name |	  fieldX 	 |
					
			   feauture_name-fieldX |	  $ld   	 | {
			   feauture_name-fieldX |	 field0 	 |
			   feauture_name-fieldX |	 field1 	 |
			   feauture_name-fieldX |	 field2 	 |
		
		feauture_name-fieldX-field0 | 	  $str  	 | 0
		feauture_name-fieldX-field1 | 	  $num  	 | 123
		feauture_name-fieldX-field2 | 	  $null 	 |
		
	Тип "Массив"
		Представляет из себя список объектов или полей со значением.
		Как и объект требует разметки для уровня "$ld". 
		В качестве value для значения "$ld" подставляется прямоугольная скобочка "["
		
		Массив задаётся в три уровня.
		- На первом уровне необходимо указать разделитель уровня и специальный оператор массива "$arr".
		- На втором уровне необходимо описать id элементов массива
		- На третьем уровне описывается сами элементы массива.
		
		Пример json с массивом, где элементы являются объектами
		{
			"fieldY":
			[
				{
					"field0": "a0"
					"field1": "a1"
				},
				{
					"field0": "b0"
					"field1": "b1"
				}
			]
		}
		
		Пример выше в виде подготовленных данных для парсинга в excel
							<root_field_names>| sub_field_name | value
								 feauture_name|		 $ld	   | {
								 feauture_name|		 fieldY    |

						  feauture_name-fieldY|		 $ld	   | [
						  feauture_name-fieldY|		 $arr	   |

					 feauture_name-fieldY-$arr|			0	   |
					 feauture_name-fieldY-$arr|			1	   |

				   feauture_name-fieldY-$arr-0|		 $ld	   | {
				   feauture_name-fieldY-$arr-0|		 field0    |
				   feauture_name-fieldY-$arr-0|		 field1    |
				   
				   feauture_name-fieldY-$arr-1|		 $ld	   | {
				   feauture_name-fieldY-$arr-1|		 field0    |
				   feauture_name-fieldY-$arr-1|		 field1    |

			feauture_name-fieldY-$arr-0-field0|		 $str	   | a0
			feauture_name-fieldY-$arr-0-field1|		 $str	   | a1

			feauture_name-fieldY-$arr-1-field0|		 $str	   | b0
			feauture_name-fieldY-$arr-1-field1|		 $str	   | b1
			
	
	В папке Example находиться excel-документ "Doc.xlsx" с демонстрацией настройки.
	В excel-файле заполнен данные для 3-х фич:
		- feauture_name (описываемый пример)
		- season
		- season1
	В \Configuration\Config.json указан список какие из этих фичей парсить и куда положить json-файл. По умолчанию файлы появятся рядом с Doc.xlsx в папке Temp.
	По умолчанию фича season1 игнорируется для парсинга
	
Рекомендации по использованию
	1. Формирование полей в excel стоит сделать автоматизированного через Concatinate()/Join().
		Это позволит легко менять названия и пере привязывать цепочки
	2. Если фича большая, а нужно проверить правильность её вывода, то можно экранировать
		несколько полей, добавив любой допонительный символ к первому уровню этого поля (поле не попадёт в ветвь дерева)
	3. Для заполнения excel можно пользоваться фильтрами или сворачивать лишние строки в "+".
	4. Фичи можно располагать на разных листах excel-файла




