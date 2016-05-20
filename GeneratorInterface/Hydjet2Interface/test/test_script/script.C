#include <iostream>
#include <list>

using namespace std;

struct Pair {
    int a, b;
    Pair(int a = 0, int b = 0);
    Pair(Pair &);
    bool operator==(const Pair &);
    ~Pair();
};

Pair::Pair(int a, int b) {
    this->a = a;
    this->b = b;
}

Pair::Pair(Pair &p) {
    this->a = p.a;
    this->b = p.b;
}

bool Pair::operator==(const Pair &p) {
    bool ret;
    if ((a == p.a && b == p.b) || (a == p.b && b == p.a)) ret = true;
    else ret = false;
    //cout << "COMPARISON: " << ret << endl;
    return ret;
}

Pair::~Pair() {
}


void script()
{
    list<Pair*> l;
    //l.push_back(new Pair(1, 2));

    //int n = 7;
    int n = 11;
    Pair *p;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            p = new Pair(i, j);
            bool fil = false;
            for (list<Pair*>::iterator it = l.begin(); it != l.end(); it++) {
                //cout << "\tCHECK: (" <<  p->a << ", " << p->b << ")\t(" << (*it)->a << ", " << (*it)->b << ")" << endl;
                if ((**it) == *p) {
                    fil = true;
                    break;
                }
            }
            if (fil) {
                delete p;
                continue;
            }
            else {
                l.push_back(p);
                //cout << p->a << " " << p->b << endl;
            }
        }
    }
    //cout << endl << l.size() << endl;
    cout << l.size() << endl;
}

