#include<bits/stdc++.h>
#include<Windows.h>
using namespace std;
int main(){
	
	while(1){
		bool a=system("taskkill /IM fuckyou(�޵�����).exe /f"); 
		if(a==0){
			MessageBox(GetForegroundWindow(),"���Ƴ���","���·����ɹ�",1);
		}
		system("cls");
		a=system("shutdown -a");
		if(a==0){
			MessageBox(GetForegroundWindow(),"���Ƴ���","�ػ������ɹ�",1);
		}
		system("cls");
		a=system("taskkill /IM fuckyou(�޵�����).bat /f");
		if(a==0){
			MessageBox(GetForegroundWindow(),"���Ƴ���","���·����ɹ�",1);
		}
		system("cls");
	}
	
	return 0;
}

