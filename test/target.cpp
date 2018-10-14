#include <stdio.h>
#include "target.h"

int g_avalue1 = 0;

namespace test {
	int g_avalue2;
}

class myclass {
public:
    void mymethod(int param_var1) {
        printf("method %d\n", param_var1);
		g_avalue2 ++;
    }
	
	int mem_var1;
	static int cs_value;
};

void testfunc(int param_var1) {
    myclass lc_var;
    lc_var.mymethod(g_avalue1);
	
	if ( g_avalue1 ) {
		char arr[10] = {0};
		arr[1] ++;
		do_something();
	}

	param_var1 ++;
}
