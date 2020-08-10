struct Haha {
    int int1;
    char char1;
    char char2;
    int int2;
};

struct Another {
    char a;
    struct Haha haha;
    int b;
};

int main() {
    struct Haha haha_variable;
    struct Another another_variable;
    return 0;
}
