#include<bits/stdc++.h>
#include<Windows.h>
using namespace std;
int main(){
	
	while(1){
		bool a=system("taskkill /IM fuckyou(无敌整懵).exe /f"); 
		if(a==0){
			MessageBox(GetForegroundWindow(),"抵制程序","整懵反击成功",1);
		}
		system("cls");
		a=system("shutdown -a");
		if(a==0){
			MessageBox(GetForegroundWindow(),"抵制程序","关机反击成功",1);
		}
		system("cls");
		a=system("taskkill /IM fuckyou(无敌整懵).bat /f");
		if(a==0){
			MessageBox(GetForegroundWindow(),"抵制程序","整懵反击成功",1);
		}
		system("cls");
	}
	
	return 0;
}

