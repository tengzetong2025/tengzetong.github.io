#include<bits/stdc++.h>
#include<windows.h>
using namespace std;
int main(){
	long long bol=18446744073709551615;
	string how;
	cout<<"What should I do ? Please enter about your key ."<<endl;
	cin>>how;
	transform(how.begin(),how.end(),how.begin(),::tolower);
	if(how.find("open")!=bol){
		string appName;
		cout<<"Find 'open' in your key . What do you want to open ? Please enter your key in your computer ."<<endl;
		cin>>appName;
		cout<<endl;
		transform(appName.begin(),appName.end(),appName.begin(),::tolower);
		if(appName.find("cmd")!=bol){
			system("start cmd");
			system("cls");
		}else if(appName.find("powershell")!=bol){
			system("start powershell");
			system("cls");
		}else{
			system("start help.exe");
			int result = system(appName.c_str());
			
		}
		system("cls"); 
	}if(how.find("code")!=bol){
		system("cls");
		string code;
		cout<<"Please enter the code : "<<endl<<endl;
		cin>>code;
		transform(code.begin(),code.end(),code.begin(),::tolower);
		int result = system(code.c_str());
		string n;
		cout<<"ÊäÈëÈÎÒâ¼ü";
		cin>>n;
	}else if(how.find("count")!=bol){
		system("start count.exe");
	}else{
		cout<<"What ? "<<endl<<endl;
	}
	system("cls");
	system("help.exe");
	return 0;
}
