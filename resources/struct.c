struct Haha {
    int a;
    char b;
    char c;
    int d;
};

struct Another {
    char f;
    struct Haha haha;
    int e;
};

int main() {
    struct Haha haha;
    struct Another another;
    return 0;
}
