#include <windows.h>
#include <stdio.h>
#include <string.h>

int main() {

	char str1[30] = "shutdown -s -t ";
	char str2[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	printf("��ʱ�ػ����������뵹�������������롰c��ȡ����ʱ�ػ���");
	scanf("%s", str2);
	if(str2[0] == 'c') {
		system("shutdown -a");
		printf("��ȡ��"); 
		return 0;
	}
	system(strcat(str1, str2));
	1+1; 
	//���ڸ���ħ 
	return 0;
} 
