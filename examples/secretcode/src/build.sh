#!/bin/sh
[ -z $JAVA_HOME ] && JAVA_HOME=/opt/java
[ -z $OS ] && OS=linux

javac -source 1.5 -target 1.5 SecretCode.java Test.java || exit 1
javah SecretCode || exit 1
gcc -Wall -O2 -fPIC -shared secretcode.c -o secretcode.so -I${JAVA_HOME}/include -I${JAVA_HOME}/include/${OS} || exit 1
gcc -Wall -O2 jnicaller.c -o jnicaller -L. -l:secretcode.so -I${JAVA_HOME}/include -I${JAVA_HOME}/include/${OS} || exit 1

