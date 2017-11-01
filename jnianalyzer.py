#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# JNI Analyzer
# A simple tool to help finding JNI calls in a x86/ARM disassembly listing.
#
# Copyright (c) 2012 Thomas Debize
# Entirely based on JNI Analyzer code, Copyright (c) 2005, 2009 Paulo Matias
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
#
# Usage: 
#    Pass the ARM and x86 (AT&T or Intel syntax) disassembly listing via stdin.
#    This was particulary designed for the objdump output.
#    The processed text can be collected at stdout.
# Example:
#    objdump -d file.so | ./jnianalyzer.py > file.s
#
#
# For a JNI call reference, look at
# http://java.sun.com/docs/books/jni/html/jniTOC.html
#

# Global imports
import sys, re

# OptionParser imports
from optparse import OptionParser

# Options definition
option_0 = { 'name' : ('-a', '--architecture'), 'help' : 'Target architecture : x86 or arm', 'nargs' : 1 }
options = [option_0]

# Supported target architecture
x86 = 'x86'
ARM = 'arm'
TARGET_ARCHITECTURE = [x86, ARM]

__jnicalls__ = [
    'GetVersion', 'DefineClass', 'FindClass', 'FromReflectedMethod', 
    'FromReflectedField', 'ToReflectedMethod', 'GetSuperclass', 'IsAssignableFrom', 
    'ToReflectedField', 'Throw', 'ThrowNew', 'ExceptionOccurred', 
    'ExceptionDescribe', 'ExceptionClear', 'FatalError', 'PushLocalFrame', 
    'PopLocalFrame', 'NewGlobalRef', 'DeleteGlobalRef', 'DeleteLocalRef', 
    'IsSameObject', 'NewLocalRef', 'EnsureLocalCapacity', 'AllocObject', 
    'NewObject', 'NewObjectV', 'NewObjectA', 'GetObjectClass', 
    'IsInstanceOf', 'GetMethodID', 'CallObjectMethod', 'CallObjectMethodV', 
    'CallObjectMethodA', 'CallBooleanMethod', 'CallBooleanMethodV', 'CallBooleanMethodA', 
    'CallByteMethod', 'CallByteMethodV', 'CallByteMethodA', 'CallCharMethod', 
    'CallCharMethodV', 'CallCharMethodA', 'CallShortMethod', 'CallShortMethodV', 
    'CallShortMethodA', 'CallIntMethod', 'CallIntMethodV', 'CallIntMethodA', 
    'CallLongMethod', 'CallLongMethodV', 'CallLongMethodA', 'CallFloatMethod', 
    'CallFloatMethodV', 'CallFloatMethodA', 'CallDoubleMethod', 'CallDoubleMethodV', 
    'CallDoubleMethodA', 'CallVoidMethod', 'CallVoidMethodV', 'CallVoidMethodA', 
    'CallNonvirtualObjectMethod', 'CallNonvirtualObjectMethodV', 'CallNonvirtualObjectMethodA', 'CallNonvirtualBooleanMethod', 
    'CallNonvirtualBooleanMethodV', 'CallNonvirtualBooleanMethodA', 'CallNonvirtualByteMethod', 'CallNonvirtualByteMethodV', 
    'CallNonvirtualByteMethodA', 'CallNonvirtualCharMethod', 'CallNonvirtualCharMethodV', 'CallNonvirtualCharMethodA', 
    'CallNonvirtualShortMethod', 'CallNonvirtualShortMethodV', 'CallNonvirtualShortMethodA', 'CallNonvirtualIntMethod', 
    'CallNonvirtualIntMethodV', 'CallNonvirtualIntMethodA', 'CallNonvirtualLongMethod', 'CallNonvirtualLongMethodV', 
    'CallNonvirtualLongMethodA', 'CallNonvirtualFloatMethod', 'CallNonvirtualFloatMethodV', 'CallNonvirtualFloatMethodA', 
    'CallNonvirtualDoubleMethod', 'CallNonvirtualDoubleMethodV', 'CallNonvirtualDoubleMethodA', 'CallNonvirtualVoidMethod', 
    'CallNonvirtualVoidMethodV', 'CallNonvirtualVoidMethodA', 'GetFieldID', 'GetObjectField', 
    'GetBooleanField', 'GetByteField', 'GetCharField', 'GetShortField', 
    'GetIntField', 'GetLongField', 'GetFloatField', 'GetDoubleField', 
    'SetObjectField', 'SetBooleanField', 'SetByteField', 'SetCharField', 
    'SetShortField', 'SetIntField', 'SetLongField', 'SetFloatField', 
    'SetDoubleField', 'GetStaticMethodID', 'CallStaticObjectMethod', 'CallStaticObjectMethodV', 
    'CallStaticObjectMethodA', 'CallStaticBooleanMethod', 'CallStaticBooleanMethodV', 'CallStaticBooleanMethodA', 
    'CallStaticByteMethod', 'CallStaticByteMethodV', 'CallStaticByteMethodA', 'CallStaticCharMethod', 
    'CallStaticCharMethodV', 'CallStaticCharMethodA', 'CallStaticShortMethod', 'CallStaticShortMethodV', 
    'CallStaticShortMethodA', 'CallStaticIntMethod', 'CallStaticIntMethodV', 'CallStaticIntMethodA', 
    'CallStaticLongMethod', 'CallStaticLongMethodV', 'CallStaticLongMethodA', 'CallStaticFloatMethod', 
    'CallStaticFloatMethodV', 'CallStaticFloatMethodA', 'CallStaticDoubleMethod', 'CallStaticDoubleMethodV', 
    'CallStaticDoubleMethodA', 'CallStaticVoidMethod', 'CallStaticVoidMethodV', 'CallStaticVoidMethodA', 
    'GetStaticFieldID', 'GetStaticObjectField', 'GetStaticBooleanField', 'GetStaticByteField', 
    'GetStaticCharField', 'GetStaticShortField', 'GetStaticIntField', 'GetStaticLongField', 
    'GetStaticFloatField', 'GetStaticDoubleField', 'SetStaticObjectField', 'SetStaticBooleanField', 
    'SetStaticByteField', 'SetStaticCharField', 'SetStaticShortField', 'SetStaticIntField', 
    'SetStaticLongField', 'SetStaticFloatField', 'SetStaticDoubleField', 'NewString', 
    'GetStringLength', 'GetStringChars', 'ReleaseStringChars', 'NewStringUTF', 
    'GetStringUTFLength', 'GetStringUTFChars', 'ReleaseStringUTFChars', 'GetArrayLength', 
    'NewObjectArray', 'GetObjectArrayElement', 'SetObjectArrayElement', 'NewBooleanArray', 
    'NewByteArray', 'NewCharArray', 'NewShortArray', 'NewIntArray', 
    'NewLongArray', 'NewFloatArray', 'NewDoubleArray', 'GetBooleanArrayElements', 
    'GetByteArrayElements', 'GetCharArrayElements', 'GetShortArrayElements', 'GetIntArrayElements', 
    'GetLongArrayElements', 'GetFloatArrayElements', 'GetDoubleArrayElements', 'ReleaseBooleanArrayElements', 
    'ReleaseByteArrayElements', 'ReleaseCharArrayElements', 'ReleaseShortArrayElements', 'ReleaseIntArrayElements', 
    'ReleaseLongArrayElements', 'ReleaseFloatArrayElements', 'ReleaseDoubleArrayElements', 'GetBooleanArrayRegion', 
    'GetByteArrayRegion', 'GetCharArrayRegion', 'GetShortArrayRegion', 'GetIntArrayRegion', 
    'GetLongArrayRegion', 'GetFloatArrayRegion', 'GetDoubleArrayRegion', 'SetBooleanArrayRegion', 
    'SetByteArrayRegion', 'SetCharArrayRegion', 'SetShortArrayRegion', 'SetIntArrayRegion', 
    'SetLongArrayRegion', 'SetFloatArrayRegion', 'SetDoubleArrayRegion', 'RegisterNatives', 
    'UnregisterNatives', 'MonitorEnter', 'MonitorExit', 'GetJavaVM', 
    'GetStringRegion', 'GetStringUTFRegion', 'GetPrimitiveArrayCritical', 'ReleasePrimitiveArrayCritical', 
    'GetStringCritical', 'ReleaseStringCritical', 'NewWeakGlobalRef', 'DeleteWeakGlobalRef', 
    'ExceptionCheck', 'NewDirectByteBuffer', 'GetDirectBufferAddress', 'GetDirectBufferCapacity', 
    'GetObjectRefType', 'DestroyJavaVM', 'AttachCurrentThread', 'DetachCurrentThread', 
    'GetEnv', 'AttachCurrentThreadAsDaemon'
]

def get_jnicall(displacement):
    """ Returns a string containing the JNI call name if the displacement
    is valid. Otherwise returns None. """
    global __jnicalls__
    
    # A valid displacement here must be a multiple of four if we are in a 32 bit architecture.
    if (displacement % 4) != 0:
        return None
    # Get the JNINativeInterface_ struct entry index from the displacement.
    i = displacement // 4
    
    # The first four names in the struct are reserved pointers, and are not used for JNI calls.
    if i < 4:
        return None
    # Realign the index to match __jnicalls__.
    i -= 4
   
    # Check if the index is present in __jnicalls__.
    if i >= len(__jnicalls__):
        return None
    
    # Everything is OK, return the JNI call name.
    return __jnicalls__[i]


def x86_analysis():
    regs = {}
    
    while True:
        line = sys.stdin.readline()
        
        if line == '':
            break  # EOF
        
        # Strip trailing '\n'.
        line = line[:-1]

        # Check for a possible JNINativeInterface_ entry reference  
        # in a mov instruction like 'mov 0xNN(%reg0),%reg1', and hold state in the regs dict.
        m_att = re.search(r'mov\s+([x0-9a-f]+)\(%[a-z]{2,}\)\s*,\s*(%[a-z]{2,})', line, re.IGNORECASE)
        m_intel = re.search(r'mov\s+([a-z]{2,}),DWORD\s+PTR\s+\[[a-z]{2,}\+([x0-9a-f]+)\]', line)
        if m_att or m_intel:
            try:
                # Get the displacement and the register.
                if m_att :
                    displacement = int(m_att.group(1), 16)
                    reg = m_att.group(2)
                
                elif m_intel :
                    displacement = int(m_intel.group(2), 16)
                    reg =  m_intel.group(1)
                
                # Look for a possible JNI call.
                jnicall = get_jnicall(displacement)
                
                # If possibly valid, hold a state for this register.
                if jnicall:
                    # Hold the state.
                    regs[reg] = jnicall
                    
                    # Avoid clearing the state in the next side-effect test.
                    print(line)
                    continue
            except:
                pass
        
        # Check for a call like 'call *%reg'.
        # If we have state held for the %reg register, then it's probably a JNI call.
        m_att = re.search(r'call\s+\*\s*(%[a-z]{2,})', line, re.IGNORECASE)
        m_intel = re.search(r'call\s+([a-z]{2,})', line)
        patterns = [m_att, m_intel]
        for p in patterns :
            if p :
                # Get the register.
                reg = p.group(1)
                
                # Check for state.
                if reg in regs:
                    # We have state. Add a JNI call reference.
                    line += '\t\t;jnicall: ' + regs[reg]
                
        # Check for a call like 'call *0xNN(%reg)'.
        # If the displacement 0xNN is a valid JNINativeInterface_struct displacement, then it's probably a JNI call.
        m_att = re.search(r'call\s+\*\s*([x0-9a-f]+)\(%[a-z]{2,}\)', line, re.IGNORECASE)
        m_intel = re.search(r'call\s+DWORD\s+PTR\s+\[[a-z]{2,}\+([x0-9a-f]+)\]', line, re.IGNORECASE)
        patterns = [m_att, m_intel]
        for p in patterns :
            if p :
                try:
                    # Get the displacement.
                    displacement = int(p.group(1), 16)
                    
                    # Look for a possible JNI call.
                    jnicall = get_jnicall(displacement)
                    
                    # If possibly valid, add a JNI call reference.
                    if jnicall:
                        line += '\t\t;jnicall: ' + jnicall
                except:
                    pass
                   
        # Check if the instruction has a side-effect on a register.
        m = re.search(r'(,|pop\s)\s*(%[a-z]{2,})\s*(?:;.*)?$', line, re.IGNORECASE)
        if m:
            # Get the register.
            reg = m.group(2)
            
            # Remove any state held for this register.
            if reg in regs:
                del regs[reg]
        
        print(line)


def arm_analysis() :
    regs = {}
    
    while True:
        line = sys.stdin.readline()
        
        if line == '':
            break  # EOF
        
        # Strip trailing '\n'.
        line = line[:-1]

        # Check for a possible JNINativeInterface_ entry reference  
        # in a mov instruction like 'movs   reg, #XX', and hold state in the regs dict.
        m = re.search(r'movs\s+(r[0-9]+),\s+#([0-9]+)', line, re.IGNORECASE)
        if m :
            try :               
                # Get the displacement (multiplied by 4 here, as the listing prints out decimal and pointer-size independant offsets) and the register.
                displacement = int(m.group(2),10)*4
                reg = m.group(1)
                
                # Look for a possible JNI call.
                jnicall = get_jnicall(displacement)
                
                if jnicall:
                    # Hold the state.
                    regs[reg] = jnicall
                    # Avoid clearing the state in the next side-effect test.
                    print(line)
                    continue
            
            except:
                pass
        
        # Check for a call like 'lsls reg, reg, #2'. (Left Shift by 2^2 == 4 == pointer size)
        # If we have state held for the reg register, then it's probably a JNI call.
        m = re.search(r'lsls\s+(r[0-9]+),\s+(r[0-9]+),\s+#2', line, re.IGNORECASE)
        if m :
            # Get the register.
            reg1 = m.group(1)
            reg2 = m.group(2)
            
            # Check for state.
            if reg1 == reg2 and reg1 in regs:
                # We have state. Add a JNI call reference.
                line += '\t\t;jnicall: ' + regs[reg1]
                
                # Remove any state held for this register.
                del regs[reg1]
        
        print(line)

def main(options, arguments) :
    if (options.architecture != None) and (options.architecture in TARGET_ARCHITECTURE) :
        if options.architecture == x86 :
            x86_analysis()
        elif options.architecture == ARM :
            arm_analysis()
    else :
        parser.error("Please specify a valid target architecture")

if __name__ == '__main__':
    parser = OptionParser()
    for option in options :
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    main(options, arguments)
