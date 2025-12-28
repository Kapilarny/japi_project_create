#include "plugin.h"

#include <JoJoAPI.h>

JAPIModMeta GetModMeta() {
    static JAPIModMeta meta = {
        "%%{guid}%%",
        "%%{author}%%",
        "%%{guid}%%",
        "1.0.0",
        "%%{description}%%"
    };

    return meta;
}

void ModInit() {
    JINFO("%%{guid}%% initialized!");
}