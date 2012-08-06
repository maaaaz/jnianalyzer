JNI Analyzer
============

Description
-----------
A simple tool to help finding JNI calls in a x86/ARM disassembly listing

Originally presented here http://www.thebugmagazine.org/magazine/bug04/0x02-engenharia-reversa-em-apps-java.txt, this script has been modified in order to support both x86 syntaxes and ARM.
Thus, it can be used for debugging/reverse engineering android native libraries.

Features
--------
* Support of x86 AT&T and Intel syntaxes
* Support of ARM

Usage
-----
Pass the ARM and x86 (AT&T or Intel syntax) disassembly listing via stdin.
This was particulary designed for the objdump output.
The processed text can be collected at stdout.

* x86 AT&T syntax libraries
```
$ objdump -d mylib.so | python jnianalyzer.py -a x86
```
* x86 intel syntax libraries
```
$ objdump -M intel -d mylib.so | python jnianalyzer.py -a x86
```
* ARM libraries
```
$ tools/arm-linux-androideabi-objdump -d mylib.so | python jnianalyzer.py -a arm
```
Pass the ARM and x86 (AT&T or Intel syntax) disassembly listing via stdin.

Example
-------
You can find some compiled libraries, coming from different projects, and their source code in the `example` folder.

* hello-jni : sample from android-ndk-r8b
```
$ objdump -M intel -d examples/hello-jni/libs/x86/libhello-jni.so | python jnianalyzer.py -a x86
...
00000500 <Java_com_example_hellojni_HelloJni_stringFromJNI>:
 500:	53                   	push   ebx
 501:	83 ec 18             	sub    esp,0x18
 504:	e8 e8 ff ff ff       	call   4f1 <__cxa_atexit@plt+0x101>
 509:	81 c3 cf 1a 00 00    	add    ebx,0x1acf
 50f:	8b 44 24 20          	mov    eax,DWORD PTR [esp+0x20]
 513:	8b 00                	mov    eax,DWORD PTR [eax]
 515:	8b 90 9c 02 00 00    	mov    edx,DWORD PTR [eax+0x29c]
 51b:	8d 83 5c e5 ff ff    	lea    eax,[ebx-0x1aa4]
 521:	89 44 24 04          	mov    DWORD PTR [esp+0x4],eax
 525:	8b 44 24 20          	mov    eax,DWORD PTR [esp+0x20]
 529:	89 04 24             	mov    DWORD PTR [esp],eax
 52c:	ff d2                	call   edx		;jnicall: NewStringUTF
 52e:	83 c4 18             	add    esp,0x18
 531:	5b                   	pop    ebx
 532:	c3                   	ret    
 533:	90                   	nop
...
```
```
$ tools/arm-linux-androideabi-objdump -d examples/hello-jni/libs/armeabi/libhello-jni.so | python jnianalyzer.py -a arm
...
00000c24 <Java_com_example_hellojni_HelloJni_stringFromJNI>:
     c24:       b500            push    {lr}
     c26:       b083            sub     sp, #12
     c28:       9001            str     r0, [sp, #4]
     c2a:       9100            str     r1, [sp, #0]
     c2c:       9b01            ldr     r3, [sp, #4]
     c2e:       681a            ldr     r2, [r3, #0]
     c30:       23a7            movs    r3, #167        ; 0xa7
     c32:       009b            lsls    r3, r3, #2              ;jnicall: NewStringUTF
     c34:       58d2            ldr     r2, [r2, r3]
     c36:       9901            ldr     r1, [sp, #4]
     c38:       4b04            ldr     r3, [pc, #16]   ; (c4c <Java_com_example_hellojni_HelloJni_stringFromJNI+0x28>)
     c3a:       447b            add     r3, pc
     c3c:       1c08            adds    r0, r1, #0
     c3e:       1c19            adds    r1, r3, #0
     c40:       4790            blx     r2
...
```

Copyright and license
---------------------
JNI Analyzer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

JNI Analyzer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with JNI Analyzer. 
If not, see http://www.gnu.org/licenses/.

Greetings
-------------
* Paulo Matias < thotypous [at] gmail [dot] com >, author of the original JNI Analyzer
