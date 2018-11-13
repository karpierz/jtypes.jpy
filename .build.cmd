@echo off
setlocal
set JAVA8_HOME=C:\Program Files\Java\jdk1.8.0_181
if not defined JAVA_HOME (set JAVA_HOME=%JAVA8_HOME%)
set javac="%JAVA_HOME%"\bin\javac -encoding UTF-8 -g:none -deprecation -Xlint:unchecked ^
    -source 1.8 -target 1.8 -bootclasspath "%JAVA8_HOME%\jre\lib\rt.jar"
set py=C:\Windows\py.exe -3.6 -B
set vc32="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
pushd "%~dp0"
rmdir /Q/S %TEMP%\jtypes.jpy 2> nul
setlocal
set ARCH=x86
set BUILD_DIR=%TEMP%\jtypes.jpy\build-%ARCH%
mkdir %BUILD_DIR%
call %vc32%
cl /TC /O2 /Ob2 /LD ^
   /wd4133 /Y- /Fd%BUILD_DIR%\ /Fo%BUILD_DIR%\ ^
   /Fe.\src\jt\jpy\_java\org\jpy\jpy-windows-%ARCH%.dll ^
   /I..\jtypes.jni\src .\src\jt\jpy\_java\org\jpy\jpy.c ^
   /link /IMPLIB:%BUILD_DIR%\jt.lib /INCREMENTAL:NO
endlocal
setlocal
set ARCH=x64
set BUILD_DIR=%TEMP%\jtypes.jpy\build-%ARCH%
mkdir %BUILD_DIR%
call %vc64%
cl /TC /O2 /Ob2 /LD ^
   /wd4133 /Y- /Fd%BUILD_DIR%\ /Fo%BUILD_DIR%\ ^
   /Fe.\src\jt\jpy\_java\org\jpy\jpy-windows-%ARCH%.dll ^
   /I..\jtypes.jni\src .\src\jt\jpy\_java\org\jpy\jpy.c ^
   /link /IMPLIB:%BUILD_DIR%\jt.lib /INCREMENTAL:NO
endlocal
popd
pushd "%~dp0"\src\jt\jpy\_java
%javac% ^
    ..\..\..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\Version.java ^
    org\jpy\*.java ^
    org\jpy\reflect\*.java ^
    org\jpy\annotations\*.java ^
    org\jpy\jsr223\*.java
%py% -m class2py org\jpy\PyLib.class
%py% -m class2py org\jpy\PyLib$CallableKind.class
%py% -m class2py org\jpy\PyLib$Diag.class
%py% -m class2py org\jpy\PyLibConfig.class
%py% -m class2py org\jpy\PyLibConfig$OS.class
%py% -m class2py org\jpy\PyModule.class
%py% -m class2py org\jpy\PyObject.class
%py% -m class2py org\jpy\PyInputMode.class
%py% -m class2py org\jpy\PyDictWrapper.class
%py% -m class2py org\jpy\PyListWrapper.class
%py% -m class2py org\jpy\DL.class
%py% -m class2py org\jpy\KeyError.class
%py% -m class2py org\jpy\StopIteration.class
%py% -m class2py org\jpy\annotations\Mutable.class
%py% -m class2py org\jpy\annotations\Output.class
%py% -m class2py org\jpy\annotations\Return.class
%py% -m class2py org\jpy\reflect\ProxyHandler.class
%py% -m class2py org\jpy\jsr223\ScriptEngineFactoryImpl.class
%py% -m class2py org\jpy\jsr223\ScriptEngineImpl.class
del /F/Q ^
    ..\..\..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\Version.class ^
    org\jpy\*.class ^
    org\jpy\reflect\*.class ^
    org\jpy\annotations\*.class ^
    org\jpy\jsr223\*.class
popd
pushd "%~dp0"\tests\c
rmdir /Q/S build 2> nul & mkdir build
%javac% -d build ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\util\Run.java ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\util\PythonInterpreter.java ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\util\ClassEnquirer.java ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\util\ClassListEnquirer.java ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\core\PyModule.java ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\core\PyObject.java ^
    ..\..\..\jtypes.jvm\src\jt\jvm\java\org\python\core\PyException.java
popd
pushd "%~dp0"\tests
rmdir /Q/S java\classes 2> nul & mkdir java\classes
dir /S/B/O:N ^
    ..\..\jtypes.jvm\src\jt\jvm\java\org\python\Version.java ^
    ..\src\jt\jpy\_java\org\jpy\*.java ^
    java\org\jpy\*.java ^
    2> nul > build.fil
%javac% -d java/classes -classpath java/lib/* @build.fil
del /F/Q build.fil
popd
endlocal
