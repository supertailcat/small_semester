#include <windows.h>
#include <stdio.h>
#include <string.h>

int main() {

	char str1[30] = "shutdown -s -t ";
	char str2[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	printf("定时关机程序。请输入倒数秒数：（输入“c”取消定时关机）");
	scanf("%s", str2);
	if(str2[0] == 'c') {
		system("shutdown -a");
		printf("已取消"); 
		return 0;
	}
	system(strcat(str1, str2));
	1+1; 
	//李在赣神魔 
	return 0;
} 
