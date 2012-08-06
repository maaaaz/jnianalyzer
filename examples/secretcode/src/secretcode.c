#include <stdlib.h>
#include <string.h>
#include "SecretCode.h"

static unsigned char xormask[]={0xDE, 0xAD, 0xBE, 0xEF};

JNIEXPORT jstring JNICALL Java_SecretCode_encode(JNIEnv *env, jclass SecretCode, jstring s) {
    jsize i, len;
    const char *chars;
    char *encoded;
    jstring jencoded;

    chars = (*env)->GetStringUTFChars(env, s, NULL);
    len = (*env)->GetStringLengthUTF(env, s);

    encoded = (char *)malloc(2*len + 1);
    encoded[0] = 0;

    for(i = 0; i < len; i++) {
        sprintf(encoded, "%s%02x", encoded, (unsigned char)chars[i] ^ xormask[i % sizeof(xormask)]);
    }

    jencoded = (*env)->NewStringUTF(env, encoded);
    (*env)->ReleaseStringUTFChars(env, s, chars);
    free(encoded);

    return jencoded;
}

