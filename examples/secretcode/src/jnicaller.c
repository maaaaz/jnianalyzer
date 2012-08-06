/* Example on how to call a JNI method without using Java.
 *
 * Copyright (c) 2009 Paulo Matias
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <jni.h>
#include "SecretCode.h"

/* JNI reference:
 * http://java.sun.com/docs/books/jni/html/jniTOC.html
 */

JNIEXPORT const char *GetStringUTFChars(JNIEnv *env, jstring str, jboolean *isCopy) {
    assert(str == (jstring)0x2);

    if(isCopy != NULL) {
        *isCopy = JNI_FALSE;
    }

    return (*env)->reserved0;
}

JNIEXPORT jsize GetStringUTFLength(JNIEnv *env, jstring str) {
    assert(str == (jstring)0x2);
    return strlen((*env)->reserved0);
}

char *new_string = NULL;

JNIEXPORT jstring NewStringUTF(JNIEnv *env, const char *utf) {
    new_string = strdup(utf);
    return (jstring)0x3;
} 

JNIEXPORT void ReleaseStringUTFChars(JNIEnv *env, jstring str, const char* chars) {
    /* nothing needed */
}


int main(int argc, char **argv) {
    struct JNINativeInterface_ ifc;
    struct JNINativeInterface_ *ifc_p = &ifc;

    assert(argc == 2);
    ifc.reserved0 = argv[1];

    ifc.GetStringUTFChars = GetStringUTFChars;
    ifc.GetStringUTFLength = GetStringUTFLength;
    ifc.NewStringUTF = NewStringUTF;
    ifc.ReleaseStringUTFChars = ReleaseStringUTFChars;
    
    assert( Java_SecretCode_encode((JNIEnv *)&ifc_p, (jclass)0x1, (jstring)0x2) == (jstring)0x3 );
    assert( (new_string != NULL) );

    printf("%s\n", new_string);
    free(new_string);

    return 0;
}

