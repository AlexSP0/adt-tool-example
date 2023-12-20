# Описание задачи 
Нам необходимо сделать набор из трех тестов для ADT:
- Один исполняемый файл, принимающий на вход имя теста и запускающий его
- При запуске с параметром --l- или --list- выводится список возможных тестов
- В каждом тесте в стандартном выводится строка с номером теста
- Добавить функцию вывода справки и версии программы

Эту задачу можно разбить на 3 подзадачи:
- Создание исполняемого файла
- Создание файлов .alterator и .backend
- упаковка в RPM пакет

## Создаем исполняемый файл
Может быть как бинарным, так и текстовым (написанным на интерпретируемом языке). После установки должен находиться в каталоге <code>/usr/lib/<имя>/</code>
Исполняемый файл будем делать с помощью bash. Создадим каталог для нашего диагностического инструмента, в нем разместим текстовый файл <code>adt-tool-example</code> (название заменить на свое) и сразу добавим в начало строку, указывающую какой интерпретатор использовать для его запуска, имя программы и версию:
<pre>
-!/bin/bash -e

prog="<тут укажите имя программы>"
version="<сюда подставьте версию>"
</pre>

Далее добавим функции выводящие справку, версию программы и список возможных тестов:

<pre>
show_usage() {
    echo "$prog" 
    echo ""
    echo "Usage: $PROG [options] [<check/test-function-name>]"
    echo ""
    echo "<check/test-function-name> must be a function name from the list of tests"
    echo ""
    echo "Options:"
    echo "  -h, --help      This message"
    echo "  -v, --version      Display version number"
    echo "  -l, --list      List of tests"
    echo ""
    return
}

print_version() {
	echo "$prog" ": " "$version"
	exit 0;
}

list() {
	echo "test1"
	echo "test2"
	echo "test3"
	exit 0;
}
</pre>

Необходимо, чтобы функция <code>list()</code> выводила имена тестов через строку. <code>test1</code>...<code>test3</code> нужно заменить на свои. Значения из этого списка будут использоваться в качестве параметра командной строки для указания, какой именно тест нужно выполнить.

Теперь напишем функции для каждого теста (имена функций <code>test1</code>...<code>test3</code> заменить на свои, в соответствии с названиями тестов). В теле каждой функции нужно написать последовательность команд, описывающих алгоритм тестирования. Если тест прошел успешно, функция должна завершиться с кодом возврата 0. Иначе - с отличным от нуля. Это можно сделать как с помощью <code>exit $?</code> (функция завершится с кодом возврата предыдущей команды), так и указать код возврата явно (<code>exit 0</code> или <code>exit 1</code>)
<pre>
test1() {
	- сюда добавляем свою последовательность команд
	exit $?
}

test2() {
	- сюда добавляем свою последовательность команд
	exit 0
}

test3() {
	- сюда добавляем свою последовательность команд
	exit 1
}
</pre>

Осталось добавить конструкцию, которая в соответствии с переданным параметром запускает нужную функцию. <code>test1</code>...<code>test3</code> заменить на свои.
<pre>
if [ "$-" -eq 1 ]
then
  case "$1" in
    -h | --help) show_usage
    ;;
    -l | --list) list
    ;;
    -v | --version) print_version
    ;;
    test1) test1
    ;;
    test2) test2
    ;;
    test3) test3
    ;;
    -) echo "Unrecognized option: $1" ; show_usage ; exit 1
    ;;
  esac
else
	show_usage
	exit 1
fi
</pre>


## Создаем файлы .alterator и .backend

### .alterator
Напишем файл <code>adt-example.alterator</code> (adt-example заменить на свое, .alterator оставить) в соответствии с [[Шаблон диагностического инструмента для Alt-diagnostic-tool-файл .alterator|шаблоном]], содержащий информацию для GUI.
Добавим в него секцию [Alterator Entry]:
<pre>
[Alterator Entry]
Type=diag1
Name=example_tool
Name[ru_RU]=пример диагностического инструмента 
Name[en_EN]=example tool 

Comment=example tool default description
Comment[ru_RU]=описание примера диагностического инструмента
Comment[en_EN]=description of example diagnostic tool

Icon=system-run
</pre>
Значения всех полей, кроме <code>Type</code> заменим на свои:
- <code>Name</code> - идентификатор набора тестов.
- <code>Name[ru_RU]</code> и <code>Name[en_EN]</code> - название набора тестов на на русском и английском языках.
- <code>Comment</code>, <code>Comment[ru_RU]</code> и <code>Comment[en_EN]</code> - описания на русском и английском языках.
- <code>Icon</code> - имя системной иконки

Далее добавим секции, описывающие тесты. (по одной секции на каждый тест). Секции описывающие тесты выглядят следующим образом.
<pre>
[test1]
Name=test1
Name[ru_RU]=тест1 примера диагностического инструмента
Name[en_US]=test1 of example diagnostic tool
Comment=default description of test 1 in example diagnostic tool
Comment[ru_RU]=описание теста 1 примера диагностического инструмента
Comment[en_US]=default description of test 1 in example diagnostic tool
</pre>
Аналогично предыдущему пункту, значения всех полей заменим на свои.

### .backend
Создадим текстовый файл .<code>adt-example.backend</code> (adt-example заменить на свое, .backend оставить) в соответствии с [[Шаблон диагностического инструмента для Alt-diagnostic-tool-файл .backend|шаблоном]], содержащий информацию для GUI.
Добавим в него секцию Alterator Entry:
<pre>
[Alterator Entry]
Type = Backend
Module = executor
Name = example_tool
Interface = diag1
</pre>
Тут заменим на свое только <code>Name</code>.  Остальные поля оставим как есть.

Добавим секцию Info:
<pre>
[Info]
execute = cat /usr/share/alterator/objects/adt-tool-example/adt-example.alterator
stdout_bytes = enabled
thread_limit = 3
action_id = Info
</pre>
В поле <code>execute</code> заменим<code>adt-example.alterator</code> на имя файла, созданного в предыдущем пункте. Остальные поля оставим как есть.

Добавим секцию Run:
<pre>
[Run]
execute = /usr/lib/adt-tool-example/adt-tool-example {param}
stdout_signal_name = diag1_stdout_signal
stderr_signal_name = diag1_stderr_signal
action_id = Run
</pre>
В поле <code>execute</code> заменим<code>adt-tool-example</code> на имя созданного ранее исполняемого файла. Остальные поля оставим как есть.

Добавим секцию List:
<pre>
[List]
execute = /usr/lib/adt-tool-example/adt-tool-example -l
stdout_strings = enabled
action_id = List
</pre>
В поле <code>execute</code> заменим<code>adt-tool-example</code> на имя созданного ранее исполняемого файла. Остальные поля оставим как есть.


## запаковываем в RPM пакет
Для сборки получившегося диагностического инструмента в RPM пакета с помощью <code>rpmbuild</code> нам будет достаточно написать SPEC-файл. Но для сборки с помощью <code>gear</code> нам потребуется доустановить следующий набор программ:
- git
- gear

### создание git-репозитория
В каталоге проекта выполняем следующюю последовательность команд:
<pre>
test@test $ git init
test@test $ git add ./adt-tool-example
test@test $ git add ./adt-example.alterator
test@test $ git add ./adt-example.backend
test@test $ git commit -m "first commit"
</pre>

### делаем из git-репозитория gear-репозиторий
Создадим в крене каталога файл <code>adt-tool-example.spec</code> (название файла заменить на свое, расширение .spec оставить). Добавим в него строку:
<pre>
%define _unpackaged_files_terminate_build 1
</pre>
Далее добавим поля с информацией о пакете. Значения всех полей кроме <code>Source0</code> заменяем на свои. В поле <code>URL</code> указываем адрес публичного репозитория (если репозитория пока нет - поле можно добавить позже).
<pre>
Name: adt-tool-example
Version: 0.0.1
Release: alt1

Summary: Example tool for ADT.
License: GPLv2+
Group: Other
URL: http://....git
BuildArch: noarch
Source0: %name-%version.tar
</pre>
Добавим секцию с описанием. Описание заменим на свое.
<pre>
%description
Example tool for ADT.
</pre>
Добавим две пустые секции prep и setup
<pre>
%prep
%setup
</pre>
Добавим секцию install.Тут используются макросы. При сборке пакета на их место произойдет подстановка необходимых значений.
- %name - имя программы, вместо него будет подставлено значение поля Name
- %buildroot - будет подставлен путь к каталогу /usr/src/tmp/<имя программы>-buildroot. В этом каталоге будет дерево каталогов и файлов пакета.
- %_libexecdir - каталог, в который попадет исполняемый файл. 
- %_datadir - каталог для файлов, предназначенных только для чтения (в данном случае для .alterator и .backend)
Тут нужно заменить только имена файлов adt-tool-example, adt-example.backend и adt-example.alterator на свои.
<pre>
%install
mkdir -p %buildroot%_libexecdir/%name
mkdir -p %buildroot%_datadir/alterator/backends
mkdir -p %buildroot%_datadir/alterator/objects/%name

install -v -p -m 755 -D adt-tool-example %buildroot%_libexecdir/%name
install -v -p -m 644 -D adt-example.backend %buildroot%_datadir/alterator/backends
install -v -p -m 655 -D adt-example.alterator %buildroot%_datadir/alterator/objects/%name
</pre>
Командой mkdir мы создаем дерево каталогов пакета.
Командой install мы устанавливаем ранее созданные файлы в эти каталоги и прописываем флаги доступа.

Далее добавим секцию и перечислим в ней пути к файлам, которые должны попасть в пакет. Имена файлов заменить на свои.
<pre>
%files
%_libexecdir/%name/adt-tool-example
%_datadir/alterator/backends/adt-example.backend
%_datadir/alterator/objects/%name/adt-example.alterator
</pre>
Если в пакете предполагаются какие либо файлы - необходимо аналогичным образом создать для них каталоги и поместить их туда. Важно: файлы, которые будут в составе пакета должны обязательно лежать внутри каталога %buildroot или одного из его подкаталогов.

Выполним следующую команду, чтобы добавить changelog:
<pre>
add_changelog adt-tool-example.spec --entry="- initial build"
</pre>
Имя spec-файла и текст в кавычках заменить на свои.
Если теперь открыть spec-файл, то можно увидеть появившуюся секцию с changelog'ом:
<pre>
%changelog
- Tue Dec 12 2023 Aleksey Saprunov <sav@altlinux.org> 0.0.1-alt1
- initial build
</pre>

Создадим каталог <code>.gear</code>. в него добавим файл <code>rules</code> со следующим содержимым (имя spec-файла заменить на свое):
<pre>
tar: .
spec: adt-tool-example.spec
</pre>

Выполним следующую последовательность команд:
<pre>
test@test $ git add adt-tool-example.spec
test@test $ git add .gear/rules
test@test $ gear-commit
</pre>

### собираем пакет
Для сборки необходимо выполнить команду:
<pre>
test@test $ gear-hsh -v --no-sisyphus-check
</pre>

После успешной сборки пакет можно будет найти в <code>~/hasher/repo/x86_64/RPMS.hasher/</code>
