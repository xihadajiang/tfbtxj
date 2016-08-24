set JAVA_OPTION=-Dfile.encoding=UTF-8 -Xms256m -Xmx256m -XX:MaxPermSize=64m
set MAIN_CLASS=C:\jython2.5.3\jython.jar
java.exe %JAVA_OPTION% -jar %MAIN_CLASS% tx_httpserver1.py
java -Dfile.encoding=UTF-8 -jar /home/gaps32/Jython/jython.jar tx_httpserver1.py
